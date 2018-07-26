from flask import Flask, jsonify, request
from transceiver import *

app = Flask(__name__)


# Server, Bridge, Room: Sensor ADDR
sensors = {
    "1, 1, 1": 5
}

measurements = [{"Address": 5, "Humidity: ": -1, "Temperature": -1}]

trans = Transceiver("COM10")

def get_address(server, bridge, room):
    return sensors[str(server) + ", " + str(bridge) + ", " + str(room)]

def get_latest_measurement(server, bridge, room):
    addr = get_addr(server, bridge, room)
    
    index = 1
    while True:
        current = measurements[-index]
        if current["Address"] == addr:
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
    return str(get_latest_measurement(server, bridge, room)["Temperature"])


# Requests new data from sensor
@app.route('/request/<server>/<bridge>/<room>')
def request_data(server, bridge, room):
    addr = get_address(server, bridge, room)

    temp = trans.request_data(str(addr), "Temperature")
    hum = trans.request_data(str(addr), "Humidity")

    measurements.append({"Address": addr, "Temperature": temp, "Humidity": hum})

    return "Request complete"



    
    
    return "request"

if __name__ == "__main__":
    app.run(debug=True)


