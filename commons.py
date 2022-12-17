from minecraftserver import MinecraftServer
import json
import os

FILE_SERVERS_LOCATION = "servers.json"
FILE_CONFIG_LOCATION = "config.json"

loaded_servers = []

def loadServers():
    """
    Loads the servers.json, and returns the contents of it. (List of servers)
    """
    servers = []

    with open(FILE_SERVERS_LOCATION) as file:
        json_object = json.load(file)
        for index, server in enumerate(json_object["servers"]):
            servers.append(MinecraftServer(index=index, name=server["server_name"], ip_addr=server["hostname"], port=server["port"] ,rcon_port=server["rcon_port"], rcon_passwd=server["rcon_password"]))
    
    return servers

# returns servers/slepysmp/server.jar
def getServerExecutablePath(index):
    """
    Returns server executable path, for example: 'servers/devserver/server.jar'
    """
    return loaded_servers[index]["server_name"] + "/server.jar"
    
def startServer(index):
    serverInstance = os.popen("java")

def stopServer(index):
    pass