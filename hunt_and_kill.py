import generator_utils as util
import random
import numpy as np

class node:
    visited = False;
    def __init__(self, walls_in):
        self.walls = walls_in

def local_wall_idx(dir):
    if dir == 'L':
        return 0
    elif dir == 'R':
        return 1
    elif dir == 'T':
        return 2
    elif dir == 'B':
        return 3

def walk(grid, cur_cell):
    #Check neighbors
    grid[cur_cell[0]][cur_cell[1]].visited = True
    
    valid_nbrs = []
    
    for dir in Directions:
        idx = util.nbr_index(cur_cell, dir)
        if(not util.bounds_check(idx, Rows, Cols) and not grid[idx[0]][idx[1]].visited):
            #unvisited neighbor
            valid_nbrs.append((idx, dir))
    
    if(len(valid_nbrs) == 0):
        return
    
    x = random.randint(0, len(valid_nbrs) - 1)
    
    dir = valid_nbrs[x][1]
    wall_idx = local_wall_idx(dir)
    
    grid[cur_cell[0]][cur_cell[1]].walls[wall_idx] = 'X'
    
    walk(grid, valid_nbrs[x][0])

def hunt(grid):
    for r in range(Rows):
        for c in range(Cols):
            if(not grid[r][c].visited):
                #Found cell not already in maze
                valid_nbrs = []
                
                for dir in Directions:
                    idx = util.nbr_index((r,c), dir)
                    if not util.bounds_check(idx, Rows, Cols) and grid[idx[0]][idx[1]].visited:
                        #valid neighbor that is part of maze
                        valid_nbrs.append(dir)
               
                if len(valid_nbrs):
                    x = random.randint(0, len(valid_nbrs) - 1)
                    wall_idx = local_wall_idx(valid_nbrs[x])
                    grid[r][c].walls[wall_idx] = 'X'
                    return (r,c)
    return None

def hunt_and_kill(rows, cols, gif):
    random.seed(0)
    
    grid = [[node(['L','R','T','B']) for j in range(cols)] for i in range(rows)]
    
    global Directions 
    Directions = ['L','R','T','B']
    global Rows
    Rows = rows
    global Cols
    Cols = cols
    
    #Choose random start, perform random walk until no unvisited neighbors of current cell --> Deadend
    #Then Enter Hunt Mode and find first unvisited cell with visited neighbors
    #Carve a passage from that cell to a random visited neigbor and begin a new walk
    rand_r = random.randint(0,rows-1)
    rand_c = random.randint(0,cols-1)
    cell = (rand_r, rand_c)
    
    while cell != None:
        walk(grid, cell)
        cell = hunt(grid)
    
    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'
    
    x = random.randint(0, cols - 1)
    grid[len(grid) - 1][x].walls[3] = 'X'
    
    return grid
