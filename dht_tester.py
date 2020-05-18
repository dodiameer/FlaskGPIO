import board
import adafruit_dht
import time

dhtDevice = adafruit_dht.DHT11(board.D4)

while True:
    try:
        tc = dhtDevice.temperature
        print(f'Temperature: {tc}C')
    except RuntimeError:
        pass
    time.sleep(2.0)