# Proyecto Control de invernadero
Proyecto final de la materia de procesadores multinúcleo semestre 2024-1
## Contents:
-`ESP32_GENERIC-20230426-v1.20.0.bin` se tiene que flashear en el ESP32 como dice el video: https://www.youtube.com/watch?v=RLqPB1PM6gE&list=PLtZQ6WyfEW8MqUpt2VmDr5FuJe3CiV7bA
-`RPI_PICO-20231005-v1.21.0.uf2` se tiene que flashear al RP2040 simplemente conectandolo con el boton boot presionado y cuando aparezca el unidad extraible guardar el archivo ahí.
-`esp8266_i2c_lcd.py` Dirver del LCD para que el ESP32 lo maneje con micropython, se guarda en la memoria del ESP32
-`esp32.py` Software de control y transmisión de datos del ESP32, se guarda en la memoria del ESP32
-`rp2040.py` Software de control y transmisión de datos del RP2040, se guarda en su memoria flash
