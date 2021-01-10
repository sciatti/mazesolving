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

def walk(grid, cur_cell, gif):
    #Check neighbors
    grid[cur_cell[0]][cur_cell[1]].visited = True
    
    valid_nbrs = []
    
    for dir in Directions:
        idx = util.nbr_index(cur_cell, dir)
        if(not util.bounds_check(idx, Rows, Cols) and not grid[idx[0]][idx[1]].visited):
            #unvisited neighbor
            valid_nbrs.append((idx, dir))
    
    if(len(valid_nbrs) == 0):
        if gif:
            newIMG = util.create_snapshot(gif_arr[-1].copy(), (cur_cell[0] * 2 + 1, cur_cell[1] * 2 + 1), -1)
            gif_arr.append(newIMG)
        return
    
    #Select random valid neighbor to walk to next
    x = random.randint(0, len(valid_nbrs) - 1)
    dir = valid_nbrs[x][1]
    wall_idx = local_wall_idx(dir)
    
    if gif:
        newIMG = util.create_snapshot(gif_arr[-1].copy(), (cur_cell[0] * 2 + 1, cur_cell[1] * 2 + 1), wall_idx)
        gif_arr.append(newIMG)
    
    grid[cur_cell[0]][cur_cell[1]].walls[wall_idx] = 'X'
    
    walk(grid, valid_nbrs[x][0], gif)

def hunt(grid, gif):
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
                    #Choose random neighbor in maze to connect to
                    x = random.randint(0, len(valid_nbrs) - 1)
                    wall_idx = local_wall_idx(valid_nbrs[x])
                    
                    if gif:
                        newIMG = util.create_snapshot(gif_arr[-1].copy(), (r * 2 + 1, c * 2 + 1), wall_idx)
                        gif_arr.append(newIMG)
                        
                    grid[r][c].walls[wall_idx] = 'X'
                    return (r,c)
    return None

def hunt_and_kill(rows, cols, gif):
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
    
    global gif_arr
    gif_arr = []
    if gif:
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        gif_arr.append(maze)
        newIMG = util.create_snapshot(gif_arr[-1], (rand_r * 2 + 1, rand_c * 2 + 1), -1)
        gif_arr.append(newIMG)
    
    while cell != None:
        walk(grid, cell, gif)
        cell = hunt(grid, gif)
    
    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'
    
    y = random.randint(0, cols - 1)
    grid[len(grid) - 1][y].walls[3] = 'X'
    
    if gif:
        newIMG = util.create_snapshot(gif_arr[-1].copy(), (0, x * 2 + 1), -1)
        newIMG = util.create_snapshot(newIMG, (rows * 2, y * 2 + 1), -1) 
        gif_arr.append(newIMG)
        return gif_arr
    
    return grid
