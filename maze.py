import pygame
import time
import random
import math
import socket
from client import *

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
facing = "S" 

def direction(nextDir, drive):
    global facing
    coords = ["N","E","S","W"]
    
    while nextDir != facing:
        if facing == "N" and nextDir =="W":
            drive.append("left")
            facing = "W"
        elif facing == "W" and nextDir =="N":
            drive.append("right")
            facing = "N"
        else:
            difference = coords.index(nextDir) - coords.index(facing)
            if difference > 0:
                drive.append("right")
                facing = coords[coords.index(facing) + 1]
            else:
                drive.append("left")
                facing = coords[coords.index(facing) - 1]

move = []

def go():
    for i in range(len(solution) - 1):
        x = solution[i + 1][0] - solution[i][0]
        y = solution[i + 1][1] - solution[i][1]
        if x > 0:
            direction("E", move)
            move.append("E")
        elif x < 0:
            direction("W", move)
            move.append("W")
        elif y > 0:
            direction("S", move)
            move.append("S")
        else:
            direction("N", move)
            move.append("N")

go()

for i in range(len(move)):
    client(move[i])
    
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
