#RP2040
from time import sleep_ms
from machine import I2C, Pin, UART, ADC
from esp8266_i2c_lcd import I2cLcd
import _thread

adc_pin = ADC(26)

DEFAULT_I2C_ADDR = 0x27

h=0
uart = None
led = None
LKUART = _thread.allocate_lock()
LKADC = _thread.allocate_lock()

# Función para configurar, de aquí pasa a configurar el uart en la función
# setupUART
def setup():
    global led, uart
    setupUART()
    led = Pin(25, Pin.OUT)

# Configura el uart, en este caso el UART0
def setupUART():
    global uart
    pin_tx = Pin(0, Pin.OUT)
    pin_rx = Pin(1, Pin.IN)
    uart = UART(0, baudrate=115200, tx=pin_tx, rx=pin_rx, timeout=1, timeout_char=1)

# Envía los datos por tx al ESP32
def send_data(data):
    global uart
    uart.write("{:.1f}".format(float(data)))

# Recibe los datos por rx del ESP32
def receive_data():
    global uart
    data = uart.read(10)  # Máximo 10 caracteres
    return data

def read_adc(arg):
    global h
    sleep_ms(1000)
    while True:
        with LKADC:
            hum_suelo = adc_pin.read_u16()
            sleep_ms(500)
            h = hum_suelo / 65535  # Convertir a porcentaje
            print(f"Humedad suelo: {h}%")
            send_data(str(h))
            

def test_main():
    global h
    print("Running test_main")
    i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
    sleep_ms(3000)
    lcd.clear()
    count = 0
    show_temperature = True
    while True:
        #read_adc(arg)
        received_data = receive_data()  # Lee los datos de rx
        lcd.move_to(0, 0)  # En 0,0 del LCD
        if show_temperature:
            lcd.putstr("Temp: " + str(received_data, 'utf-8') + "C" if received_data else "No data")  # Escribe en LCD
        else:
            lcd.putstr("Hum: " + str(received_data, 'utf-8') + "%" if received_data else "No data")  # Escribe en LCD
        
        lcd.move_to(0, 1)
        lcd.putstr("Suelo: " + str(h) + "%" if h else "No data")  # Escribe en LCD
        
        sleep_ms(1000)
        lcd.clear()
        show_temperature = not show_temperature

_thread.start_new_thread(read_adc, (None,))
setup()
test_main()

