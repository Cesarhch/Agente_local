from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
import sys

# pip install langchain langchain-core langchain-community langchain-ollama

# 1. Configuración del modelo con streaming
phi4 = ChatOllama(
    model="phi3",
    temperature=0.3,
    stream=True,  # Habilitar respuestas en streaming
)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. Memoria conversacional con límite de 10 mensajes
message_history = ChatMessageHistory()

def get_last_messages(n=10):
    """ Obtiene los últimos n mensajes del historial """
    return message_history.messages[-n:]

# 5. Plantilla de prompt mejorada
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """Eres Lara, un asistente IA inteligente. Responde usando:
     Contexto relevante: {context}
     Historial de conversación: {chat_history}
     Se breve, no repetiras el historial de conversacion en tu respuesta."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

# 6. Generar respuesta con RAG + Memoria y streaming
def generate_response(user_input):
    
    # Obtener historial de conversación
    chat_history = get_last_messages(10)

    # Recuperar contexto de los documentos
    context = ""

    # Crear el input del modelo
    prompt_input = prompt_template.format(
        context=context,
        chat_history=chat_history,
        input=user_input
    )

    # Enviar el prompt al modelo con streaming
    response_stream = phi4.stream(prompt_input)

    # Mostrar la respuesta en tiempo real
    print("Lara: ", end="", flush=True)
    full_response = ""
    for chunk in response_stream:
        text = chunk.content
        sys.stdout.write(text)
        sys.stdout.flush()
        full_response += text

    print("\n")  # Salto de línea al final
    
    # Guardar la respuesta en el historial
    message_history.add_user_message(user_input)
    message_history.add_ai_message(full_response)

# 7. Interfaz interactiva en main()
def main():
    print("¡Hola! Soy Lara, tu asistente. Pregunta lo que quieras. Escribe 'salir' para terminar.")
    while True:
        user_input = input("\nTú: ")
        if user_input.lower() == "salir":
            print("¡Hasta luego!")
            break
        generate_response(user_input)

if __name__ == "__main__":
    main()
