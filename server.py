import socket
import time
import datetime

BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1243))
s.listen(1)

while True:
    current_time = datetime.datetime.now()
    clientsocket, address = s.accept()
    data = clientsocket.recv(BUFFER_SIZE)
    
    if not data:
        break
    
    print("Received [", current_time,"]: ", data)
    clientsocket.send(data)
    
clientsocket.close()
