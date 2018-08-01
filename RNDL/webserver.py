from flask import Flask, jsonify, request
from transceiver import *
from threading import *
import json
import datetime


app = Flask(__name__)

# Server, Bridge, Room: Sensor ADDR
sensors = {
    "1, 1, 1": 5,
    "1, 2, 1": 1
}

measurements = [{"address": 5, "humidity": -42, "temperature": -88, "time": 420}, {"address": 1, "humidity": -44, "temperature": -2311, "time": 534}]

trans = Transceiver("COM9") 

def get_address(server, bridge, room):
    return sensors[str(server) + ", " + str(bridge) + ", " + str(room)]

def get_latest_measurement(server, bridge, room):
    addr = get_address(server, bridge, room)
    
    index = 1
    while True:
        current = measurements[-index]
        if current["address"] == addr:
            return current
            
        if index > len(measurements):
            return None
        index = index + 1

@app.route('/')
def index():
    return "test"

# Returns the latest data
@app.route('/get/<server>/<bridge>/<room>')
def get_data(server, bridge, room):
    return str(get_latest_measurement_json(server, bridge, room))

def get_latest_measurement_json(server, bridge, room):
    d = get_latest_measurement(server, bridge, room)
    js = json.dumps(d)
    return js

# Requests new data from sensor
@app.route('/request/<server>/<bridge>/<room>')
def request_data(server, bridge, room):
    addr = get_address(server, bridge, room)
    print("requesting temperature")
    temp = trans.request_data(str(addr), "temperature")
    print("requesting humidity")
    hum = trans.request_data(str(addr), "humidity")

    print("requesting time")
    time = trans.request_data(str(addr), "time") 

    measurements.append({"address": addr, "temperature": temp, "humidity": hum, "systemtime": time, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    print(temp)

    return str(get_latest_measurement_json(server, bridge, room))


@app.route('/getraw/<server>/<bridge>/<room>')
def request_raw_data(server, bridge, room):
    dic = get_latest_measurement(server, bridge, room)
    #try:
    temp = dic['temperature']
    hum = dic['humidity']
    time = dic['time']
    addr = dic['address']
    #except KeyError:
    #    return "keyerror"

    reply = str(temp) + "\n" + str(hum) + "\n" + str(time) + "\n" + str(addr)

    return reply

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

