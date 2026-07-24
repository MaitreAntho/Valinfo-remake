import socket
import os.path
import time
import os
from src.i18n import t

class Error:
    
    def __init__(self, log):
        self.log = log


    def PortError(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("127.0.0.1", port))
        except:
            print(t("firewall_blocked"))
            self.log("Port is being blocked by the firewall or in use by another application")
        sock.close()

    def LockfileError(self, path):
        
        if os.path.exists(path):
            return True
        else:
            # self.log("Lockfile does not exist, VALORANT is not open")
            print(t("valorant_not_open"))
            while not os.path.exists(path):
                time.sleep(1)
            os.system('cls')
            return True
