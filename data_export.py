
"""
https://docs.python.org/3/howto/sockets.html
https://docs.unrealengine.com/4.27/en-US/API/Runtime/Sockets/FSocket/
"""


import socket

#PyQt application acts as client to send/recv data
class Sender():
    def __init__(self):
        TCP_IP = '127.0.0.1' #localhost
        BUFFER_SIZE = 1024
        TCP_PORT = 8000
        self.s = None

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(5)
        self.s.connect((self.TCP_IP, self.TCP_PORT))

    def sendMessage(self, MESSAGE):
        self.s.send(MESSAGE)

    def receiveMessage(self):
        BUFFER_SIZE = 1024
        data = self.s.recv(BUFFER_SIZE)
        print(u"client received data:", data.decode("utf-8"))

    def disconnect(self):
        self.s.close()

class Recvr():
    def __init__(self):
        TCP_IP = '127.0.0.1' #localhost
        BUFFER_SIZE = 1024
        TCP_PORT = 8000
    def connect(self):
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        serversocket.bind((socket.gethostname(), 80))
        # become a server socket
        serversocket.listen(5)
    def disconnect(self):
        self.s.close()