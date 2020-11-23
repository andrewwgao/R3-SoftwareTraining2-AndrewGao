# import modules
import pygame
import numpy
import random

done = False # boolean variable for checking when maze is fully generated

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

n = random.randint(5,50) # random maze size

w = 800 # width
h = 800 # height
sr = w/n # size of 1 cell (square)

screen = pygame.display.set_mode((w, h)) # set window size to 800x800
clock = pygame.time.Clock() # fps for pygame

# maze class
class maze:
    '''
    declaring variables
    '''
    def __init__(self, x, y):
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.adj = [] # the 4 cells adjacent to the current cell
        self.visited = False # variable to track if cell was visited for algorithm
        self.walls = [True, True, True, True] # variable to see if there is a wall (1 of the 4 sides of a cell)
    '''
    drawing the walls
    '''
    def draw(self, color):
        if self.walls[0]: # draw the top wall
            pygame.draw.line(screen, color, [self.x*sr, self.y*sr], [self.x*sr+sr, self.y*sr])
        if self.walls[1]: # draw the right wall
            pygame.draw.line(screen, color, [self.x*sr+sr, self.y*sr], [self.x*sr+sr, self.y*sr + sr])
        if self.walls[2]: # draw the bottom wall
            pygame.draw.line(screen, color, [self.x*sr+sr, self.y*sr+sr], [self.x*sr, self.y*sr+sr])
        if self.walls[3]: # draw the left wall
            pygame.draw.line(screen, color, [self.x*sr, self.y*sr+sr], [self.x*sr, self.y*sr])

    '''
    adding the adjacent cells to the adj array if they have not been visited
    '''        
    def add_adj(self):
        if self.x > 0:
            self.adj.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.adj.append(grid[self.x][self.y - 1])
        if self.x < n - 1:
            self.adj.append(grid[self.x + 1][self.y])
        if self.y < n - 1:
            self.adj.append(grid[self.x][self.y + 1])


'''
remove one of the sides of the current cell to create a "path"
'''  
def remove_walls(a, b):
    if a.y == b.y and a.x > b.x: # remove left wall
        grid[b.x][b.y].walls[1] = False
        grid[a.x][a.y].walls[3] = False
    if a.y == b.y and a.x < b.x: # remove right wall
        grid[a.x][a.y].walls[1] = False
        grid[b.x][b.y].walls[3] = False
    if a.x == b.x and a.y < b.y: # remove top wall
        grid[b.x][b.y].walls[0] = False
        grid[a.x][a.y].walls[2] = False
    if a.x == b.x and a.y > b.y: # remove bottom wall
        grid[a.x][a.y].walls[0] = False
        grid[b.x][b.y].walls[2] = False

grid = [[maze(i, j) for j in range(n)] for i in range(n)] # array for grid

for i in range(n): # adjacent cell array
    for j in range(n):
        grid[i][j].add_adj()

current = grid[0][0] # start at top left corner of window
visited = [current] # the current cell is visited
completed = False # boolean variable to check when maze is done generating

while not done:
    
    clock.tick(60) # run at 60 fps
    screen.fill(BLACK) # background color
    
    if not completed: # keep looping until maze is generated
        grid[current.x][current.y].visited = True # current cell is visited
        next_cell = False # next cell
        temp = 10 # repeat loop

        while not next_cell and not completed: # randomly choose an adjacent cell to go next
            r = random.randint(0, len(current.adj)-1)
            Tempcurrent = current.adj[r] 
            if not Tempcurrent.visited: # if the chosen cell has not been visited yet
                visited.append(current)
                current = Tempcurrent
                next_cell = True
            if temp == 0: # if there is still unvisited cells, keep looping
                temp = 10
                if len(visited) == 0: # all cell visited, end the loop
                    completed = True
                    break
                else:
                    current = visited.pop() # adds current cell to visited array
            temp = temp - 1

        if not completed: # maze not completed, keep removing walls
            remove_walls(current, visited[len(visited)-1])

        for i in range(n): # draw grid
            for j in range(n):
                grid[i][j].draw(WHITE)

        current.visited = True
        pygame.display.flip() # update display

    for event in pygame.event.get(): # checks for exiting the window
        if event.type == pygame.QUIT:
            done = True
quit()
