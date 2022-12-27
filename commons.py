from libs.mcserver import MCServer
from libs.mcserversubprocess import MCServerSubprocess
import json
import os
import shutil
import subprocess
import requests

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
            servers.append(MCServer(index=index, name=server["server_name"], max_ram=server["max_ram"]))
    
    return servers

loaded_servers = loadServers()

def refreshLoadedServers():
    """
    Refreshes all commonly used variables. (`loaded_servers`)
    Required after big changes, like modifying `config.json` or `servers.json`.
    """
    global loaded_servers
    loaded_servers = loadServers()

def getServerExecutablePath(index):
    """
    Returns server executable path, for example: `servers/devserver/server.jar`
    """
    return "server/" + loaded_servers[index].name + "/server.jar"

def getServerByIndex(index):
    """
    Returns server object from index.
    (looks up in `loaded_servers` for `MCServer` object at `index`)
    """
    return loaded_servers[index]

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
        
        mcserver_subprocesses.append(MCServerSubprocess(server=loaded_servers[index], subprocess=server_subprocess))

        # Go back to the main directory
        os.chdir(cwd)

        # Return True because server has started successfully.
        return True
    except:
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
    Returns `False` if server's subprocess has not been found, otherwise
    it returns `True`.
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

def newServer(name, version, software, max_ram):
    """
    Creates a new server.
    Returns `True` if new server has been successfully created.
    Otherwise, returns a tuple with `False` and error description.
    """
    if software == "paper":
        # Get the latest release for the selected version
        builds = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{version}")
        
        if builds.status_code == 400:
            return (False, "bad request")

        builds = builds.json()

        if "error" in builds: return (False, "version not found")

        latest_build = builds["builds"][-1]

        # Download the latest release of the version selected
        response = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{latest_build}/downloads/paper-{version}-{latest_build}.jar")
        
        if response.status_code == 400:
            return (False, "bad request")
        
        if "error" in response: return (False, "version not found")

        cwd = os.getcwd()

        try:
            os.mkdir(f"servers/{name}")
            os.chdir(f"servers/{name}")
        except:
            return (False, "couldn't create/switch to the server directory")
        
        open("server.jar", "wb").write(response.content)

        # Open server.jar file to setup server.
        server_subprocess = subprocess.Popen(JVM_STARTUP_FLAGS % (max_ram, max_ram), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        server_subprocess.wait()

        # Set eula to true now.
        try:
            eula_file = open("eula.txt", "r")
            eula_content = eula_file.read()
            eula_file.close()

            eula_content = eula_content.replace("eula=false", "eula=true")

            # Opening file with "w" mode truncates it
            # automatically.
            eula_file = open("eula.txt", "w")
            eula_file.write(eula_content)
            eula_file.close()
        except:
            return (False, "couldn't find eula.txt file")

        os.chdir(cwd)

        # Adds the server to the servers.json folder
        new_data = {"server_name": name, "max_ram": max_ram}

        # Add server to servers.json file.
        try:
            with open('servers.json', "r+") as file:
                servers = json.load(file)
                servers["servers"].append(new_data)

                file.seek(0)

                json.dump(servers, file, indent=4)
        except:
            return (False, "couldn't write to servers.json")
        
        # Refresh loaded_servers.
        refreshLoadedServers()

        return True
    else:
        return False

def deleteServer(index):
    """
    Deletes a server.
    Returns `True` if server has been successfully deleted,
    otherwise `False`.
    """
    try:
        server_name = loaded_servers[index].name

        # Remove server's folder and its contents.
        shutil.rmtree(f"servers/{server_name}")

        # Remove server from servers.json
        with open('servers.json', "r+") as file:
            servers = json.load(file)
            servers["servers"].pop(index)

            # Resets server.json file.
            file.seek(0)
            file.truncate()

            # Writes to server.json file, with
            # specified server excluded.
            json.dump(servers, file, indent=4)

        # Refresh loaded_servers.
        refreshLoadedServers()

        return True
    except:
        return False

def getServerSettings(index):
    """
    Loads the server.properties file from the request server and returns it in a dictonary.
    """
    try:
        properties_file = open(f"servers/{loaded_servers[index].name}/server.properties").readlines()
    except:
        return (False, "server not found")

    settingsList = []

    for item in properties_file:
        if item[0] == "#":
            continue
        else:
            settingsList.append(item)

    server_properties = {}

    for item in settingsList:
        server_property = item.split("=")
        if server_property[0] == "\n":
            continue

        # Removes \n in the lines
        server_property[1] = server_property[1].rstrip()

        # "True" has to be converted to True (same for false),
        # because the settings page on the client accepts only lowercase true & false
        # if server_property[1] == "true":
        #     server_property[1] = True
        # elif server_property[1] == "false":
        #     server_property[1] = False

        server_properties[server_property[0]] = server_property[1]

    return server_properties

def changeServerSettings(index, settings):
    """
    Changes the server.properties file of the index server
    """
    newSettings = {}
    with open(f"servers/{loaded_servers[index].name}/server.properties", "w") as file:
        final_string = ""

        # True or "True" have to be converted to "true" (same for false)
        # because Java only accepts lovercase true & false
        for item in settings.keys():
            if settings[item] == True:
                newSettings[item] = "true"
            if settings[item] == False:
                newSettings[item] = "false"
            else:
                newSettings[item] = settings[item]

            # Add everything to the final string
            # that will be written to the file
            final_string = final_string + item + "=" + newSettings[item] + "\n"
        
        # Write to the file and return
        file.write(final_string)
        return True

def returnAPIError(description=None):
    """
    Returns API Error Dictionary:
    `{"result": False, "error": description}`
    """
    if description == None: return {"result": False}
    return {"result": False, "error": description}