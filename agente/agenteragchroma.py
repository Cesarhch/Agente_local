from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader, TextLoader, PythonLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os
import keyboard  # Para detectar la barra espaciadora

# pip install langchain langchain-core langchain-community langchain-text-splitters langchain-ollama chromadb pypdf keyboard

# Configuración del modelo y embeddings
phi3 = ChatOllama(model="phi3", temperature=0.3, stream=True)
embeddings = OllamaEmbeddings(model="nomic-embed-text")  # para descargar el modelo:ollama pull nomic-embed-text

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

    print(f"Documentos cargados: {len(documents)}")
    return documents

# Dividir documentos en fragmentos optimizados
def process_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Fragmentos creados: {len(chunks)}")
    return chunks

# Crear base de datos de vectores en Chroma
def setup_rag():
    documents = load_documents()
    if not documents:
        raise ValueError("¡No hay archivos en la carpeta 'rag'!")

    chunks = process_documents(documents)
    
    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    return retriever

# Generar respuesta con contexto de los documentos
def query_rag(question):
    retriever = setup_rag()
    docs = retriever.invoke(question)  # Usar invoke en lugar de get_relevant_documents
    context = "\n".join([doc.page_content for doc in docs])

    if not context.strip():
        return "No encontré información relevante en los documentos."

    # Crear la plantilla correctamente para el sistema
    prompt_template = ChatPromptTemplate.from_messages([ 
        ("system", "Las respuestas deben ser breves y concisas, las respuestas solo seran con respecto a la pregunta sin decir mas informacion:\n{context}"),
        ("human", "{question}")
    ])

    # Formateamos la plantilla con los valores correctos
    formatted_prompt = prompt_template.format(context=context, question=question)

    # Ahora pasamos el prompt correctamente formateado a phi3
    response = ""
    for chunk in phi3.stream(formatted_prompt):
        response += chunk.content  # Extraemos el contenido de cada fragmento
        
        # Detecta si se presiona la barra espaciadora para detener la impresión
        if keyboard.is_pressed('space'):
            print("\n¡Interrumpido por el usuario!")
            break
        
        print(chunk.content, end='', flush=True)

    return response

# Función principal para interactuar con el modelo desde el prompt
def main():
    print("Bienvenido al asistente de búsqueda. ¡Puedes comenzar a hacer preguntas!")
    while True:
        question = input("\nTu pregunta: ").strip()
        if question.lower() in ["salir", "exit", "quit"]:
            print("\n¡Hasta luego!")
            break

        if not question:
            continue

        try:
            respuesta = query_rag(question)
            print(f"\nRespuesta: {respuesta}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
