#!/usr/bin/env python3

import socket
from time import sleep
from PyQt5.QtCore import QThread


class TCPController(QThread):
    def run(self):
        self.ThreadActive = True
        self.tcp = MySocket()
        self.tcp.Run()

    def stop(self):
        self.tcp.Stop()
        self.ThreadActive = False
        self.quit()


class MySocket(socket.socket):

    def __init__(self):
        super().__init__()
        self.HOST = '127.0.0.1'  # localhost
        self.PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
        self.Running = False
        self.message = "hello!"

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
                    while True:
                        conn.send(self.message.encode())
                        sleep(2)

    def SetMessage(self, message):
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
    

