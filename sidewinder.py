import generator_utils as util
import random
import numpy as np

class node:
    def __init__(self, walls_in):
        self.walls = walls_in

def sidewinder(rows, cols, gif):
    if gif:
        return sidewinder_gif(rows, cols)
    
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

def sidewinder_gif(rows, cols):
    gif_arr = []
    maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
    gif_arr.append(maze)
    
    for c in range(cols - 1):
        newIMG = util.create_snapshot(gif_arr[-1].copy(), (1, c * 2 + 1), 1)
        gif_arr.append(newIMG)
    
    newIMG = util.create_snapshot(gif_arr[-1],(1, (cols-1) * 2 + 1), -1)
    
    for r in range(1, rows):
        run_start = 0
        for c in range(cols):
            #Cur cell is (r,c)
            
            #Carve east if 1 and not last column
            carve_east = random.randint(0, 1)
            if (carve_east and c != cols - 1):
                newIMG = util.create_snapshot(gif_arr[-1].copy(), (r * 2 + 1, c * 2 + 1),1)
                gif_arr.append(newIMG)
            else:
                col = random.randint(run_start, c)
                newIMG = util.create_snapshot(gif_arr[-1].copy(), (r * 2 +1, col * 2 + 1),2)
                gif_arr.append(newIMG)
                newIMG = util.create_snapshot(gif_arr[-1], (r*2 + 1, c*2 + 1), -1)
                run_start = c + 1
    
    #Side entrance and exit then rotate in generator
    x = random.randint(0, rows - 1)
    
    y = random.randint(0, rows - 1)
    newIMG = util.create_snapshot(gif_arr[-1].copy(), (x *2 + 1, 0), -1)
    gif_arr.append(newIMG)
    newIMG = util.create_snapshot(gif_arr[-1], (y *2 + 1, cols*2), -1)
    
    return gif_arr
