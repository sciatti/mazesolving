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

def create_snapshot(new_image, index, direction, color):
    if color == None:
        color = 255
    new_image[index[0], index[1]] = color
    if direction < 0:
        return new_image
    mark_as_white = maze_index(index, direction)
    new_image[mark_as_white[0], mark_as_white[1]] = color
    return new_image

def grid_to_image(index):
    return (index[0] * 2 + 1, index[1] * 2 + 1)

def mark_change(idx, gif_arr, wall_idx, secondIdx = None, color = None):
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

def squareRoutine(node, maze, index):
    for i in range(4):
        if node.walls[i] != 'X':
            mark_as_white = maze_index(index, i)
            maze[mark_as_white[0], mark_as_white[1]] = 0
        maze[index[0], index[1]] = 0

def create_image(maze, grid, save=False):
    #print(maze.shape)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            current_node = grid[i][j]
            squareRoutine(current_node, maze, ((2*i) + 1, (2*j) + 1))
    from PIL import Image
    img = Image.fromarray(maze)
    if save:
        img = img.resize((maze.shape[0] * 20, maze.shape[0] * 20), Image.NEAREST)
        img.save("rec_div_output.png")
        
    else:
        return img

def create_gif(gif_arr, filename, upscale, duration):
    img_arr = []
    print(len(gif_arr), "images required for this gif")
    from PIL import Image
    print('---------------------------')
    for grid in gif_arr:
        print_maze(grid)
        print()
        maze = np.zeros((2*len(grid) + 1, 2*len(grid[0]) + 1))
        
        maze.fill(255)
        
        x = create_image(maze, grid)
        
        if upscale != '1':
            x = x.resize((x.size[0] * int(upscale), x.size[0] * int(upscale)), Image.NEAREST)
        img_arr.append(x)
    duration = (int(duration) * 1000)/len(gif_arr)
    img = img_arr[0]
    duration_arr = [max(int(duration), 20)] * (len(gif_arr) - 1)
    duration_arr.append(2000)
    img.save(filename, save_all=True, append_images=img_arr[1:], loop=0, duration=duration_arr, optimize=True)
