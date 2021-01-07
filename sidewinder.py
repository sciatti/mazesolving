import generator_utils as util
import random
import numpy as np

class node:
    def __init__(self, walls_in):
        self.walls = walls_in

def sidewinder(rows, cols, gif):
    grid = [[node(['L','R','T','B']) for j in range(cols)] for i in range(rows)]
    
    for c in range(cols - 1):
        #Top row must be a single passage
        grid[0][c].walls[1] = 'X'
    
    for r in range(1, rows):
        run_start = 0
        for c in range(cols):
            #Cur cell is (r,c)
            
            #Carve east if 1 and not last column
            carve_east = random.randint(0, 1)
            if (carve_east and c != cols - 1):
                grid[r][c].walls[1] = 'X'
            else:
                col = random.randint(run_start, c)
                grid[r][col].walls[2] = 'X'
                run_start = c + 1
    
    #Side entrance and exit then rotate in generator
    x = random.randint(0, rows - 1)
    grid[x][0].walls[0] = 'X'
    
    x = random.randint(0, rows - 1)
    grid[x][cols - 1].walls[1] = 'X'
    return grid
