"""Maze Generator Created By Salvatore Ciatti"""

from PIL import Image #allows the creation and deletion of images
from collections import deque
import numpy as np
import argparse
import random
import time

class node:
    visited = False
    def __init__(self, index_in, walls_in, visited_in):
        self.index = index_in
        self.walls = walls_in
        self.visited = visited_in

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", default='random DFS')
    parser.add_argument("-r", "--rows", default='4')
    parser.add_argument("-c", "--cols", default='4')
    parser.add_argument("-f", "--filename", default='maze.png')
    parser.add_argument("-u", "--upscale", action='store_true')
    parser.add_argument("-clr", "--colored", action='store_true')
    args = parser.parse_args()

    generate(args.method, int(args.rows), int(args.cols), args.filename, args.upscale, args.colored)

def generate(method, rows, cols, filename, upscale, colored):
    random.seed(1)
    if method == 'random DFS':
        grid = random_DFS(rows, cols)
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        create_image(maze, grid, filename, upscale, colored)

def maze_index(index, dir):
    if dir == 0:
        return (index[0], index[1] - 1)
    elif dir == 1:
        return (index[0], index[1] + 1)
    elif dir == 2:
        return (index[0] - 1, index[1])
    return (index[0] + 1, index[1])

def squareRoutine(node, maze, index):
    for i in range(4):
        if node.walls[i] == 'X':
            mark_as_white = maze_index(index, i)
            maze[mark_as_white[0], mark_as_white[1]] = 255
        maze[index[0], index[1]] = 255

def create_image(maze, grid, filename, upscale, colored):
    print(maze.shape)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            current_node = grid[i][j]
            squareRoutine(current_node, maze, ((2*i) + 1, (2*j) + 1))
    original = Image.fromarray(maze)
    if colored == True:
        tmp = []
        for i in range(0, 3):
            x = np.copy(maze)
            tmp.append(x.reshape(maze.shape[0], maze.shape[1], 1))
        maze = np.concatenate((tmp[0], tmp[1], tmp[2]), axis=2)
        for i in range(maze.shape[0]):
            for j in range(maze.shape[1]):
                if maze[i, j, 0] == 0:
                    for x in range(3):
                        #cascade from red to green
                        # if x == 0:
                        #     maze[i, j, x] = (i / maze.shape[0]) * 255
                        # if x == 1:
                        #     maze[i, j, x] = (j / maze.shape[1]) * 255
                        # else:
                        #     maze[i, j, x] = random.randint(0, 255)

                        #varying shades of red
                        # if x == 0:
                        #     maze[i, j, x] = i
                        # if x == 1:
                        #     maze[i, j, x] = j
                        # else:
                        #     maze[i, j, x] = random.randint(0, 255)

                        #cascade from black to green????
                        if x == 0:
                            maze[i, j, x] = (i / maze.shape[0]) * 255
                        if x == 1:
                            maze[i, j, x] = (j / maze.shape[1]) * 255
                        else:
                            maze[i, j, x] = (j + i) % 225
                        
                        #black to pink to green to white
                        # if x == 0:
                        #     maze[i, j, x] = (i / maze.shape[0]) * 255
                        # if x == 1:
                        #     maze[i, j, x] = (j / maze.shape[1]) * 255
                        # else:
                        #     maze[i, j, x] = (j / maze.shape[1] + i / maze.shape[0]) * 255
                        
                        #totally random color selection
                        #maze[i, j, x] = random.randint(0, 255)
        img = Image.fromarray(maze, 'RGB')
    else:
        img = Image.fromarray(maze)
    if upscale == True:
        img = img.resize((maze.shape[0] * 20, maze.shape[0] * 20), Image.NEAREST)
    img.save(filename)

def neighborCheck(grid, curr, rows, cols):
    #order: Left, Right, Top, Down
    ops = [(0,-1), (0,1), (-1,0), (1,0)]
    #short for operations
    ret = []
    for i in range(4):
        #bounds checking
        if curr.index[0] == 0:
            if i == 2:
                continue
        elif curr.index[0] == rows - 1:
            if i == 3:
                continue
        if curr.index[1] == 0:
            if i == 0:
                continue
        elif curr.index[1] == cols - 1:
            if i == 1:
                continue
        x = curr.index[1] + ops[i][1]
        y = curr.index[0] + ops[i][0]
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
    
def random_DFS(rows, cols):
    stack = deque()
    grid = [[node((i, j), ['L', 'R', 'T', 'B'], False) for j in range(cols)] for i in range(rows)]
    #1
    x = random.randint(0, cols - 1)
    grid[0][x].visited = True
    grid[0][x].walls[2] = 'X'
    stack.append(grid[0][x])
    #print("\nStack at the start:")
    #for i in stack:
        #print(i.index)    
    #2
    while len(stack) != 0:
        #print_grid(grid)
        #print_visited(grid)
        #print("\nStack:")
        #for i in stack:
            #print(i.index)
        #1
        curr = stack.pop()
        #2
        neighbors = neighborCheck(grid, curr, rows, cols)
        #print("neighbors: ", neighbors)
        #print("curr: ", curr.index)
        if len(neighbors) > 0:
            #1
            stack.append(curr)
            #2
            nbr_dir = neighbors[random.randint(0, len(neighbors) - 1)]
            #print("nbr_dir: ", nbr_dir)
            #print("curr.walls: ", curr.walls)
            new_index = nbr_index(curr.index, curr.walls[nbr_dir])
            #print("new_index: ", new_index)
            new_curr = grid[new_index[0]][new_index[1]]
            #3
            #print(nbr_dir)
            #print(conv_nbr_wall(curr.walls[nbr_dir]))
            curr.walls[nbr_dir] = 'X'
            #new_curr.walls[conv_nbr_wall(curr.walls[nbr_dir])] = 'X'
            #4
            new_curr.visited = True
            stack.append(new_curr)
    x = random.randint(0, cols - 1)
    grid[rows - 1][x].walls[3] = 'X'
    return grid

main()