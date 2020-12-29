import random
import generator_utils as util
import numpy as np

class node:
    direction=''
    in_maze=False
    def __init__(self, walls_in):
        self.walls = walls_in

def conv_nbr_wall(dir):
    if dir == 'L':
        return 0
    elif dir == 'R':
        return 1
    elif dir == 'T':
        return 2
    return 3

def wilsons(rows, cols):
    directions = ['L', 'R', 'T', 'B']
    grid = [[node(['L', 'R', 'T', 'B']) for j in range(cols)] for i in range(rows)]
    
    #Top entrance
    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'
    
    #Select arbitrary cell for maze
    grid[random.randint(0,rows-1)][random.randint(0,cols-1)].in_maze = True
    
    for r in range(rows):
        for c in range(cols):
            #Already part of maze
            if grid[r][c].in_maze:
                continue
            
            #(r,c) is starting location, keep a record of locations and directions
            path_r = r
            path_c = c
            
            while (not grid[path_r][path_c].in_maze):
                #Pick random direction to move
                random.shuffle(directions)
                for dir in directions:
                    nbr = util.nbr_index((path_r,path_c), dir)
                    if util.bounds_check(nbr, rows,cols):
                        #out of bounds direction
                        continue
                    grid[path_r][path_c].direction = dir
                    
                    #IF GIF NEED TO MARK WALL AS 'X' HERE, CHECK IF LOOP AND ERASE LOOP IF NECESSARY
                    path_r, path_c = nbr
                    break
            #NO GIF | Trace path here
            trace_r = r
            trace_c = c
            while((trace_r,trace_c) != (path_r,path_c)):
                wall_idx = conv_nbr_wall(grid[trace_r][trace_c].direction)
                grid[trace_r][trace_c].walls[wall_idx] = 'X'
                grid[trace_r][trace_c].in_maze=True
                trace_r, trace_c = util.nbr_index((trace_r,trace_c), grid[trace_r][trace_c].direction)
                
    x = random.randint(0, cols - 1)
    grid[len(grid) - 1][x].walls[3] = 'X'
    
    return grid