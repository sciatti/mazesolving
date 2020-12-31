import numpy as np
import generator_utils as util
import random

class node:
    visited = False
    def __init__(self, index_in, walls_in, visited_in):
        self.index = index_in
        self.walls = walls_in
        self.visited = visited_in

def aldousBroder(rows, cols, gif):
    random.seed(0)
    grid = [[node((i, j), ['L', 'R', 'T', 'B'], False) for j in range(cols)] for i in range(rows)]

    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'

    neighbors = []
    idx = util.convert_2d(random.randint(0, rows * cols - 1), cols)
    current = grid[idx[0]][idx[1]]
    current.visited = True
    unvisited = rows * cols - 1

    gif_arr = []
    if gif:
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        gif_arr.append(maze)
        util.mark_node((0, x * 2 + 1), gif_arr)

    while unvisited != 0:
        neighbors = util.getNeighbor(grid, current, rows, cols)
        rndm_nbr = neighbors[random.randint(0, len(neighbors) - 1)]
        if not rndm_nbr.visited:
            wall_idx = util.conv_nbr_wall(util.conv_idx_dir(current.index, rndm_nbr.index))
            grid[current.index[0]][current.index[1]].walls[wall_idx] = 'X'
            rndm_nbr.visited = True
            unvisited -= 1

            if gif:
                util.mark_change(util.grid_to_image(current.index), gif_arr, wall_idx, util.grid_to_image(rndm_nbr.index))
        elif gif:
            util.mark_node(util.grid_to_image(current.index), gif_arr)
        current = rndm_nbr

    x = random.randint(0, cols - 1)
    grid[rows - 1][x].walls[3] = 'X'

    if gif:
        util.mark_node((rows * 2, x * 2 + 1), gif_arr)
        return gif_arr

    return grid