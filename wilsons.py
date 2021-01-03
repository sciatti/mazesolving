import random
import generator_utils as util
import numpy as np
from collections import OrderedDict

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

def wilson_create_snapshot(new_image, index, direction):
    new_image[index[0], index[1]] = 200
    if direction < 0:
        return new_image
    mark = util.maze_index(index, direction)
    new_image[mark[0], mark[1]] = 200
    return new_image


def wilsons(rows, cols, gif):
    if gif:
        return wilson_gif(rows, cols)
    
    return wilson_img(rows, cols)

def wilson_gif(rows, cols):
    directions = ['L', 'R', 'T', 'B']
    grid = [[node(['L', 'R', 'T', 'B']) for j in range(cols)] for i in range(rows)]
    
    gif_arr = []
    
    #Select arbitrary cell for maze
    rand_r = random.randint(0,rows-1)
    rand_c = random.randint(0,cols-1)
    
    maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
    gif_arr.append(maze)
    newIMG = util.create_snapshot(gif_arr[-1], (rand_r * 2 + 1, rand_c * 2 + 1), -1)
    gif_arr.append(newIMG)
    
    grid[rand_r][rand_c].in_maze = True
    
    for r in range(rows):
        for c in range(cols):
            #Already part of maze
            if grid[r][c].in_maze:
                continue
            
            #(r,c) is starting location, keep a record of locations and directions
            path_r = r
            path_c = c
            
            counter = 0
            #Dictionary from each position to frame
            cur_path = OrderedDict()
            while (not grid[path_r][path_c].in_maze):
                #Check if created loop
                
                if ((path_r, path_c)) in cur_path:
                    #Created a loop
                    frame = cur_path[(path_r,path_c)]
                    
                    newIMG = util.create_snapshot(gif_arr[frame[0] - 1].copy(), (path_r * 2 + 1,path_c * 2 + 1), -1)
                    gif_arr.append(newIMG)
                    
                    #Remove the items in loop from cur_path
                    for i in range(counter - frame[1] - 1):
                        cur_path.popitem()
                    counter = frame[1]
                    cur_path[(path_r,path_c)] = [len(gif_arr) - 1, counter]
                        
                #Pick random direction to move
                random.shuffle(directions)
                for dir in directions:
                    nbr = util.nbr_index((path_r,path_c), dir)
                    if util.bounds_check(nbr, rows,cols):
                        #out of bounds direction
                        continue
                    grid[path_r][path_c].direction = dir
                    
                    wall_idx = conv_nbr_wall(grid[path_r][path_c].direction)
                    
                    idx = (path_r * 2 + 1, path_c * 2 + 1)
                    newIMG = util.create_snapshot(gif_arr[-1].copy(), idx, wall_idx)
                    gif_arr.append(newIMG)
                    cur_path[(path_r,path_c)] = [len(gif_arr) - 1, counter]
                    cur_path.move_to_end((path_r,path_c))
                    counter += 1
                    
                    path_r, path_c = nbr
                    break
            trace_r = r
            trace_c = c
            #If gif only need to mark as part of maze
            #newIMG = gif_arr[-1].copy() 
            while((trace_r,trace_c) != (path_r,path_c)):
                #wall_idx = conv_nbr_wall(grid[trace_r][trace_c].direction)
                #newIMG = util.create_snapshot(newIMG, idx, wall_idx)
                grid[trace_r][trace_c].in_maze=True
                trace_r, trace_c = util.nbr_index((trace_r,trace_c), grid[trace_r][trace_c].direction)
            
    #Top entrance
    x = random.randint(0, cols - 1)
    
    newIMG = util.create_snapshot(gif_arr[-1].copy(), (0, x * 2 + 1), -1)
    gif_arr.append(newIMG)
    
    x = random.randint(0, cols - 1)
    
    newIMG = util.create_snapshot(gif_arr[-1].copy(), (rows * 2, x * 2 + 1), -1)
    gif_arr.append(newIMG)
    return gif_arr
    
    
def wilson_img(rows, cols):
    directions = ['L', 'R', 'T', 'B']
    grid = [[node(['L', 'R', 'T', 'B']) for j in range(cols)] for i in range(rows)]
    
    #Select arbitrary cell for maze
    rand_r = random.randint(0,rows-1)
    rand_c = random.randint(0,cols-1)

    grid[rand_r][rand_c].in_maze = True
    
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
                    path_r, path_c = nbr
                    break
            trace_r = r
            trace_c = c
            
            while((trace_r,trace_c) != (path_r,path_c)):
                wall_idx = conv_nbr_wall(grid[trace_r][trace_c].direction)
                grid[trace_r][trace_c].walls[wall_idx] = 'X'
                grid[trace_r][trace_c].in_maze=True
                trace_r, trace_c = util.nbr_index((trace_r,trace_c), grid[trace_r][trace_c].direction)
    #Top entrance
    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'
    
    x = random.randint(0, cols - 1)
    grid[len(grid) - 1][x].walls[3] = 'X'
    return grid
