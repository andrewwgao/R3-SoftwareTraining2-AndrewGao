# R3-SoftwareTraining2-AndrewGao


![](maze.gif)

## Milestone #1
Created a python program that generates a random maze everytime the program is run given a number n for n x n grid

## Steps
- Used recursive backtracker algorithm for maze generation
1. Choose a starting cell
2. Randomly choose an adjacent cell that is unvisited and remove a side between the current cell and adjacent cell
3. If all adjacent cells have been visited, go back to the last cell that has no sides removed and repeat
4. Maze is generated when all cells have been visited

- Program starts by generating a n x n grid based on the value of n (random number between 5 and 50)
- Maze is generated in real life at 60FPS
