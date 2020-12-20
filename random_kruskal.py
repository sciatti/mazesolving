import random
import generator_utils as util
import numpy as np
from disjoint_set import disjoint_set

class cell:
    def __init__(self, row, col):
        self.location = (row, col)
    
    def __eq__(self, other):
        return self.location == other.location

class wall:
    def __init__(self, cell_1, cell_2):
        self.separate = (cell_1, cell_2)

class node:
    def __init__(self, walls_in):
        self.walls = walls_in

def random_kruskals(rows, cols):
    #[row][col
    #1
    cells = [[cell(i,j) for j in range(cols)] for i in range(rows)]
    wall_arr = []
    for i in range(rows):
        for j in range(cols):
            for direction in ['R', 'D']:
                nbr = util.nbr_index((i,j), direction)
                if not util.bounds_check(nbr, rows, cols):
                    wall_arr.append(wall((i,j), nbr))

    cell_set = disjoint_set(rows*cols, cols)
    grid = [[node(['L', 'R', 'T', 'B']) for j in range(cols)] for i in range(rows)]
    
    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'
    
    #for testing purposes set the seed to 0
    random.seed(0)
    #TODO: delete the previous line when done testing
    print(len(wall_arr))
    assert (len(wall_arr) == 2 * (rows - 1) * (cols - 1) + (rows - 1) + (cols - 1))
    sequence = random.sample(range(len(wall_arr)), len(wall_arr))
    #2
    for i in sequence:
        cellA = wall_arr[i].separate[0]
        cellB = wall_arr[i].separate[1]
        cell_indexA = cellA[0] * cols + cellA[1]
        cell_indexB = cellB[0] * cols + cellB[1]
        
        separateSets = cell_set.union(cell_indexA, cell_indexB)
        
        if (separateSets):
            wall_idx = util.conv_nbr_wall(util.conv_idx_dir(cellA, cellB))            
            grid[cellA[0]][cellA[1]].walls[wall_idx] = 'X'
            wall_idx = util.conv_nbr_wall(util.conv_idx_dir(cellB, cellA))            
            grid[cellB[0]][cellB[1]].walls[wall_idx] = 'X'
            
    x = random.randint(0, cols - 1)
    print(cell_set.parents)
    grid[0][x].walls[3] = 'X'
    return grid
