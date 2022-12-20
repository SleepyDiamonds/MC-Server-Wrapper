class MCServer():
    def __init__(self, index, name, ip_addr, port,rcon_port, rcon_passwd, max_ram):
        self.index = index
        self.name = name
        self.ip_addr = ip_addr
        self.port = port
        self.rcon_port = rcon_port
        self.rcon_passwd = rcon_passwd
        self.max_ram = max_ram