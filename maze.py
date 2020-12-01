import pygame
import time
import random
import math
import socket
import threading

WIDTH = 800
HEIGHT = 800
FPS = 30
grid = []
visited = []
solVisited = []
availableSpaces = {}
solution = []
HEADERSIZE = 4

direction = {
    "N":[0,-1],
    "S":[0,1],
    "E":[1,0],
    "W":[-1,0],
}

n = 5
w = WIDTH/n
h = HEIGHT/n

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid")
clock = pygame.time.Clock()
white = [255, 255, 255]
black = [0,0,0]
screen.fill(white)
pygame.display.update()



def drawGrid(n):
    w = WIDTH/n
    h = HEIGHT/n
    x = 0.0
    y = 0.0
    for i in range(0,n):
        for j in range(0,n):
            pygame.draw.line(screen, black,[x,y],[x+w,y],2) # TOP
            pygame.draw.line(screen, black,[x, y], [x, y+h],2) # LEFT
            pygame.draw.line(screen, black,[x + w, y], [x + w, y + h],2) # RIGHT
            pygame.draw.line(screen, black,[x, y + h], [x+w, y + h],2) # BOTTOM
            grid.append([x,y])
            availableSpaces[(x,y)] = []
            x += w
        x = 0.0
        y += h
    #print(len(grid))
    pygame.display.update()

def carveMazefrom(x,y,grid):
    if [x,y] in visited or [x,y] not in grid:
        return
    else:
        visited.append([x,y])


    dir_order = ["N","S","E","W"]
    random.shuffle(dir_order)

    for i in range(0,len(dir_order)):
        next_x = x + (direction.get(dir_order[i])[0])*w
        next_y = y + (direction.get(dir_order[i])[1])*h
        
        if [next_x, next_y] not in visited and [next_x, next_y] in grid:
            if dir_order[i] == "N":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["N"]
                pygame.draw.line(screen, white,[x,y],[x+w,y],2)
            if dir_order[i] == "S":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["S"]
                pygame.draw.line(screen, white,[x, y + h], [x+w, y + h],2) 
            if dir_order[i] == "E":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["E"]
                pygame.draw.line(screen, white,[x + w, y], [x + w, y + h],2) 
            if dir_order[i] == "W":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["W"]
                pygame.draw.line(screen, white,[x, y], [x, y+h],2)
            pygame.display.update()
            #time.sleep(0.05) # Comment This If You Dont Want To Wait For Maze To Generate
            carveMazefrom(next_x,next_y,grid)
        
        



def solveMaze (x,y,aSpaces,grid,currentPath):
    if ((x,y) in currentPath):
        return
    currentPath.append((x,y))

    if (x,y) == (WIDTH-w,HEIGHT-h):
        solution[:] = list(currentPath)
        currentPath.pop()
        return

    for i in range(0,len(aSpaces.get((x,y)))):
        next_x = x + (direction.get(aSpaces.get((x,y))[i])[0])*w
        next_y = y + (direction.get(aSpaces.get((x,y))[i])[1])*h
        if aSpaces.get((x,y))[i] == "N":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "S":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "E":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "W":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
    currentPath.pop()
    return

            
drawGrid(n)
carveMazefrom(0,0,grid)
solveMaze(0,0,availableSpaces,grid,[])
for i in solution:
    pygame.draw.circle(screen, [255,0,0], [int(i[0]+(w/2)) , int(i[1]+(h/2))],10)
    pygame.display.update()
    #time.sleep(0.05) # Comment This If You Dont Want To Wait For Solution To Generate

# Write your code here or make a new python file and run the code from here
# The array that contains the solution is called solution[], use this for the TCP Stream.

"""
Sends commands to robot (server) in the format: [M1_A][M1_B][M2_A][M2_B]
M1 - robot's left side motors
M2 - robot's right side motors
A - backwards
B - forwards
[0][0][0][0] - stop
[0][255][0][255] - go forward
[255][0][255][0] - go backward
[0][255][255][0] - turn right
[255][0][0][255] - turn left
"""
def client():
    """
    Sends movement commands to robot (server), where '[M1_A][M1_B][M2_A][M2_B]',
    1 is left motors, 2 is right motors, and
    A = 255, B = 0 => reverse, A = 0, B = 255 => forward
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1243))
    
    def motor(pwm):
        return '[{}][{}]'.format(-min(pwm, 0), max(0, pwm))

    def drive(pwm):
        return motor(pwm) + motor(pwm)

    def turn(pwm):
        return motor(pwm) + motor(-pwm)
    
    curr_pos = solution[0]
    facing = 'S'
    direction = {(0, -h): 'N',(w, 0): 'E',(0, h): 'S',(-w, 0): 'W'}

    for move in solution[1:]:
        move_dir = direction.get((move[0] - curr_pos[0], move[1] - curr_pos[1]))

        if facing != move_dir:
            if facing + move_dir in ('NE', 'ES', 'SW', 'WN'):
                command = turn(255)

            elif facing + move_dir in ('NW', 'WS', 'SE', 'EN'):
                command = turn(-255)
            else:
                raise RuntimeError("can't go there".format(facing, move_dir))

            s.send('{chars:<{header}}{msg}'.format(chars=len(command), header=HEADERSIZE, msg=command).encode('utf-8'))
            time.sleep(1)

        command = drive(255)
        s.send('{chars:<{header}}{msg}'.format(chars=len(command), header=HEADERSIZE, msg=command).encode('utf-8'))
        curr_pos = move
        facing = move_dir
        pygame.display.update()
        time.sleep(1)
        
    msg = '[0][0][0][0]'
    s.send('{chars:<{header}}{msg}'.format(chars=len(msg), header=HEADERSIZE, msg=msg).encode('utf-8'))
    time.sleep(1)
    
    msg = 'DONE'
    s.send('{chars:<{header}}{msg}'.format(chars=len(msg), header=HEADERSIZE, msg=msg).encode('utf-8'))
    s.close()

t = threading.Thread(target = client)
t.start()
    
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
