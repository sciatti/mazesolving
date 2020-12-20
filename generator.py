"""Maze Generator Created By Salvatore Ciatti"""

from PIL import Image #allows the creation and deletion of images
import numpy as np
import argparse
import random
import time
import generator_utils as util
import random_dfs as r_dfs
import random_kruskal as r_krsk

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", default='DFS')
    parser.add_argument("-r", "--rows", default='4')
    parser.add_argument("-c", "--cols", default='4')
    parser.add_argument("-f", "--filename", default='maze.png')
    parser.add_argument("-u", "--upscale", action='store_true')
    parser.add_argument("-clr", "--colored", action='store_true')
    args = parser.parse_args()

    generate(args.method, int(args.rows), int(args.cols), args.filename, args.upscale, args.colored)

def generate(method, rows, cols, filename, upscale, colored):
    #random.seed()
    if method == 'DFS':
        grid = r_dfs.random_DFS(rows, cols)
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        create_image(maze, grid, filename, upscale, colored)
        #print(maze)
    if method == 'Kruskal':
        grid = r_krsk.random_kruskals(rows, cols)
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        create_image(maze, grid, filename, upscale, colored)

def squareRoutine(node, maze, index):
    for i in range(4):
        if node.walls[i] == 'X':
            mark_as_white = util.maze_index(index, i)
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

main()