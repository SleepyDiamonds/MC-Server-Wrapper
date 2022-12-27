import commons

class LogManager():
    def __init__(self, mc_subprocess, max_read_lines):
        self.mc_subprocess = mc_subprocess
        self.server_index = mc_subprocess.server.index
        self.server_name = mc_subprocess.server.name
        self.max_read_lines = max_read_lines

    def read_last_logs(self):
        """
        Reads latest logs from `stdout`.
        """
        line = self.subprocess.stdout.readline()
        print(line)

    # [info] hello  <----- last_loaded_line -- 3
    # [warning] plugin not loaded ------------ 2
    # [info] hi     -------------------------- 1

    def read_old_logs(self, last_loaded_line):
        try: 
            old_logs = []

            # Reads the last "self.max_read_lines" number of logs
            # Used when the client connects
            if last_loaded_line == 0:
                file = open(f"servers/{self.server_name}/logs/latest.log", "r")
                
                file_logs = file.readlines()
                file_logs.reverse()
                
                for index, line in enumerate(file_logs, start=1):
                    old_logs.append(line.rstrip())
                    if index >= self.max_read_lines:
                        break
                
                return (True, old_logs)
            
            # Used for reading the specific number of lines
            else:
                file = open(f"servers/{self.server_name}/logs/latest.log", "rb")
                
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
                
                return (True, final_logs)
        except:
            return (False)

            
    @staticmethod
    def read_old_logs_index(index, last_loaded_line=0, max_read_lines=25):
        try:
            old_logs = []

            # Reads the last "self.max_read_lines" number of logs
            # Used when the client connects
            server = commons.getServerByIndex(index)

            if last_loaded_line == 0:
                file = open(f"servers/{server.name}/logs/latest.log", "r")
                
                file_logs = file.readlines()
                file_logs.reverse()
                
                for index, line in enumerate(file_logs, start=1):
                    old_logs.append(line.rstrip())
                    if index >= max_read_lines:
                        break
                
                return (True, old_logs)
            
            # Used for reading the specific number of lines
            else:
                file = open(f"servers/{server.name}/logs/latest.log", "r")
                
                final_logs = []

                file_logs = file.readlines()
                file_logs.reverse()

                log_break = last_loaded_line + max_read_lines

                for index, line in enumerate(file_logs, start = 1):
                    if index <= last_loaded_line:
                        continue

                    final_logs.append(line.rstrip())
                    
                    if index >= log_break:
                        break
                
                return (True, final_logs)
        except Exception as exception:
            return (False, str(exception))
        

