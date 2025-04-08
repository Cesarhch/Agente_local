#include <Arduino.h>
#include <DHT.h>

// Configuración del sensor DHT
#define DHTPIN 33
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);

  dht.begin();
  Serial.println("Sensor DHT inicializado.");
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("Error al leer el sensor DHT");
  } else {
    Serial.print("Temperatura: ");
    Serial.print(temp);
    Serial.print(" °C\tHumedad: ");
    Serial.print(hum);
    Serial.println(" %");
  }

  delay(2000);  // Espera antes de la siguiente lectura
}
