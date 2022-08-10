# https://flask.palletsprojects.com/en/2.1.x/quickstart/#a-minimal-application
# https://flask.palletsprojects.com/en/2.1.x/quickstart/#routing
from flask import Flask, render_template
from markupsafe import escape 
from flask_socketio import SocketIO, emit, send
import json
import threading
import time
import toolkit

# NOTE:
# URL Parameters are localhost:5000/hello?url=parameter&this=is
# allowing for the following:

# Web server
app = Flask(__name__)

# SocketIO server
socketio = SocketIO(app)

count = 0
def update_count():
    while True:   
        global count
        count = count + 1
        time.sleep(1)

t = threading.Thread(target=update_count)
t.start()

def get_userdata():
    file = open('userdata.json')
    userdata = json.load(file)
    file.close()

    return userdata

# localhost:5000/
@app.route("/")
def index():
    return render_template('index.html', userdata=get_userdata())

@app.route("/counter")
def counter():
    return f"<p>Current number: {count}</p>"

@app.route("/server/<int:id>")
def server(id):
    userdata = get_userdata()

    if id > len(userdata["servers"]) - 1:
        return escape("Server not found | id out of range")

    server = userdata["servers"][id]
    
    return render_template('server.html', server=server)

# reserved names for events
# message, json, connect and disconnect
# @socketio.on("connect", namespace="/logs")
# def logs_connect():
#     socketio.send("Connected to /logs!", namespace="/logs")

@socketio.on('connect', namespace='/logs')
def socket_connect():
    send(("lastlogs", toolkit.get_latest_logs(0)))


def send_new_logline():
    modified = os.path.getmtime(get_server_path(0))
    while True:

        with app.test_request_context("/logs"):
            socketio.send(("lastlogline", "test"), namespace="/logs")
        time.sleep(1)

if __name__ == "__main__":
    onfilechangeThread = threading.Thread(target=send_new_logline)
    onfilechangeThread.start()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

# localhost:5000/server/0 FLASK URL
# localhost:5000/test SOCKETIO URL
# @socketio.on('connect', namespace='/logs')
# def test_connect():
#     socketio.emit('connect', 'OK! Starting to send logs...', namespace='/logs')

#     time.sleep(1)
    
#     socketio.emit('connect', 'I love python', namespace='/logs')

#     time.sleep(1)

#     socketio.emit('connect', 'mario likes coding', namespace='/logs')

# @socketio.on('getlogs', namespace='/test')
# def test_emit():
#     socketio.emit('getlogs', 'log lines', namespace='/test')