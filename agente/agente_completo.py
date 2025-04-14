from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader, TextLoader, PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os
import keyboard
import sys

# pip install langchain langchain-core langchain-community langchain-text-splitters langchain-ollama chromadb pypdf keyboard

# Configuración del modelo y embeddings
modelo = ChatOllama(model="phi3", temperature=0.3, stream=True)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Memoria conversacional
message_history = ChatMessageHistory()
def get_last_messages(n=10):
    return message_history.messages[-n:]

# Cargar documentos
def load_documents(folder_path="rag"):
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
    return documents

# Fragmentar documentos
def process_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

# Configurar RAG (una vez)
def setup_rag():
    documents = load_documents()
    if not documents:
        raise ValueError("¡No hay archivos en la carpeta 'rag'!")
    chunks = process_documents(documents)
    vectorstore = Chroma.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

retriever = setup_rag()

# Plantilla de prompt
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Eres Lara, una asistente IA. Responde de forma breve, natural y útil."),
    ("system", "Información relevante extraída de documentos:\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Generar respuesta combinando RAG + memoria
def generate_response(user_input):
    chat_history = get_last_messages(10)
    docs = retriever.invoke(user_input)

    # Filtrar contexto solo si el contenido tiene texto útil
    context = ""
    if docs:
        contextos_validos = [doc.page_content.strip() for doc in docs if len(doc.page_content.strip()) > 10]
        context = "\n".join(contextos_validos)

    if context:
        print("\n[Contexto con RAG]")
        #print(context[:300] + "\n..." if len(context) > 300 else context)
    else:
        print("\n[No se usó contexto del RAG.]")

    # Formatear prompt
    prompt_input = prompt_template.format(
        context=context,
        chat_history=chat_history,
        input=user_input
    )

    # Stream respuesta
    print("Lara: ", end="", flush=True)
    full_response = ""
    for chunk in modelo.stream(prompt_input):
        content = chunk.content
        sys.stdout.write(content)
        sys.stdout.flush()
        full_response += content

        if keyboard.is_pressed('space'):
            print("\n(Interrumpido por el usuario)")
            break

    print("\n")
    message_history.add_user_message(user_input)
    message_history.add_ai_message(full_response)

# Interfaz interactiva
def main():
    print("¡Hola! Soy Lara, tu asistente. Pregúntame lo que quieras. Escribe 'salir' para terminar.")
    while True:
        user_input = input("\nTú: ").strip()
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("¡Hasta luego!")
            break
        if not user_input:
            continue
        try:
            generate_response(user_input)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
