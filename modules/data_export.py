#!/usr/bin/env python3

#import sys
#sys.path.append(r'C:\Program Files\Epic Games\UE_4.27\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python')
#from remote_execution import RemoteExecution
import threading
import socket
from time import sleep
from PySide2.QtCore import QThread

class myRemoteExecution():##RemoteExecution):
    def __init__(self):
        super().__init__()

class TCPController(threading.Thread):
    tcp = None
    
    def Run(self):
        print("Run controller thread")
        self.ThreadActive = True
        if self.tcp is None:
            self.tcp = MySocket()
        self.tcp.Run()

    def Stop(self):
        print("Stop controller thread")
        self.tcp.Stop()
        self.ThreadActive = False
        self.quit()

    def SetMessage(self, msg):
        self.tcp.SetMessage(msg)

class MySocket(socket.socket):
    def __init__(self):
        super().__init__()
        print("Init socket")
        self.HOST = '127.0.0.1'  # localhost
        self.PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
        self.Running = False
        self.message = "..."
        self.DataReceived = True

    def Run(self):
        self.Running = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        if self.Running:
            print("Run TCP")
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            if conn:
                print('Connected to', addr)
            else:
                print("No TCP connection found")
                return
            
            while self.Running:
                if self.DataReceived:
                    print("Sending message")
                    conn.send(self.message.encode())
                    sleep(10)

                else:
                    print("No data")

            print("exit")


    def SetMessage(self, message):
        print("Set message")
        self.message = message
        self.DataReceived = True

    def Stop(self):
        print("Stop TCP")
        self.DataReceived = False
        self.Running = False


if __name__ == "__main__":
    conn = TCPController()
    conn.Run()
    while True:
        conn.SetMessage("0.0,0.0,0.0") 
        sleep(1)

