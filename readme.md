Estructura del servicio.

En este proyecto el sistema de entrada basado en la ESP32, recogera la lectura de temperatura con DHT11 y por puerto USB protocolo UART,
enviara la informacion y guardara en un archivo .txt del ordenador.

El flujo de datos correra de la siguiente manera:

DHT11 ->  ESP32 -> Sistema Operativo (PC) -> Agente de inteligencia artificial.
