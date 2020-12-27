
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
        if bounds_check((x,y), rows, cols):
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

def create_snapshot(previous_image, index, direction):
    previous_image[index[0], index[1]] = 255
    if direction < 0:
        return previous_image
    mark_as_white = maze_index(index, direction)
    previous_image[mark_as_white[0], mark_as_white[1]] = 255
    return previous_image
