# import modules
import socket
import time
import datetime

HEADERSIZE = 4 # number of chars to buffer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket object
s.bind((socket.gethostname(), 1243)) # connect to IP and Port
s.listen(1) # listen to a queue of 1

while True:
    # now our endpoint knows about the OTHER endpoint
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    full_msg = ''
    msg_len = -1
    new_msg = True

    while True:
        msg = clientsocket.recv(HEADERSIZE)

        if new_msg:
            msg_len = int(msg)
            new_msg = False

        full_msg += msg.decode('utf-8')

        if len(full_msg) - HEADERSIZE == msg_len:
            if full_msg[HEADERSIZE:] == '[0][255][0][255]':
                move = 'forward'
            elif full_msg[HEADERSIZE:] == '[0][255][255][0]':
                move = 'right'
            elif full_msg[HEADERSIZE:] == '[255][0][0][255]':
                move = 'left'
            elif full_msg[HEADERSIZE:] == '[0][0][0][0]':
                move = 'stop'
            else:
                move = 'UNKNOWN'
            print("Received [{:%y/%m/%d %I:%M:%S %p}]: {}".format(datetime.datetime.now(), full_msg[HEADERSIZE:]))

            if full_msg[HEADERSIZE:] == 'DONE':
                clientsocket.close()
                print(f"Connection from {address} has been closed.")
                break

            full_msg = ''
            new_msg = True
