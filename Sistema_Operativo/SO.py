def leer_esp32(puerto="COM3", baudrate=115200):
    with serial.Serial(puerto, baudrate, timeout=1) as ser:
        while True:
            if ser.in_waiting:
                linea = ser.readline().decode("utf-8").strip()
                print(f"Dato recibido: {linea}")
                
                with open("datos_esp32.txt", "a") as archivo:
                    archivo.write(linea + "\n")
