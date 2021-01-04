import generator_utils as util
import random
from collections import deque
import numpy as np

class node:
    visited = False
    def __init__(self, index_in, walls_in, visited_in):
        self.index = index_in
        self.walls = walls_in
        self.visited = visited_in


def random_DFS(rows, cols, gif):
    stack = deque()
    grid = [[node((i, j), ['L', 'R', 'T', 'B'], False) for j in range(cols)] for i in range(rows)]
    #1
    x = random.randint(0, cols - 1)
    grid[0][x].visited = True
    grid[0][x].walls[2] = 'X'
    stack.append(grid[0][x])
    #2
    gif_arr = []
    if gif:
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        gif_arr.append(maze)
        util.mark_node((0, x * 2 + 1), gif_arr)

    while len(stack) != 0:
        #1
        curr = stack.pop()
        #2
        neighbors = util.neighborCheck(grid, curr, rows, cols)
        if len(neighbors) > 0:
            #1
            stack.append(curr)
            #2
            nbr_dir = neighbors[random.randint(0, len(neighbors) - 1)]
            new_index = util.nbr_index(curr.index, curr.walls[nbr_dir])
            new_curr = grid[new_index[0]][new_index[1]]
            #3
            curr.walls[nbr_dir] = 'X'
            #4
            new_curr.visited = True
            stack.append(new_curr)
            if gif:
                util.mark_change(util.grid_to_image(curr.index), gif_arr, nbr_dir)
        elif gif:
            util.mark_node(util.grid_to_image(curr.index), gif_arr)

    x = random.randint(0, cols - 1)
    grid[rows - 1][x].walls[3] = 'X'
    
    if gif:
        util.mark_node((rows * 2, x * 2 + 1), gif_arr)
        return gif_arr

    return grid
    x = 0