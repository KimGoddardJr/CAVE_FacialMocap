#!/usr/bin/env python3

import socket
from time import sleep


class MySocket(socket.socket):

    def __init__(self):
        super().__init__()
        self.HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        self.PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    def Run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected to', addr)
                while True:
                    str = "hello!"
                    conn.send(str.encode())
                    sleep(2)

    def SendMessage(self, message):
        pass



if __name__ == "__main__":
    conn = MySocket()
    conn.Run()
    

