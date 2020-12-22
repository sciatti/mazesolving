import random
import generator_utils as util
import numpy as np

class node:
    def __init__(self, walls_in):
        self.walls = walls_in
        self.visited = False

#TODO
def random_prims(rows, cols):
    
    grid = [[['L', 'R', 'T', 'B']) for j in range(cols)] for i in range(rows)]
    
    #Select random cell
    r = randrange(rows)
    c = randrange(cols)
    
    
    adj_cells = [(r,c)] #Turn into a set probably so that never add neighbor more than once
    #Figure out if storing direction from which discovered or if randomly scanning around cell to determine which wall to tear down to connect to maze
    
    while len(adj_cells):
        #Select random cell from adjacent list
        idx = randrange(len(adj_cells))
        cell_r, cell_c = adj_cells[idx]
        del adj_cells[idx]
        if grid[cell_r][cell_c]
        
        grid[cell_r][cell_c].visited = True
        #Randomly scan around to figure out what wall to tear down
        
        for dir in ['R','B','T','L']:
            nbr = util.nbr_index((cell_r, cell_c), dir)
            if utils.bounds_check(nbr, rows, cols):
                continue
            if grid[nbr[0]][nbr[1]].visited:
                continue
            adj_cells.append(nbr)
        
        
    #grid[r][c].visited = True
    
    
    print("implement")
    return np.zeros((rows,cols), dtype=np.uint8)