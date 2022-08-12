import rcon
import json
import time
from file_read_backwards import FileReadBackwards

# USERDATA FUNCTIONS
def get_userdata():
    file = open('userdata.json')
    userdata = json.load(file)
    file.close()

    return userdata

# CONSTANTS
CONFIG = get_userdata()["configuration"]
LOG_READ_LIMIT = CONFIG["log-read-limit"]
LOG_COUNT_WAIT = CONFIG["log-count-wait"]

def get_server_path(server_index):
    servers = get_userdata()["servers"]
    path = servers[server_index]["path"]
    if path == "default":
        path = "servers/" + servers[server_index]["servername"]

    return path

# RCON SETUP / FUNCTIONS
rcon_host = "127.0.0.1"
rcon_port = 25575
rcon_password = "1234567890"

def set_rcon(host, port, password):
    rcon_host = host
    rcon_port = port
    rcon_password = password

def run_command(*args):
    with rcon.Client(rcon_host, rcon_port, passwd=rcon_password) as client:
        client.run(args)

# GET LOGS FUNCTIONS
def get_latest_logs(server_index, limit=LOG_READ_LIMIT):
    logs = []

    path = get_server_path(server_index)
    
    with FileReadBackwards(path + "/logs/latest.log", encoding="utf-8") as file:
        index = 0
        for line in file:
            if index >= limit:
                break
            logs.append(line)
            index += 1

    return logs[::-1]

def get_loglines_count(server_index):
    file = open(get_server_path(server_index) + "/logs/latest.log")
    line_count = 0
    buffer_size = 1024 * 1024
    read_file = file.read

    buffer = read_file(buffer_size)
    while buffer:
        line_count += buffer.count("\n")
        buffer = read_file(buffer_size)
    
    return line_count

def wait_new_logline(server_index):
    line_count = get_loglines_count(server_index)
    new_line_count = line_count
    while line_count == new_line_count:
        new_line_count = get_loglines_count(server_index)
        time.sleep(LOG_COUNT_WAIT)