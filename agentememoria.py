from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader, TextLoader, PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import os

# 1. Configuración del modelo
phi4 = ChatOllama(
    model="phi4",
    temperature=0.3,
    stream=True,
)
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# 2. Memoria conversacional
message_history = ChatMessageHistory()

# 3. Cargar y procesar documentos
def load_and_process_documents(folder_path="rag"):
    loaders = {".pdf": PyPDFLoader, ".txt": TextLoader, ".py": PythonLoader}
    documents = []
    for file in os.listdir(folder_path):
        ext = os.path.splitext(file)[1].lower()
        if ext in loaders:
            try:
                loader = loaders[ext](os.path.join(folder_path, file))
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error cargando {file}: {e}")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
    return text_splitter.split_documents(documents)

# 4. Plantilla mejorada
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """Eres Lara, un asistente IA inteligente. Responde usando:
     Contexto relevante: {context}
     Historial de conversación: {chat_history}
     Sé concisa (1-2 frases máximo)."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

# 5. Configuración de la cadena RAG
def setup_rag():
    documents = load_and_process_documents()
    if not documents:
        raise ValueError("¡Coloca archivos en la carpeta 'rag' (PDF, TXT o PY)!")
    
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    def get_current_history(_):
        return message_history.messages
    
    rag_chain = (
        {
            "context": retriever,
            "input": RunnablePassthrough(),
            "chat_history": RunnableLambda(get_current_history)
        }
        | prompt_template
        | phi4
        | StrOutputParser()
    )
    return rag_chain

def main():
    try:
        rag_chain = setup_rag()
        print("\n=== Chat con Lara (Phi-4 + RAG + Memoria) ===")
        print("Escribe 'salir' para terminar.\n")
        
        while True:
            user_input = input("Tú: ").strip()
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("\nLara: ¡Hasta luego!")
                break
                
            if not user_input:
                continue
            
            # Guardar mensaje del usuario
            message_history.add_message(HumanMessage(content=user_input))
            
            # Generar respuesta
            print("\nLara:", end=" ", flush=True)
            response = []
            for chunk in rag_chain.stream(user_input):  # Pasa directamente el string
                print(chunk, end="", flush=True)
                response.append(chunk)
            
            # Guardar respuesta de la IA
            message_history.add_message(AIMessage(content="".join(response)))
            print("\n" + "-"*50)
            
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists("rag"):
        os.makedirs("rag")
        print("¡Coloca tus documentos en la carpeta 'rag'!")
    main()
