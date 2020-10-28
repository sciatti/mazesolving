"""Maze Generator Created By Salvatore Ciatti"""

#layout:
#   1. take input arguments from the user
#   2. check input arguments
#   3. return if invalid
#   4. execute generation of Maze
#   
#   generation of maze:
#   5. create your data structures and classes, use basic arguments to generate the maze, then write the image
#   6. We will be making our implementation of the maze 

from PIL import Image #allows the creation and deletion of images
from collections import deque
import numpy as np
import argparse
import random
import time
#example image: img = Image.fromarray(data, 'RGB')

class node:
    visited = False
    walls = ['L', 'R', 'T', 'B']
    index = None
    def node(self, index_in):
        index = index_in

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", default='random DFS')
    parser.add_argument("-r", "--rows", default='10')
    parser.add_argument("-c", "--cols", default='10')
    parser.add_argument("-f", "--filename")
    args = parser.parse_args()
    generate(args.method, args.rows, args.cols, args.filename)

def generate(method, rows, cols, filename):
    print("implement")
    if method == 'random DFS':
        grid = random_DFS(rows, cols)

    maze = np.zeros((rows, cols, 3))

def neighborCheck(grid, curr):
    #order: Left, Right, Top, Down
    ops = [(0,-1), (0,1), (1,0), (-1,0)]
    #short for operations
    ret = []
    for i in range(4):
        #bounds checking
        if curr.index[0] == 0:
            if i == 3:
                continue
        elif curr.index[0] == len(grid) - 1:
            if i == 2:
                continue
        elif curr.index[1] == 0:
            if i == 0:
                continue
        elif curr.index[1] == len(grid[0])):
            if i == 1:
                continue
        x = curr.index[0] + ops[i][0]
        y = curr.index[1] + ops[i][1]
        if grid[x][y].visited == False:
            ret.append((x, y))
    if len(ret) == 0:
        return False, ret
    return True, ret

def random_DFS(rows, cols):
    stack = deque()
    grid = []
    for i in len(rows):
        grid.append([])
        for j in len(cols):
            grid[i].append(node((i, j)))
    random.seed(time.time())
    y = random.randint(0, cols - 1)
    x = random.randint(0, rows - 1)

    grid[x][y].visited = True
    stack.append(grid[x][y])
    
    while stack:
        curr = stack.top()
        curr_index = curr.index
        push, neighbors = neighborCheck(grid, curr)
        if push == True:
            randNbr = random.randint(0, len(neighbors))
            stack.append(curr)

            
        random.randint(0, 3)



main()