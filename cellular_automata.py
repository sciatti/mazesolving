import numpy as np
import random
import generator_utils as util

def driver(rows, cols, gif, survivalRule, birthRule, evolutions, stop_len):
    grid = np.zeros((rows * 2 + 1, cols * 2 + 1), dtype=np.uint8)
    changes = True

    y = random.randint(2, rows * 2 - 1)
    x = random.randint(2, cols * 2 - 1)
    grid[y,x] = 255

    unvisited = set((i, j) for i in range(rows * 2 + 1) for j in range(cols * 2 + 1))

    all_nodes = set()
    all_nodes.add((y,x))

    gif_arr = []
    util.start_cells(grid, y, x, random, all_nodes, unvisited)
    if gif:
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        gif_arr.append(maze)

    stop = grid.shape[0] * grid.shape[1] - (2 * grid.shape[0] + 2 * grid.shape[1])
    stop_arr = [0] * (stop_len - 1)
    stop_arr.append(1)
    
    count = 0

    while len(all_nodes) < stop and not check_stop(stop_arr) and count < evolutions:
        stop_arr.append(len(all_nodes))
        stop_arr.pop(0)
        changes = False
        for y in range(1, grid.shape[0] - 1):
            for x in range(1, grid.shape[1] - 1):
                if grid[y,x] == 0:
                    #cell is dead, check for birth
                    if util.checkRules(grid, (y,x), birthRule):
                        grid[y,x] = 255
                        changes = True
                        util.update_set(y, x, all_nodes, grid, unvisited)
                else:
                    #cell is alive, check for survival
                    if not util.checkRules(grid, (y,x), survivalRule):
                        grid[y,x] = 0
                        changes = True
                        util.update_set(y, x, all_nodes, grid, unvisited)
        count += 1
        if not changes:
            #jumpstart the grid by marking a random section of cells that havent been visited as alive
            selections = random.sample(unvisited, k=1)
            y, x = selections[0]
            util.start_cells(grid, y, x, random, all_nodes, unvisited)
        
        if gif:
            gif_arr.append(grid.copy())

    add_passage(grid, 1, 0)

    add_passage(grid, grid.shape[0] - 2, grid.shape[0] - 1)

    if gif:
        gif_arr.append(grid.copy())
        return gif_arr        
    return grid

def check_stop(stop_arr):
    elt = stop_arr[0]
    for i in stop_arr:
        if elt != i:
            return False
    return True

def add_passage(grid, y1, y2):
    passage_arr = []
    for i in range(grid.shape[1]):
        if grid[y1, i] == 255:
            passage_arr.append(i)
    x = random.randint(0, len(passage_arr) - 1)
    grid[y2, passage_arr[x]] = 255
    
def Maze(rows, cols, gif, evolutions, stop_len):
    return driver(rows, cols, gif, "12345", "3", evolutions, stop_len)

def Mazectric(rows, cols, gif, evolutions, stop_len):
    return driver(rows, cols, gif, "1234", "3", evolutions, stop_len)
    