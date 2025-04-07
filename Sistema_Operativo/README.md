# Detección de Puerto COM de la ESP32 en Windows

Cuando conectas tu placa **ESP32** a tu ordenador con Windows mediante USB, es necesario identificar en qué **puerto COM** se encuentra conectada para poder programarla o monitorear su salida.

A continuación, se describen varios métodos para detectar el puerto COM desde la línea de comandos (CMD).

---

## Método 1: Usar el comando `mode`

```cmd
mode
```

Este comando lista todos los **puertos COM disponibles** junto con su configuración actual. Verás salidas como:

```
Status for device COM3:
-----------------------
    Baud:            9600
    Parity:          None
    Data Bits:       8
    Stop Bits:       1
    ...
```

---

## Método 2: Usar `wmic` para obtener nombres descriptivos

```cmd
wmic path Win32_SerialPort get DeviceID,Name,Description
```

Este comando muestra detalles útiles como el nombre del adaptador USB:

```
DeviceID  Name                            Description
COM4      USB-SERIAL CH340 (COM4)         USB-SERIAL CH340
```

Busca el nombre relacionado con tu chip USB a UART. Algunos ejemplos comunes:

- **CP210x USB to UART Bridge** → Para chips CP2102
- **USB-SERIAL CH340** → Para chips CH340
- **Silicon Labs** → Para CP210x

---

## Método 3: Usar PowerShell

También puedes obtener la lista desde PowerShell ejecutado desde CMD:

```cmd
powershell "Get-WmiObject Win32_SerialPort | Select-Object Name, DeviceID"
```

Esto te mostrará un listado similar al anterior con el nombre y el puerto COM.

---

## Método 4: Listar dispositivos USB conectados

```cmd
pnputil /enum-devices /connected
```

Este comando te permite ver todos los dispositivos USB actualmente conectados, incluido el adaptador serial de la ESP32.

---

## Consejos útiles

- Conecta la ESP32 y ejecuta los comandos: busca el **nuevo puerto COM** que aparece.
- Si desconectas la placa y vuelves a ejecutar el comando, el COM que desaparece es el de la ESP32.
- Si tienes varios puertos COM, prueba desconectar y reconectar para identificar el correcto fácilmente.

---

## Automatización (opcional)

Puedes crear un archivo `.bat` con los comandos `wmic` o `mode` para ejecutarlo cada vez que necesites verificar rápidamente el puerto de la ESP32.

```bat
@echo off
wmic path Win32_SerialPort get DeviceID,Name,Description
pause
```

Guarda el archivo como `ver_com_esp32.bat` y ejecútalo con doble clic.
