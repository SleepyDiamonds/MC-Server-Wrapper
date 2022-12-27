class LogManager():
    def __init__(self, mc_subprocess, max_read_lines: int):
        self.mc_subprocess = mc_subprocess
        self.server_index = mc_subprocess.server.index
        self.server_name = mc_subprocess.server.name
        self.max_read_lines = max_read_lines

    def read_last_logs(self):
        line = self.subprocess.stdout.readline()
        print(line)

    # [info] hello  <----- last_loaded_line -- 3
    # [warning] plugin not loaded ------------ 2
    # [info] hi     -------------------------- 1

    def read_old_logs(self, last_loaded_line):
        old_logs = []

        # Reads the last "self.max_read_lines" number of logs
        # Used when the client connects
        if last_loaded_line == None:
            file = open(f"servers/{self.server_name}/logs/latest.log", "r") #FIXME: Replace "namehere" with the server name
            
            file_logs = file.readlines()
            file_logs.reverse()
            
            for index, line in enumerate(file_logs, start=1):
                old_logs.append(line)
                if index >= self.max_read_lines:
                    break
            
            return old_logs
        
        # Used for reading the specific number of lines
        else:
            file = open(f"servers/{self.server_name}/logs/latest.log", "rb") #FIXME: Replace "namehere" with the server name
            
            final_logs = []

            file_logs = file.readlines()
            file_logs.reverse()

            log_break = last_loaded_line + self.max_read_lines

            for index, line in enumerate(file_logs, start = 1):
                if index <= last_loaded_line:
                    continue

                final_logs.append(line.rstrip())
                
                if index >= log_break:
                    break
            
            return final_logs
    

