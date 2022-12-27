from .logmanager import LogManager

class MCServerSubprocess():
    def __init__(self, server, subprocess):
        self.server = server
        self.subprocess = subprocess
        self.log_manager = LogManager(server.index)

    def terminate(self):
        """
        Stops minecraft server safely.
        (Runs `/stop` command and waits for subprocess to terminate)
        """
        self.subprocess.communicate(input="stop".encode())
    
    def stdin_write(self, command):
        """
        Writes command to `stdin` of Minecraft Server's subprocess.
        """
        self.subprocess.stdin.write(f"{command}\n".encode())
        self.subprocess.stdin.flush()