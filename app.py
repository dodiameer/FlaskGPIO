from flask import Flask, render_template, jsonify
import RPi.GPIO as GPIO
import board
import adafruit_dht
import time
app = Flask(__name__)
# Setting up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
dht = adafruit_dht.DHT11(board.D4)

def genericToggle(pin):
    try:
        GPIO.output(pin, not GPIO.input(pin))
        return True
    except:
        return False

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
    done = genericToggle(pin)
    return jsonify({"done": done})

@app.route('/temperature')
def temperatureHandler():
    tempData = getTemperature()
    return jsonify(tempData)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
