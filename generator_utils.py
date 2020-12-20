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
        return 3
    return 2

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

def create_image(maze, grid, filename, upscale, colored):
    print(maze.shape)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            current_node = grid[i][j]
            squareRoutine(current_node, maze, ((2*i) + 1, (2*j) + 1))
    original = Image.fromarray(maze)
    img = Image.fromarray(maze)
    if upscale == True:
        img = img.resize((maze.shape[0] * 20, maze.shape[0] * 20), Image.NEAREST)
    img.save(filename)