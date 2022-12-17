class MinecraftServer():
    def __init__(self, index, name, ip_addr, port,rcon_port, rcon_passwd):
        self.index = index
        self.name = name
        self.ip_addr = ip_addr
        self.port = port
        self.rcon_port = rcon_port
        self.rcon_passwd = rcon_passwd