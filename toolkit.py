from xml.dom import UserDataHandler
import rcon
import json
from file_read_backwards import FileReadBackwards


# file = open('userdata.json')
# userdata = json.load(file)
# file.close()

def get_userdata():
    file = open('userdata.json')
    userdata = json.load(file)
    file.close()

    return userdata

# CONSTANTS
CONFIG = get_userdata()["configuration"]
LOG_READ_LIMIT = CONFIG["log-read-limit"]

# USERDATA FUNCTIONS
def get_server_path(server_index):
    servers = get_userdata()["servers"]
    path = servers[server_index]["path"]
    if path == "default":
        path = servers[server_index]["servername"]

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
    with rcon.Client(RCON_HOST, RCON_PORT, passwd=RCON_PASSWORD) as client:
        client.run(args)

# GET LOGS FUNCTIONS
def get_latest_logs(server_index, limit=LOG_READ_LIMIT):
    logs = []

    path = get_server_path(server_index)
    
    with FileReadBackwards("servers/" + path + "/logs/latest.log", encoding="utf-8") as file:
        index = 0
        for line in file:
            if index >= limit:
                break
            logs.append(line)
            index += 1

    return logs[::-1]

############
# OLD CODE #
############

# def find_line_at_index(filename, index):
#     file = open(filename)
#     for i, line in enumerate(file):
#         if i == index - 1: 
#             return line 
#     file.close()
# while True: 
    #     if sum(1 for i in open(SERVER_FOLDER + "\\logs\\latest.log", "rb")) >= line_index:
    #         print(find_line_at_index(SERVER_FOLDER + "\\logs\\latest.log", line_index))
    #         line_index = line_index + 1
    #     elif sum(1 for i in open(SERVER_FOLDER + "\\logs\\latest.log", "rb")) + 1 < line_index:
    #         line_index = 1

    # index = 0
    # a = "Hello World!\r\nThis is a new line\r\nalso new line\r\n"
    # for logline in open("servers/"+ path + "/logs/latest.log", "r"):
    #     index -= 1

    #     logs.append(logline[index])
    
    # with open("servers/" + path + "/logs