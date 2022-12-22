from flask import Flask, render_template, request
from commons import loaded_servers, startServer, stopServer, mcserver_subprocesses, sendCommand, returnAPIError, newServer
import atexit

app = Flask(__name__)

@app.before_first_request
def startup():
    # Load servers, setup configs and other commons.
    pass

def shutdown():
    # On flask shutdown, stop all subprocesses.
    # (Not needed, they are automatically terminated)
    pass

@app.route("/")
def index():
    return render_template("index.html", servers=loaded_servers, subprocesses=mcserver_subprocesses)

@app.route("/server/<int:index>")
def server_page(index):
    return render_template("serverpage.html", server=loaded_servers[index])

@app.route("/new-server")
def new_server_page():
    return render_template("newserver.html")

# Servers API
# /api/server/<int:index>/<start|stop>
@app.route("/api/server/<int:index>/start", methods=["POST"])
def api_startServer(index):
    success = startServer(index)
    return {"result": success}

@app.route("/api/server/<int:index>/stop", methods=["POST"])
def api_stopServer(index):
    success = stopServer(index)
    return {"result": success}

# /api/server/<int:index>/command
# POST Data: {"command": <string:command>}
@app.route("/api/server/<int:index>/command", methods=["POST"])
def api_sendCommand(index):
    # Check if required post data exists.
    if not "command" in request.form: return returnAPIError("command not specified")
    
    # Send command to server.
    success = sendCommand(index, request.form["command"])

    # Return error if server doesn't exist.
    if success == False: return returnAPIError("server not found")

    return {"result": True}

# /api/server/new
# POST Data: {"name": "mcserver", "software": "paper", "version": "1.19.3", "max-ram": "2G"}
@app.route("/api/server/new", methods=["POST"])
def api_createNewServer():
    # Check if required post data exists.
    if not "name" in request.form: return returnAPIError("name not specified")
    if not "version" in request.form: return returnAPIError("version not specified")
    if not "software" in request.form: return returnAPIError("server software not specified")
    if not "max-ram" in request.form: return returnAPIError("max ram not provided")

    # Try to create a new server.
    success = newServer(name=request.form["name"], max_ram=request.form["max-ram"], software=request.form["software"], version=request.form["version"])
    
    if isinstance(success, tuple):
        return returnAPIError(success[1])

    return {"result": success} 

# Register shutdown() function.
atexit.register(shutdown)

if __name__ == "__main__":
    app.run(port=5000, debug=True)