from flask import Flask, render_template, jsonify
import RPi.GPIO as GPIO
import board
import adafruit_dht
import time
import atexit

# FLask instance
app = Flask(__name__)

### Raspi-specific code ###

# Setting up GPIO
GPIO.setmode(GPIO.BCM)
outputPins = [18, 17, 23]
for pin in outputPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Setting up DHT11 sensor (Temperature & Humidity)
dht = adafruit_dht.DHT11(board.D4)

# Exit cleanup code
@atexit.register
def cleanup_exiter():
    time.sleep(1)
    print("\nRunning cleanup before exit")
    GPIO.cleanup()
    print("Cleanup done!\nExiting...")

# Generic pin toggler (No special requirements for toggle)
def genericToggle(pin):
    try:
        GPIO.output(pin, not GPIO.input(pin))
        return {"done": True, "state": GPIO.input(pin)}
    except:
        return {"done": False, "state": GPIO.input(pin)}

# Temperature getter (NO LONGER SPAGHETII CODE!)
def getTemperature():
    try:
        return {"temperature": dht.temperature, "humidity": dht.humidity}
    except RuntimeError:
        getTemperature()

### Flask logic code ###

# Index page
@app.route('/')
def index():
    return render_template('index.html')

# Pin toggle API - genericToggle()
@app.route('/pin/<int:pin>/toggle')
def toggleHandler(pin):
    res = genericToggle(pin)
    return jsonify(res)

# Temperature API - getTemperature()
@app.route('/temperature')
def temperatureHandler():
    tempData = getTemperature()
    return jsonify(tempData)

# Run server if not imported
if __name__ == "__main__":
    app.run(host="0.0.0.0")
