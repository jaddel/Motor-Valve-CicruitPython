# Adafruit CircuitPython 7.3.2 on 2022-07-20; Challenger NB RP2040 WiFi with rp2040
# References:
# - https://cdn-learn.adafruit.com/downloads/pdf/adding-a-wifi-co-processor-to-circuitpython-esp8266-esp32.pdf
import time
import board
import busio
from digitalio import DigitalInOut, Direction
from adafruit_espatcontrol import adafruit_espatcontrol
# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
# Debug Level
# Change the Debug Flag if you have issues with AT commands
print(board.board_id)
debugflag = False

# Wifi settings for challenger_nb_rp2040_wifi
RX = board.ESP_RX
TX = board.ESP_TX
resetpin = DigitalInOut(board.WIFI_RESET)
rtspin = False
uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048)
esp_boot = DigitalInOut(board.WIFI_MODE)
esp_boot.direction = Direction.OUTPUT
esp_boot.value = True
status_light = None

print("ESP AT commands")

esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag)

print("Resetting ESP module")
esp.hard_reset()
first_pass = True
while True:
    try:
        if first_pass:
            # Some ESP do not return OK on AP Scan.
            # See https://github.com/adafruit/Adafruit_CircuitPython_ESP_ATcontrol/issues/48
            # Comment out the next 3 lines if you get a No OK response to AT+CWLAP
            #print("Scanning for AP's")
            #for ap in esp.scan_APs():
            #    print(ap)
            print("Checking connection...")
            # secrets dictionary must contain 'ssid' and 'password' at a minimum
            print("Connecting...")
            esp.connect(secrets)
            print("Connected to AT software version ", esp.version)
            print("IP address ", esp.local_ip)
            first_pass = False
        print("Pinging 8.8.8.8...", end="")
        print(esp.ping("8.8.8.8"))
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue
