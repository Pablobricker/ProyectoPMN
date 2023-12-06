#ESP32 ENVIANDO AMBOS DATOS
#ESP32
import os
import machine
import utime
import _thread
import dht
from machine import Pin

bomba=Pin(22,Pin.OUT)
foco=Pin(23,Pin.OUT)
ventilador=Pin(21,Pin.OUT)
sensor=dht.DHT11(Pin(4))
humedad=0
temperatura=0
line=0

UART = None
LKUART = _thread.allocate_lock()
LKSENSOR=_thread.allocate_lock()
LKTEMP = _thread.allocate_lock()
LKHUM = _thread.allocate_lock()
LKSUELO = _thread.allocate_lock()
LKDATOS = _thread.allocate_lock()

def setup():
    global UART
    setupUART()

def setupUART():
    global UART
    pin_tx = machine.Pin(17, machine.Pin.OUT)
    pin_rx = machine.Pin(16, machine.Pin.IN)
    UART = machine.UART(2, baudrate=115200, tx=17, rx=16, timeout=1, timeout_char=1)

def send_data(data):
    global UART
    #with LKUART:  
    UART.write(data)
        #print(data)

def Leer_UART(arg):
    global line
    while True:
        utime.sleep(1)
        #with LKUART:  # Usar el candado correcto
        line_bytes = UART.readline()
        if not line_bytes:
            continue
        line = line_bytes.decode('utf-8').strip()
        line_parts=line.split('.')
        if len(line_parts) >= 2:
            line = f"{line_parts[0]}.{line_parts[1]}"
        #print(line)
 
def leer_temperatura(arg):
    global temperatura
    sensor.measure()
    temperatura = sensor.temperature()
    send_data(str(temperatura))
    #print(f"Temperatura: {temperatura}")
    utime.sleep(0.8)
        
def leer_humedad(arg):
    global humedad
    utime.sleep(2)
    humedad=sensor.humidity()
    send_data(str(humedad))
           # print(f"Humedad: {humedad}")
    utime.sleep(0.8)
            
            
def act_bomba(arg): ##AQUÍ VA EN FUNCIÓN DE HUMEDAD DEL SUELO, ME FALTA ESO
    global humedad
    global line
    utime.sleep(2)
    if int(humedad)<50:
        bomba.value(1)
    else:
        bomba.value(0)
    print(f"Humedad: {humedad}%")
    utime.sleep(1)
    print(f"Humedad de suelo: {line}%")
            
def act_foco_vent(arg):
    global temperatura
    utime.sleep(2)
    utime.sleep(1)
    print(f"Temperatura: {temperatura}")
    if temperatura<10:
        foco.value(1)
        ventilador.value(0)
    elif temperatura>20:
        ventilador.value(1)
        foco.value(0)
                
_thread.start_new_thread(Leer_UART, (None,)) #Hilo siempre leyendo UART
_thread.start_new_thread(leer_temperatura, (None,)) #Hilo siempre leyendo sensores
_thread.start_new_thread(leer_humedad, (None,)) #Hilo siempre leyendo sensores
_thread.start_new_thread(act_bomba, (None,)) #Hilo siempre IMPRIMIENDO sensores
_thread.start_new_thread(act_foco_vent, (None,)) #Hilo siempre IMPRIMIENDO sensores
