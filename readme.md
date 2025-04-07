# Sistema de Monitoreo con ESP32 y Agente de Inteligencia Artificial

Este proyecto implementa un flujo de lectura y procesamiento de datos ambientales utilizando un **sensor DHT11**, una **placa ESP32**, y un **sistema operativo con un agente de inteligencia artificial** que recibe y almacena los datos.

---

## 📦 Estructura del Servicio

El sistema está compuesto por varios componentes que trabajan en conjunto:

### 1. **Entrada: Sensor DHT11**
- El sensor **DHT11** mide la **temperatura** y la **humedad relativa** del ambiente.
- Está conectado a la **ESP32** y se consulta periódicamente.

### 2. **Microcontrolador: ESP32**
- La ESP32 lee los datos del sensor y los envía al ordenador mediante **protocolo UART** a través del **puerto USB**.
- Utiliza comunicación serie (Serial) para transmitir los valores de temperatura y humedad.

### 3. **Sistema Operativo (PC)**
- El ordenador recibe los datos por el puerto **COM** correspondiente.
- Un script local en Python u otro lenguaje lee el puerto y **guarda los datos en un archivo `.txt`**.

### 4. **Agente de Inteligencia Artificial**
- Los datos almacenados son procesados o utilizados por un **agente local de IA**.
- Este agente puede analizar tendencias, responder a preguntas del usuario, o activar funciones automatizadas.

---

## 🔁 Flujo de Datos

```
DHT11 → ESP32 → Sistema Operativo (PC) → Agente de Inteligencia Artificial
```

---

## 🧪 Ejemplo de Uso

1. Conectar el sensor DHT11 a la ESP32.
2. Subir un firmware que lea el DHT11 y envíe los datos por `Serial.print`.
3. En el PC, ejecutar un script que:
    - Detecte el puerto COM.
    - Lea los datos continuamente.
    - Almacene la información en un archivo `datos.txt`.
4. El asistente inteligente puede:
    - Leer el archivo.
    - Responder preguntas como: “¿Cuál fue la última temperatura registrada?”
    - Detectar si hay condiciones anómalas de humedad o temperatura.

---

## 🛠 Requisitos

- Placa ESP32
- Sensor DHT11
- Cable micro USB
- Script lector en PC (Python recomendado)
- Agente de IA local (modelo compatible, como Phi, LLaMA o GPT)

---

## 📁 Archivos Generados

- `datos.txt`: archivo que almacena las lecturas en el PC.
- `firmware.ino`: sketch de Arduino para la ESP32 (no incluido en este repositorio).
- `lector_serial.py`: script lector del puerto serie (opcional, puede ser personalizado).

---

## 🚀 Expansiones Futuras

- Almacenamiento en base de datos en lugar de `.txt`
- Visualización de datos en tiempo real (gráficas)
- Envío a servicios en la nube o dashboard web
- Conexión con otros sensores y actuadores

---

Este sistema es modular, eficiente y se puede adaptar a múltiples escenarios de automatización y monitoreo inteligente.
