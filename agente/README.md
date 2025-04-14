# ChatBot con LangChain y Phi-3

Este proyecto es un chatbot basado en el modelo **Phi-3** utilizando LangChain y Ollama. Permite interacción en tiempo real a través de la terminal, generando respuestas concisas y en streaming.

## Características
- Usa el modelo **Phi-3** a través de **LangChain-Ollama**.
- Admite **streaming** de respuestas.
- Configurable en cuanto a temperatura (nivel de creatividad).
- Plantilla de prompts para mejorar la coherencia de las respuestas.

## Instalación
Antes de ejecutar el chatbot, asegúrate de tener instalado Python 3.10+ y las dependencias necesarias.

### 1. Crear un entorno virtual (opcional pero recomendado)
```sh
conda create --name chatbot_env python=3.10.16 (o tambien puedes escribir: conda create -n cursoIA python=3.10.16)

conda activate chatbot_env
```

### 2. Instalar dependencias
```sh
pip install langchain langchain-ollama
```

### 3. Verificar que **Ollama** está instalado y configurado correctamente
Si aún no tienes Ollama, instálalo desde [aquí](https://ollama.com).

## Ejecución
Para iniciar el chatbot, ejecuta:
```sh
python agentelocal.py
```
Luego, simplemente escribe tu consulta en la terminal y el chatbot responderá en tiempo real. Para salir, usa `salir`, `exit` o `quit`.

## Configuración
Puedes modificar estos parámetros en el código:
- **Temperatura:** Ajusta `temperature=0.7` en `ChatOllama()` para hacer el modelo más o menos creativo.
- **Prompt del asistente:** Cambia el mensaje en `ChatPromptTemplate.from_messages()` para personalizar la personalidad del chatbot.

## Licencia
Este proyecto está bajo la licencia **MIT**. Puedes usarlo, modificarlo y distribuirlo libremente.

---
Contribuciones y mejoras son bienvenidas.

