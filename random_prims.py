import random
import generator_utils as util
import numpy as np

class node:
    def __init__(self, walls_in):
        self.walls = walls_in
        self.visited = False

#TODO
def simplified_random_prims(rows, cols, gif):
    #Top Entrance
    x = random.randint(0, cols - 1)
    
    grid = [[node(['L', 'R', 'T', 'B']) for j in range(cols)] for i in range(rows)]
    grid[0][x].walls[2] = 'X'

    gif_arr = []
    if gif:
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        gif_arr.append(maze)
        util.mark_node((0, x * 2 + 1), gif_arr)

    #Select random cell
    r = random.randrange(rows)
    c = random.randrange(cols)
    
    adj_cells = {(r,c)} #Set containing neighboring cells
    
    while len(adj_cells):
        #Select random cell from adjacent list
        cell = random.sample(adj_cells, 1)[0]
        adj_cells.remove(cell)
        
        grid[cell[0]][cell[1]].visited = True
        
        #Randomly scan around to figure out what wall to tear down
        directions = ['R','B','T','L']
        random.shuffle(directions)
        separate = True
        for dir in directions:
            nbr = util.nbr_index((cell[0], cell[1]), dir)
            if util.bounds_check(nbr, rows, cols):
                continue
            if grid[nbr[0]][nbr[1]].visited:
                #First time tear down wall
                if separate:
                    wall_idx = util.conv_nbr_wall(util.conv_idx_dir(cell, nbr))
                    grid[cell[0]][cell[1]].walls[wall_idx] = 'X'
                    separate = False
                    if gif:
                        util.mark_change(util.grid_to_image(cell), gif_arr, wall_idx)
                continue
            elif gif:
                util.mark_node(util.grid_to_image(cell), gif_arr)
            adj_cells.add(nbr)
    
    x = random.randint(0, cols - 1)
    grid[len(grid) - 1][x].walls[3] = 'X'

    if gif:
        util.mark_node((rows * 2, x * 2 + 1), gif_arr)
        return gif_arr

    return grid
