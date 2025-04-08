import serial
import time

# Configura el puerto COM correspondiente y la velocidad de transmisión (baudrate)
PUERTO_SERIAL = 'COM5'  # Cambia según tu puerto COM
BAUDRATE = 9600

# Intenta abrir el puerto serial
try:
    esp32 = serial.Serial(PUERTO_SERIAL, BAUDRATE, timeout=1)
    print(f"Conectado a {PUERTO_SERIAL} a {BAUDRATE} baudios.")
except serial.SerialException as e:
    print(f"Error al conectar con el puerto serial: {e}")
    exit()

# Bucle para leer y guardar datos cada 20 segundos
with open("datos.txt", "a", encoding="utf-8") as archivo:
    try:
        while True:
            if esp32.in_waiting > 0:
                dato = esp32.readline().decode('utf-8').strip()
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                archivo.write(f"{timestamp} - {dato}\n")
                archivo.flush()
                print(f"Guardado: {dato}")
            time.sleep(20)
    except KeyboardInterrupt:
        print("Lectura detenida por usuario.")
    finally:
        esp32.close()
