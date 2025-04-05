from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Configura el modelo Phi-3
phi3 = ChatOllama(
    model="phi3",  
    temperature=0.7,  # Controla la creatividad (0 = preciso, 1 = creativo)
    stream=True,      # Habilita streaming
)

# 2. Plantilla para el chat (opcional, pero útil para contexto)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente IA llamado Lara. Responde de forma concisa y muy breve."),
    ("human", "{user_input}"),
])

# 3. Cadena de procesamiento
chain = prompt_template | phi3 | StrOutputParser()

def main():
    while True:
        user_input = input("\nTu: ")
        
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("¡Hasta luego!")
            break
        
        if not user_input.strip():
            print("Por favor, escribe algo.")
            continue
        
        # Generar y mostrar respuesta en streaming
        print("\nLara:", end="", flush=True)
        
        for chunk in chain.stream({"user_input": user_input}):
            print(chunk, end="", flush=True)

if __name__ == "__main__":
    main()
