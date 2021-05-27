import numpy as np
#TODO:
#1. create a streamlined and replicable gif creation set of functions in this file.
#2. implement these functions into the generation algorithms available.

def convert_2d(index, cols):
    return (index // cols, index % cols)

def bounds_check(index, rows, cols):
    if index[0] < 0 or index[0] > rows - 1:
        return True
    if index[1] < 0 or index[1] > cols - 1:
        return True
    return False

def neighborCheck(grid, curr, rows, cols):
    #order: Left, Right, Top, Down
    ops = [(0,-1), (0,1), (-1,0), (1,0)]
    #short for operations
    ret = []
    for i in range(4):
        #bounds checking
        x = curr.index[1] + ops[i][1]
        y = curr.index[0] + ops[i][0]
        if bounds_check((y,x), rows, cols):
            continue
        if grid[y][x].visited == False:
            if curr.walls[i] != 'X':
                ret.append(i)
    return ret

def nbr_index(index, dir):
    if dir == 'L':
        return (index[0], index[1] - 1)
    elif dir == 'R':
        return (index[0], index[1] + 1)
    elif dir == 'T':
        return (index[0] - 1, index[1])
    return (index[0] + 1, index[1])

def conv_nbr_wall(dir):
    if dir == 'L':
        return 1
    elif dir == 'R':
        return 0
    elif dir == 'T':
        return 2
    return 3

def conv_idx_dir(index, nbr_index):
    y = index[0] - nbr_index[0]
    x = index[1] - nbr_index[1]
    if x == 1:
        return 'R'
    if x == -1:
        return 'L'
    if y == 1:
        return 'T'
    if y == -1:
        return 'D'

def print_grid(grid):
    for i in range(len(grid)):
        print("[", end="")
        for j in range(len(grid[i])):
            print(grid[i][j].walls, end=", ")
        print("]")

def print_index(grid):
    for i in range(len(grid)):
        print("[", end="")
        for j in range(len(grid[i])):
            print(grid[i][j].index, end=", ")
        print("]")

def print_visited(grid):
    for i in range(len(grid)):
        print("[", end="")
        for j in range(len(grid[i])):
            if grid[i][j].visited == True:
                print('X', end=", ")
            else:
                print('O', end=", ")
        print("]")

def maze_index(index, dir):
    if dir == 0:
        return (index[0], index[1] - 1)
    elif dir == 1:
        return (index[0], index[1] + 1)
    elif dir == 2:
        return (index[0] - 1, index[1])
    return (index[0] + 1, index[1])

def create_snapshot(new_image, index, direction, color=None):
    # set marking color to 255 (white) if none provided
    if color == None:
        color = 255
    # assign the given color to the cell to mark it as active
    new_image[index[0], index[1]] = color
    if direction < 0:
        return new_image
    # find the index of the wall to break remove
    mark_as_white = maze_index(index, direction)
    # remove the wall (set it to the provided color)
    new_image[mark_as_white[0], mark_as_white[1]] = color
    return new_image

def grid_to_image(index):
    return (index[0] * 2 + 1, index[1] * 2 + 1)

def mark_change(idx, gif_arr, wall_idx, secondIdx = None, color = None):
    # mark one or two changes, algorithm specific 
    if secondIdx == None:
        newIMG = create_snapshot(gif_arr[-1].copy(), idx, wall_idx, color)
    else:
        newIMG = create_snapshot(gif_arr[-1].copy(), idx, wall_idx, color)
        newIMG = create_snapshot(newIMG, secondIdx, -1, color)
    if not np.array_equal(newIMG, gif_arr[-1]):
        gif_arr.append(newIMG)

def mark_node(idx, gif_arr, secondIdx = None, color = None):
    if secondIdx == None:
        newIMG = create_snapshot(gif_arr[-1].copy(), idx, -1, color)
    else:
        newIMG = create_snapshot(gif_arr[-1].copy(), idx, -1, color)
        newIMG = create_snapshot(newIMG, secondIdx, -1, color)
    if not np.array_equal(newIMG, gif_arr[-1]):
        gif_arr.append(newIMG)

def getNeighbor(grid, curr, rows, cols, previous):
    #order: Left, Right, Top, Down
    ops = [(0,-1), (0,1), (-1,0), (1,0)]
    #short for operations
    ret = []
    for i in range(4):
        #bounds checking
        x = curr.index[1] + ops[i][1]
        y = curr.index[0] + ops[i][0]
        if bounds_check((y,x), rows, cols) or (y,x) == previous.index:
            continue
        ret.append(grid[y][x])
    return ret

def print_maze(grid):
    maze = np.chararray((len(grid) * 2 + 1, len(grid[0]) * 2 + 1))
    maze[:,:] = '@'
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            for k in range(4):
                idx = maze_index((i * 2 + 1,j * 2 + 1), k)
                maze[i * 2 + 1, j * 2 + 1] = '+'
                if grid[i][j].walls[k] == 'X':
                    if k == 0 or k == 1:
                        maze[idx[0], idx[1]] = '-'
                    else:
                        maze[idx[0], idx[1]] = '|'
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            print(maze[i,j].decode('utf-8'), end=" ")
        print()

def countNeighbors(grid, index, rows, cols):
    #order: Left, Right, Top, Down, Top Left, Bottom Left, Top Right, Bottom Right
    ops = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (1,-1), (-1,1), (1,1)]
    #short for operations
    count = 0
    for i in range(8):
        #bounds checking
        x = index[1] + ops[i][1]
        y = index[0] + ops[i][0]
        if bounds_check((y,x), rows, cols):
            continue
        if grid[y,x] == 255:
            count += 1
    return count

def checkRules(grid, index, rule):
    c = countNeighbors(grid, index, grid.shape[0], grid.shape[1])    
    for character in rule:
        if c == int(character):
            return True
    return False

def start_cells(grid, y, x, random, visited, unvisited):
    ops = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (1,-1), (-1,1), (1,1)]
    dirs = random.sample(ops, k=len(ops))
    count = 0
    for index in dirs:
        if count == len(dirs):
            break
        if not bounds_check((y + index[0], x + index[1]), grid.shape[0], grid.shape[1]):
            if y + index[0] == 0 or grid.shape[0] - 1 == y + index[0] or x + index[1] == 0 or grid.shape[1] - 1 == x + index[1]:
                continue
            grid[y + index[0], x + index[1]] = 255
            visited.add((y + index[0], x + index[1]))
            update_set(y + index[0], x + index[1], visited, grid, unvisited)
            count += 1
    if count == 0:
        return False
    return True

def check_visited(y, x, visited):
    ops = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (1,-1), (-1,1), (1,1)]
    for index in ops:
        if (y + index[0], x + index[1]) in visited:
            return True
    return False
            
def update_set(y, x, all_nodes, grid, unvisited):
    ops = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (1,-1), (-1,1), (1,1)]
    for index in ops:
        if y + index[0] == 0 or grid.shape[0] - 1 == y + index[0] or x + index[1] == 0 or grid.shape[1] - 1 == x + index[1]:
            continue
        all_nodes.add((y,x))
        if (y,x) in unvisited:
            unvisited.remove((y,x))
        