from flask import Flask, render_template
from commons import loaded_servers, startServer, stopServer, loadServers

app = Flask(__name__)

@app.before_first_request
def startup():
    # Load servers, setup configs and other commons.
    global loaded_servers
    loaded_servers = loadServers()

@app.route("/")
def index():
    return render_template("index.html", servers=loaded_servers)

@app.route("/server/<int:index>")
def server_page(index):
    return render_template("serverpage.html", index=index)


# Servers API
# /api/server/<int:index>/<start|stop>
@app.route("/api/server/<int:index>/start", methods=["POST"])
def startServer(index):
    success = startServer(index)

@app.route("/api/server/<int:index>/stop", methods=["POST"])
def stopServer(index):
    success = stopServer(index)

if __name__ == "__main__":
    app.run(port=5000, debug=True)