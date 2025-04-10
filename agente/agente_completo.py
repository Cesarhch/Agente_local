import os
import sqlite3
import numpy as np
import uuid
from datetime import datetime
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader, TextLoader, PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import faiss

# Configuración global
RAG_DB_PATH = "faiss_index/index.faiss"
LTM_DB = "long_term_memory"
CONVERSATION_DB = "sqlite:///conversations.db"
METADATA_DB = "metadata.db"

# Clase de memoria integrada
class MemorySystem:
    def __init__(self, user_id):
        self.user_id = user_id
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large")

        # Cargar FAISS si ya existe
        self.faiss_index = None
        self.faiss_ids = []
        if os.path.exists(RAG_DB_PATH) and os.path.exists(METADATA_DB):
            self.faiss_index = faiss.read_index(RAG_DB_PATH)
            with sqlite3.connect(METADATA_DB) as conn:
                cursor = conn.cursor()
                self.faiss_ids = [row[0] for row in cursor.execute("SELECT id FROM metadata").fetchall()]

        # Memoria a largo plazo
        self.ltm_vectorstore = Chroma(
            collection_name="ltm",
            embedding_function=self.embeddings,
            persist_directory=LTM_DB
        )

        # Historial conversacional
        self.history = SQLChatMessageHistory(
            connection=CONVERSATION_DB + "?check_same_thread=False",
            session_id=str(uuid.uuid4())
        )

    def initialize_rag(self, folder_path="rag"):
        loaders = {".pdf": PyPDFLoader, ".txt": TextLoader, ".py": PythonLoader}
        documents = []
        for file in os.listdir(folder_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in loaders:
                try:
                    loader = loaders[ext](os.path.join(folder_path, file))
                    loaded_docs = loader.load()
                    for doc in loaded_docs:
                        doc.metadata["source"] = file
                    documents.extend(loaded_docs)
                except Exception as e:
                    print(f"Error cargando {file}: {e}")

        splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
        chunks = splitter.split_documents(documents)

        dim = 1024
        index = faiss.IndexFlatIP(dim)
        ids = []
        all_embeddings = []

        os.makedirs("faiss_index", exist_ok=True)
        os.makedirs(os.path.dirname(METADATA_DB), exist_ok=True)

        with sqlite3.connect(METADATA_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY,
                    file_name TEXT,
                    content TEXT
                )
            """)
            for chunk in chunks:
                text = chunk.page_content
                embedding = self.embeddings.embed_query(text)
                embedding = np.array(embedding, dtype="float32")
                norm = np.linalg.norm(embedding)
                if norm != 0:
                    embedding /= norm
                all_embeddings.append(embedding)

                cursor.execute("INSERT INTO metadata (file_name, content) VALUES (?, ?)", (
                    chunk.metadata.get("source", "desconocido"),
                    text
                ))
                ids.append(cursor.lastrowid)
            conn.commit()

        vectors = np.vstack(all_embeddings)
        index.add(vectors)
        faiss.write_index(index, RAG_DB_PATH)

        self.faiss_index = index
        self.faiss_ids = ids

    def store_conversation(self, input_msg, response):
        self.ltm_vectorstore.add_texts(
            texts=[f"Usuario: {input_msg}\nAsistente: {response}"],
            metadatas=[{
                "user_id": self.user_id,
                "timestamp": datetime.now().isoformat(),
                "type": "conversation"
            }]
        )
        self.history.add_user_message(input_msg)
        self.history.add_ai_message(response)

    def get_context(self, query):
        rag_context = []
        keywords = [
            "busca en", "consulta los documentos", "segun los archivos",
            "en el pdf", "en los textos", "en los documentos", "segun el rag",
            "consulta el rag", "de los archivos", "segun los documentos"
        ]
        if self.faiss_index and any(k in query.lower() for k in keywords):
            embedding = self.embeddings.embed_query(query)
            embedding = np.array(embedding, dtype="float32")
            norm = np.linalg.norm(embedding)
            if norm != 0:
                embedding /= norm

            D, I = self.faiss_index.search(np.expand_dims(embedding, axis=0), 3)
            with sqlite3.connect(METADATA_DB) as conn:
                cursor = conn.cursor()
                for idx in I[0]:
                    row = cursor.execute("SELECT file_name, content FROM metadata WHERE id = ?", (self.faiss_ids[idx],)).fetchone()
                    if row:
                        rag_context.append(f"[{row[0]}]\n{row[1]}")

        ltm_context = self.ltm_vectorstore.similarity_search(query, k=2, filter={"user_id": self.user_id})

        return "\n".join([
            "Contexto de documentos:",
            *rag_context,
            "\nContexto histórico:",
            *[doc.page_content for doc in ltm_context]
        ])

# Modelo y plantilla
phi4 = ChatOllama(model="phi4", temperature=0.3, stream=True)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """Eres Lara. Combina esta información:
{context}
Historial actual: {chat_history}
Responde de forma precisa y técnica."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

def setup_chain(memory):
    return (
        {
            "input": RunnablePassthrough(),
            "context": RunnableLambda(lambda x: memory.get_context(x["input"])),
            "chat_history": lambda _: memory.history.messages
        }
        | prompt_template
        | phi4
        | StrOutputParser()
    )

def main():
    user_id = "cesar"
    memory = MemorySystem(user_id)
    chain = setup_chain(memory)

    print("\n=== Lara (RAG + Memoria Permanente) ===")
    print("Comandos especiales: 'salir', 'recargar'")

    while True:
        user_input = input("\nTú: ").strip()

        if user_input.lower() == "salir":
            print("\nLara: ¡Hasta luego!")
            break

        if user_input.lower() == "recargar":
            memory.initialize_rag()
            print("\nLara: Documentos recargados correctamente")
            continue

        print("\nLara:", end=" ", flush=True)
        response = []

        try:
            for chunk in chain.stream({"input": user_input}):
                print(chunk, end="", flush=True)
                response.append(chunk)

            memory.store_conversation(user_input, "".join(response))

        except Exception as e:
            print(f"\nError: {str(e)}")

        print("\n" + "-"*50)

if __name__ == "__main__":
    if not os.path.exists("rag"):
        os.makedirs("rag")
        print("\n¡Coloca documentos en la carpeta 'rag'!")
    main()
