# Sensor de Temperatura y Humedad DHT11

El **DHT11** es un sensor digital básico, económico y ampliamente utilizado para medir la **temperatura** y la **humedad relativa** del ambiente. Es ideal para proyectos de electrónica, estaciones meteorológicas, domótica e IoT por su facilidad de uso y bajo consumo energético.

---

## Características Técnicas

| Parámetro              | Especificación                 |
|------------------------|-------------------------------|
| Tipo de salida         | Digital (señal serial 1 cable) |
| Rango de temperatura   | 0 – 50 °C                      |
| Precisión temperatura  | ±2 °C                          |
| Rango de humedad       | 20% – 90% RH                   |
| Precisión humedad      | ±5% RH                         |
| Voltaje de operación   | 3.3V – 5.5V                    |
| Frecuencia de muestreo | 1 lectura por segundo (1 Hz)   |
| Dimensiones            | ~15.5 mm x 12 mm x 5.5 mm      |

---

## Funcionamiento

El DHT11 contiene los siguientes componentes:

- Un **sensor capacitivo de humedad**.
- Un **termistor** para medir la temperatura.
- Un **chip integrado** que digitaliza las señales y las entrega por un único pin de datos.

Cuando se solicita una lectura, el sensor responde con una secuencia de bits codificados que representan la temperatura y la humedad. Esta información es interpretada fácilmente mediante librerías como la de **Adafruit** o la propia `DHT.h` en **Arduino/ESP32**.

---

## Conexiones Típicas (ESP32 / Arduino)

| Pin del DHT11 | Conexión típica        |
|---------------|------------------------|
| VCC           | 3.3V o 5V              |
| DATA          | Pin digital (ej. GPIO33) |
| GND           | GND                    |

> **Nota**: A menudo se utiliza una resistencia de **pull-up** de entre **4.7kΩ** y **10kΩ** entre los pines **VCC** y **DATA** para mejorar la estabilidad de la señal.

---

## Aplicaciones Comunes

- Estaciones meteorológicas.
- Control de ventilación o climatización.
- Monitoreo ambiental en interiores.
- Sistemas inteligentes para agricultura.
- Automatización del hogar.

---

## Limitaciones

- No adecuado para alta precisión.
- Solo permite una lectura por segundo.
- Intervalos de operación limitados (temperatura y humedad).

---

## Esquema de Conexión

Informacion en la pagina web infootec.net:
https://www.infootec.net/dht11-sensor/
