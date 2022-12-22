from libs.mcserver import MCServer
from libs.mcserversubprocess import MCServerSubprocess
import json
import os
import subprocess

FILE_SERVERS_LOCATION = "servers.json"
FILE_CONFIG_LOCATION = "config.json"


JVM_STARTUP_FLAGS = "java -Xms%s -Xmx%s -XX:+UseG1GC -jar server.jar nogui" 
mcserver_subprocesses = []

def loadServers():
    """
    Loads the `servers.json`, and returns the contents of it. (List of servers)
    """
    servers = []

    with open(FILE_SERVERS_LOCATION) as file:
        json_object = json.load(file)
        for index, server in enumerate(json_object["servers"]):
            servers.append(MCServer(index=index, name=server["server_name"], ip_addr=server["hostname"], port=server["port"] ,rcon_port=server["rcon_port"], rcon_passwd=server["rcon_password"], max_ram=server["max_ram"]))
    
    return servers

loaded_servers = loadServers()

def getServerExecutablePath(index):
    """
    Returns server executable path, for example: `servers/devserver/server.jar`
    """
    return "server/" + loaded_servers[index].name + "/server.jar"
    
def startServer(index):
    """
    Starts the server according to the index provided.
    Returns `True` or `False`, depending if any errors occured.
    """
    try:
        server_name = loaded_servers[index].name
        server_ram = loaded_servers[index].max_ram
        
        # Starts the server with provided Maximum RAM from the config
        # cd servers/mcserver
        # java -jar server.jar 

        cwd = os.getcwd()
        os.chdir(f"servers/{server_name}")

        server_subprocess = subprocess.Popen(JVM_STARTUP_FLAGS % (server_ram, server_ram), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        
        mcserver_subprocesses.append(MCServerSubprocess(server_index=index, subprocess=server_subprocess))

        # Go back to the main directory
        os.chdir(cwd)

        # Return True because server has started successfully.
        return True

    except Exception as e:
        # Return False because error occured.
        return False

def getMCServerSubprocess(index):
    """
    Returns `MCServerSubprocess` based on server index.
    If server is not running and subprocess doesn't exist,
    it will return `None`.
    """
    for mcserver_subprocess in mcserver_subprocesses:
        if mcserver_subprocess.server_index == index:
            # Server is found, return it.
            return mcserver_subprocess
    
    # Server is not found, return None.
    return None

def sendCommand(index, command):
    """
    Send command to minecraft server.
    Returns False if server's subprocess has not been found, otherwise
    it returns True.
    """
    mcserver_subprocess = getMCServerSubprocess(index)

    # Return False if server subprocess was not found.
    if mcserver_subprocess == None: return False

    # Write to subprocess' stdin.
    mcserver_subprocess.stdin_write(command)
    return True

def stopServer(index):
    """
    Stops the server according to the index provided.
    Returns `True` or `False`, depending if any errors occured.
    """
    mcserver_subprocess = getMCServerSubprocess(index)

    # Return False if server subprocess was not found.
    if mcserver_subprocess == None: return False

    mcserver_subprocess.terminate()

    # Remove it from mcserver_subprocesses list.
    mcserver_subprocesses.remove(mcserver_subprocess)
    
    # Return True because server has stopped successfully
    return True

def stopAllServers():
    """
    Stops all servers.
    """
    for mcserver_subprocess in mcserver_subprocesses:
        mcserver_subprocess.terminate()

def returnAPIError(description=None):
    """
    Returns API Error Dictionary:
    `{"result": False, "error": description}`
    """
    if description == None: return {"result": False}
    return {"result": False, "error": description}