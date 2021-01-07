import numpy as np
import random
import generator_utils as util

def driver(rows, cols, gif, survivalRule, birthRule, evolutions):
    random.seed(0)
    grid = np.zeros((rows * 2 + 1, cols * 2 + 1), dtype=np.uint8)
    changes = True

    grid[0, random.randint(1, cols * 2 - 1)] = 255

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
        gif_arr.append(grid.copy())
    count = 0
    stop = grid.shape[0] * grid.shape[1] - (2 * grid.shape[0] + 2 * grid.shape[1])
    stop_grid = [0] * 10
    while len(all_nodes) < stop:
        print(len(all_nodes))
        stop_grid.append(len(all_nodes))
        stop_grid.pop(0)
        if check_stop(stop_grid):
            break
        #print(visited)
        changes = False
        for y in range(1, grid.shape[0] - 1):
            for x in range(1, grid.shape[1] - 1):
                if grid[y,x] == 0:
                    #cell is dead, check for birth
                    if util.checkRules(grid, (y,x), birthRule):
                        grid[y,x] = 255
                        changes = True
                        util.update_set(y, x, all_nodes, grid, unvisited)
                        #visited.add((y,x))
                else:
                    #cell is alive, check for survival
                    if not util.checkRules(grid, (y,x), survivalRule):
                        grid[y,x] = 0
                        changes = True
                        util.update_set(y, x, all_nodes, grid, unvisited)
                        #visited.remove((y,x))
        count += 1
        if not changes:
            selections = random.sample(unvisited, k=1)
            iterations = 0
            y, x = selections[0]
            #while (grid[y,x] == 255 and util.check_visited(y, x, all_nodes)) and iterations < len(selections):
                #iterations+=1
                #y, x = selections[iterations]
            #if iterations >= len(selections):
                #break
            util.start_cells(grid, y, x, random, all_nodes, unvisited)
        gif_arr.append(grid.copy())
    if gif:
        grid[rows * 2, random.randint(1, cols * 2)] = 255
        return gif_arr        
    return grid

def check_stop(stop_grid):
    elt = stop_grid[0]
    for i in stop_grid:
        if elt != i:
            return False
    return True

def Maze(rows, cols, gif, evolutions):
    return driver(rows, cols, gif, "12345", "3", evolutions)


def Mazectric(rows, cols, gif, evolutions):
    return driver(rows, cols, gif, "1234", "3", evolutions)
    