# https://flask.palletsprojects.com/en/2.1.x/quickstart/#a-minimal-application
# https://flask.palletsprojects.com/en/2.1.x/quickstart/#routing
from flask import Flask, render_template
from markupsafe import escape 
from flask_socketio import SocketIO, emit, send
import json
import threading
import time
import toolkit
import os

# Web server
app = Flask(__name__)

# SocketIO server
socketio = SocketIO(app)

def get_userdata():
    file = open('userdata.json')
    userdata = json.load(file)
    file.close()

    return userdata

@app.route("/")
def index():
    return render_template('index.html', userdata=get_userdata())

@app.route("/server/<int:server_index>")
def server(server_index):
    userdata = get_userdata()

    if server_index > len(userdata["servers"]) - 1:
        return escape("Server not found | id out of range")

    server = userdata["servers"][server_index]
    
    return render_template('server.html', server=server)

@socketio.on('connect', namespace='/logs')
def socket_connect():
    send(("lastlogs", toolkit.get_latest_logs(0)))

# TODO: Shown log should match their server index
# Currently, it's showing log only for server_index 0. (Hardcoded)
# Change server_index to server index from URL ( e.g. /server/1 <-- )
def send_new_logline(server_index):
    while True:
        logcount = toolkit.get_loglines_count(server_index)
        toolkit.wait_new_logline(0)

        loglines = toolkit.get_latest_logs(server_index, limit=(toolkit.get_loglines_count(server_index) - logcount))
        with app.test_request_context("/logs"):
            socketio.send(("lastlogs", loglines), namespace="/logs")

onLogFileChangeThread = threading.Thread(target=send_new_logline, args=[0])
onLogFileChangeThread.start()
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)