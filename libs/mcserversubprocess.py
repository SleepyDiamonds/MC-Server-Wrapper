class MCServerSubprocess():
    def __init__(self, server_index, subprocess):
        self.server_index = server_index
        self.subprocess = subprocess

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