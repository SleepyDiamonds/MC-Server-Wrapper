from flask import Flask, render_template
from commons import loaded_servers, startServer, stopServer, mcserver_subprocesses
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

# Register shutdown() function.
atexit.register(shutdown)

if __name__ == "__main__":
    app.run(port=5000, debug=True)