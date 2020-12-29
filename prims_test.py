import random
import generator_utils as util
import numpy as np

class node:
    def __init__(self, walls_in):
        self.walls = walls_in
        self.visited = False

def random_prims(rows, cols, gif):
    
    grid = [[node(['L', 'R', 'T', 'B']) for j in range(cols)] for i in range(rows)]
    
#TODO: figure out what is causing there to be a single wall island in the maze
    #Select random cell
    r = random.randint(0, rows - 1)
    c = random.randint(0, cols - 1)
        
    tree = set((r,c))

    adj_cells = {}

    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'

    gif_arr = []
    if gif:
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        gif_arr.append(maze)
        util.mark_node((0, x * 2 + 1), gif_arr)

    for dir in ['R','B','T','L']:
        nbr = util.nbr_index((r,c), dir)
        if util.bounds_check(nbr, rows, cols):
            continue
        adj_cells[nbr] = (r,c)

    while len(adj_cells):
        #Select random cell from adjacent list
        idx = random.sample(list(adj_cells), 1)[0]
        parent = adj_cells[idx]
        del adj_cells[idx]
        tree.add(idx)

        grid[idx[0]][idx[1]].visited = True

        parent_dir = util.conv_idx_dir(idx, parent)
        grid[idx[0]][idx[1]].walls[util.conv_nbr_wall(parent_dir)] = 'X'

        if gif:
            util.mark_change(util.grid_to_image(idx), gif_arr, util.conv_nbr_wall(parent_dir))

        for dir in ['R','B','T','L']:
            nbr = util.nbr_index(idx, dir)
            if util.bounds_check(nbr, rows, cols):
                continue
            if nbr in tree:
                continue
            adj_cells[nbr] = idx
        
    x = random.randint(0, cols - 1)
    grid[len(grid) - 1][x].walls[3] = 'X'

    if gif:
        util.mark_node((rows * 2, x * 2 + 1), gif_arr)
        return gif_arr

    return grid