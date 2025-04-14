from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    PythonLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
import os

# pip install \
#  langchain \
#  langchain-core \
#  langchain-community \
#  langchain-text-splitters \
#  langchain-ollama \
#  faiss-cpu \
#  pypdf \
#  tiktoken


# 1. Configuración del modelo
phi3 = ChatOllama(
    model="phi3",
    temperature=0.3,
    stream=True,
)
embeddings = OllamaEmbeddings(model="nomic-embed-text")  # Embeddings eficientes

# 2. Cargar documentos (PDF, TXT, PY)
def load_documents(folder_path="rag"):
    loaders = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".py": PythonLoader,
    }
    documents = []
    
    for file in os.listdir(folder_path):
        ext = os.path.splitext(file)[1].lower()
        if ext in loaders:
            try:
                loader = loaders[ext](os.path.join(folder_path, file))
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error cargando {file}: {e}")
    
    return documents

# 3. Procesar documentos (chunking)
def process_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return text_splitter.split_documents(documents)

# 4. Plantilla RAG
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """Eres Lara, un asistente IA. Responde basándote en este contexto:
     {context}
     - Sé concisa (1-2 frases).
     - Si no sabes la respuesta, di 'No encontré información relevante'."""),
    ("human", "{question}"),
])

# 5. Configurar RAG
def setup_rag():
    documents = load_documents()
    if not documents:
        raise ValueError("¡No hay archivos en la carpeta 'rag'! (Formatos soportados: .pdf, .txt, .py)")
    
    processed_docs = process_documents(documents)
    vectorstore = FAISS.from_documents(processed_docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt_template
        | phi3
        | StrOutputParser()
    )
    return rag_chain

def main():
    try:
        rag_chain = setup_rag()
        print("\n=== Chat con Lara (Phi-3 + RAG) ===")
        print("Soporta PDF, TXT y PY. Escribe 'salir' para terminar.\n")
        
        while True:
            user_input = input("Tú: ").strip()
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("\nLara: ¡Hasta luego!")
                break
                
            if not user_input:
                continue
                
            print("\nLara:", end=" ", flush=True)
            try:
                for chunk in rag_chain.stream(user_input):
                    print(chunk, end="", flush=True)
            except Exception as e:
                print(f"\nError: {e}")
            print("\n" + "-"*50)
            
    except Exception as e:
        print(f"Error inicial: {e}")

if __name__ == "__main__":
    if not os.path.exists("rag"):
        os.makedirs("rag")
        print("¡Coloca tus archivos en la carpeta 'rag' (PDF, TXT o PY)!")
    else:
        main()
