import numpy as np
import random
import generator_utils as util

def driver(rows, cols, gif, survivalRule, birthRule, evolutions):
    grid = np.zeros((rows * 2 + 1, cols * 2 + 1), dtype=np.uint8)
    changes = True

    grid[0, random.randint(1, cols * 2 - 1)] = 255

    y = random.randint(2, rows * 2 - 1)
    x = random.randint(2, cols * 2 - 1)
    grid[y,x] = 255

    visited = set()
    visited.add((y,x))

    gif_arr = []
    util.start_cells(grid, y, x, random, visited)
    if gif:
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        gif_arr.append(maze)
        gif_arr.append(grid.copy())
    count = 0
    while count != evolutions:
        changes = False
        for y in range(1, grid.shape[0] - 1):
            for x in range(1, grid.shape[1] - 1):
                if grid[y,x] == 0:
                    #cell is dead, check for birth
                    if util.checkRules(grid, (y,x), birthRule):
                        grid[y,x] = 255
                        changes = True
                        visited.add((y,x))
                else:
                    #cell is alive, check for survival
                    if not util.checkRules(grid, (y,x), survivalRule):
                        grid[y,x] = 0
                        changes = True
        count += 1
        if not changes:
            y = random.randint(2, rows * 2 - 1)
            x = random.randint(2, cols * 2 - 1)
            iterations = 0
            while (grid[y, x] == 255 and util.check_visited(y, x, visited)) or iterations < evolutions:
                y = random.randint(2, rows * 2 - 1)
                x = random.randint(2, cols * 2 - 1)
                iterations+=1
            if iterations >= evolutions:
                break
            util.start_cells(grid, y, x, random)
        gif_arr.append(grid.copy())
    if gif:
        grid[rows * 2, random.randint(1, cols * 2)] = 255
        return gif_arr        
    return grid

def Maze(rows, cols, gif, evolutions):
    return driver(rows, cols, gif, "12345", "3", evolutions)


def Mazectric(rows, cols, gif, evolutions):
    return driver(rows, cols, gif, "12345", "3", evolutions)
    