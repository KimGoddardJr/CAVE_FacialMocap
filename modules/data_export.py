#!/usr/bin/env python3

import socket
from time import sleep
from PyQt5.QtCore import QThread

class TCPController(QThread):
    def Run(self):
        self.ThreadActive = True
        self.tcp = MySocket()
        self.tcp.Run()

    def Stop(self):
        self.tcp.Stop()
        self.ThreadActive = False
        self.quit()

    def SetMessage(self, msg):
        self.tcp.SetMessage(msg)

#class IMSLLController(QThread):

class MySocket(socket.socket):

    def __init__(self):
        super().__init__()
        self.HOST = '127.0.0.1'  # localhost
        self.PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
        self.Running = False
        self.message = "."
        self.DataReceived = False

    def Run(self):
        print("Run TCP")
        self.Running = True
        while self.Running:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.HOST, self.PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('Connected to', addr)
                    while True and self.DataReceived:
                        conn.send(self.message.encode())
                        self.DataReceived = False

    def SetMessage(self, message):
        self.DataReceived = True
        self.message = message

    def Stop(self):
        print("Stop TCP")
        self.Running = False

class IMSLLController():
    #REMOVED-----------
    #------------------
    pass


if __name__ == "__main__":
    conn = MySocket()
    conn.Run()
    

