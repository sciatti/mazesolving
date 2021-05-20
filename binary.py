import numpy as np
import random
import generator_utils as util

class node:
    direction=''
    in_maze=False
    def __init__(self, walls_in):
        self.walls = walls_in

def binary_tree_maze(rows, cols, gif):
    grid = [[node(['L', 'R', 'T', 'B']) for j in range(cols)] for i in range(rows)]
    dirArr = [1, 3] #r,b
    
    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'

    gif_arr = []
    if gif:
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        gif_arr.append(maze)
        util.mark_node((0, x * 2 + 1), gif_arr)

    for i in range(rows):
        for j in range(cols):
            if i == rows - 1:
                x = 0
                if i == rows - 1 and j == rows - 1:
                    continue
            elif j == cols - 1:
                x = 1
            else:
                x = random.randint(0, 1)
            grid[i][j].walls[dirArr[x]] = 'X'
            if gif:
                util.mark_change(util.grid_to_image((i, j)), gif_arr, dirArr[x])

    x = random.randint(0, cols - 1)
    grid[rows - 1][x].walls[3] = 'X'
    
    if gif:
        util.mark_node((rows * 2, x * 2 + 1), gif_arr)
        return gif_arr    
    return grid
