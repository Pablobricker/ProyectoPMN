# Proyecto Control de invernadero
Proyecto final de la materia de procesadores multinúcleo semestre 2024-1

## Contents:
- `ESP32_GENERIC-20230426-v1.20.0.bin`: se tiene que flashear en el ESP32 como menciona la pagina oficial de microPython.
- `RPI_PICO-20231005-v1.21.0.uf2`: se tiene que flashear al RP2040 simplemente conectandolo con el boton boot presionado y cuando aparezca el unidad extraible guardar el archivo ahí.
- `esp8266_i2c_lcd.py`: Dirver del LCD para que el ESP32 lo maneje con micropython, se guarda en la memoria del ESP32.
- `esp32.py`: Software de control y transmisión de datos del ESP32, se guarda en la memoria del ESP32.
- `rp2040.py`: Software de control y transmisión de datos del RP2040, se guarda en su memoria flash.

## Flash microPython firmware on ESP32:
1. Download firmware
2. - `esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash`
3. - `esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20190125-v1.10.bin`
