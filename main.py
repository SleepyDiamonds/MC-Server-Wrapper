import time

RCON_HOST = "127.0.0.1"
RCON_PORT = 25575
RCON_PASSWORD = "1234567890"
SERVER_FOLDER = ".\\server\\"

def find_line_at_index(filename, index):
    file = open(filename)
    for i, line in enumerate(file):
        if i == index - 1: 
            return line 
    file.close()

line_index = 1
while True:
    if sum(1 for i in open(SERVER_FOLDER + "\\logs\\latest.log", "rb")) >= line_index:
        print(find_line_at_index(SERVER_FOLDER + "\\logs\\latest.log", line_index))
        line_index = line_index + 1
    elif sum(1 for i in open(SERVER_FOLDER + "\\logs\\latest.log", "rb")) + 1 < line_index:
        line_index = 1
    else: time.sleep(1)
