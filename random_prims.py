import random
import generator_utils as util
import numpy as np

class node:
    def __init__(self, walls_in):
        self.walls = walls_in
        self.visited = False

#TODO
def random_prims(rows, cols):
    #Top Entrance
    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'
    
    grid = [[['L', 'R', 'T', 'B']) for j in range(cols)] for i in range(rows)]
    
    #Select random cell
    r = randrange(rows)
    c = randrange(cols)
    
    
    adj_cells = {(r,c)} #Set containing neighboring cells
    
    while len(adj_cells):
        #Select random cell from adjacent list
        cell = random.sample(adj_cells, 1)[0]
        adj_cells.remove(cell)
        
        grid[cell[0]][cell_c[1]].visited = True
        
        #Randomly scan around to figure out what wall to tear down
        separate = True
        for dir in ['R','B','T','L']:
            nbr = util.nbr_index((cell_r, cell_c), dir)
            if utils.bounds_check(nbr, rows, cols):
                continue
            if grid[nbr[0]][nbr[1]].visited:
                #First time tear down wall
                if separate:
                    wall_idx = util.conv_nbr_wall(util.conv_idx_dir(cell, nbr))
                    grid[cell[0]][cell[1]].walls[wall_idx] = 'X'
                    separate = False
                    continue
            adj_cells.add(nbr)
    
    x = random.randint(0, cols - 1)
    grid[len(grid) - 1][x].walls[3] = 'X'
    return grid
