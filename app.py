from flask import Flask, render_template, request
from commons import loaded_servers, startServer, stopServer, mcserver_subprocesses, sendCommand, returnAPIError, newServer, deleteServer, getServerSettings, changeServerSettings
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
# POST /api/server/<int:index>/<start|stop>
@app.route("/api/server/<int:index>/start", methods=["POST"])
def api_startServer(index):
    success = startServer(index)
    return {"result": success}

@app.route("/api/server/<int:index>/stop", methods=["POST"])
def api_stopServer(index):
    success = stopServer(index)
    return {"result": success}

# POST /api/server/<int:index>/command
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

# POST /api/server/new
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

# POST /api/server/<int:index>/delete
@app.route("/api/server/<int:index>/delete", methods=["POST"])
def api_deleteServer(index):
    success = deleteServer(index)
    return {"result": success}

# API for returning the server.properties in a dictonary
@app.route("/api/server/<int:index>/getSettings", methods=["POST"])
def api_getServerSettings(index):
    response = getServerSettings(index)
    return response

# Loads the server settings panel
@app.route("/server/<int:index>/settings")
def showServerSettings(index):
    server_properties = getServerSettings(index)
    return render_template("serversettings.html", index=index, server=loaded_servers, server_properties=server_properties)

# Changes the server.properties file
@app.route("/api/server/<int:index>/changeSettings", methods=["POST"])
def api_changeServerSettings(index):
    success = changeServerSettings(index, request.form.to_dict())
    return {"result":success}

# Register shutdown() function.
atexit.register(shutdown)

if __name__ == "__main__":
    app.run(port=5000, debug=True)