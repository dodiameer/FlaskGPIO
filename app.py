from flask import Flask, render_template, jsonify
import RPi.GPIO as GPIO
import board
import adafruit_dht
import time
import atexit
app = Flask(__name__)
# Setting up GPIO
GPIO.setmode(GPIO.BCM)
outputPins = [18, 17, 23]
for pin in outputPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

dht = adafruit_dht.DHT11(board.D4)

@atexit.register
def cleanup_exiter():
    print("\nRunning cleanup before exit")
    GPIO.cleanup()
    print("Cleanup done!\nExiting...")

def genericToggle(pin):
    try:
        GPIO.output(pin, not GPIO.input(pin))
        return {"done": True, "state": GPIO.input(pin)}
    except:
        return {"done": False, "state": GPIO.input(pin)}

def getTemperature():
    try:
        return {"temperature": dht.temperature, "humidity": dht.humidity}
    except RuntimeError:
        time.sleep(2)
        return {"temperature": dht.temperature, "humidity": dht.humidity}

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/pin/<int:pin>/toggle')
def toggleHandler(pin):
    res = genericToggle(pin)
    return jsonify(res)

@app.route('/temperature')
def temperatureHandler():
    tempData = getTemperature()
    return jsonify(tempData)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
