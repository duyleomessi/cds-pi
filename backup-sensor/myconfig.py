import threading

STADIUM = "G" # "Green" G1,R1,G2,R2

SERVER_IP = '192.168.1.51'
SERVER_PORT = 8080
    
class myThread(threading.Thread):
    def __init__(self, threadID, name, function):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.function = function
    def run(self):
        print("Starting %s" % self.name)
        self.function(self.name)
        print("Exiting " + self.name)