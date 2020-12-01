import socket
import time
import datetime

BUFFER_SIZE = 20

def client(move):
    
    current_time = datetime.datetime.now()

    if move == "right":
        move = "[255][0][0][255]"
        
    elif move == "left":
        move = "[0][255][255][0]"
        
    else:
        move =" [255][0][255][0]"

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1243))
    s.send(move.encode('utf-8'))
    data = s.recv(BUFFER_SIZE)
    s.close()
