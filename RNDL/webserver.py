from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "test"


@app.route("/get/<string:server>/<string:bridge>/<string:room>")
def getData(server):
    data = [{
        "Server": server,
        "Bridge": bridge,
        "Room": room,
        "Temperature": 44,
        "Humidity": 88,
        "People": 20
    }]

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)


