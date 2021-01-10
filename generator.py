"""Maze Generator Created By Salvatore Ciatti and Andrew Chen"""

from PIL import Image #allows the creation and deletion of images
import numpy as np
import argparse
import random
import time
import generator_utils as util
from random_dfs import random_DFS
from random_kruskal import random_kruskals
from random_prims import simplified_random_prims
from prims_test import random_prims
from wilsons import wilsons
from Aldous_Broder import aldousBroder
from recursive_div import recursive_division
from binary import binary_tree_maze
from cellular_automata import Maze
from cellular_automata import Mazectric
from sidewinder import sidewinder
#TODO: delete when done
import profiler
import tracemalloc

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", default='DFS')
    parser.add_argument("-r", "--rows", default='4')
    parser.add_argument("-c", "--cols", default='4')
    parser.add_argument("-f", "--filename", default='maze.png')
    parser.add_argument("-u", "--upscale", default='1')
    parser.add_argument("-clr", "--colored", action='store_true')
    parser.add_argument("-g", "--gif", action='store_true')
    parser.add_argument("-gd", "--gifDuration", default='60')
    parser.add_argument("-lm", "--lowMemory", action='store_true')
    parser.add_argument("-ev", "--evolutions", default='250')
    parser.add_argument("-sl", "--stopLength", default='10')
    parser.add_argument("-at", "--automataType", default='Maze')
    args = parser.parse_args()

    generate(args.method, int(args.rows), int(args.cols), args.filename, args.upscale, args.colored, args.gif, args.gifDuration, args.lowMemory, args.evolutions, args.stopLength, args.automataType)

def generate(method, rows, cols, filename, upscale, colored, gif, duration, lowMemory, evolutions, stopLength, automataType):
    #random.seed(0)
    import time
    start = time.time()
    grid = None
    method = method.lower()
    if method == 'dfs':
        grid = random_DFS(rows, cols, gif)
    if method == 'kruskal':
        grid = random_kruskals(rows, cols, gif)
    if method == 'prims':
        grid = random_prims(rows, cols, gif)
    if method == 'simpleprims':
        grid = simplified_random_prims(rows, cols, gif)
    if method == 'wilson':
        grid = wilsons(rows, cols, gif)
    if method == 'aldous':
        grid = aldousBroder(rows, cols, gif)
    if method == 'recursive':
        grid = recursive_division(rows, cols, gif)
    if method == 'binary':
        grid = binary_tree_maze(rows, cols, gif)
    if method == 'cellular':
        if automataType == 'Maze':
            grid = Maze(rows, cols, gif, int(evolutions), int(stopLength))
        else:
            grid = Mazectric(rows, cols, gif, int(evolutions), int(stopLength))
    if method == 'sidewinder':
        grid = sidewinder(rows, cols, gif)
    tracemalloc.start()    
    if gif:
        if filename == "maze.png":
            filename = "maze.gif"
        create_gif(grid, filename, upscale, duration, lowMemory)
    else:
        if method == 'cellular':
            create_image(np.zeros((0,0)), grid, filename, upscale, colored)
        else:
            maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
            create_image(maze, grid, filename, upscale, colored)
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        create_image(maze, grid, filename, upscale, colored)

    print("Time to execute: ", time.time() - start)
    snapshot = tracemalloc.take_snapshot()
    profiler.display_top(snapshot)

def squareRoutine(node, maze, index):
    for i in range(4):
        if node.walls[i] == 'X':
            mark_as_white = util.maze_index(index, i)
            maze[mark_as_white[0], mark_as_white[1]] = 255
        maze[index[0], index[1]] = 255

def create_image(maze, grid, filename, upscale, colored):
    #print(maze.shape)
    if maze.shape != (0,0):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                current_node = grid[i][j]
                squareRoutine(current_node, maze, ((2*i) + 1, (2*j) + 1))
    else:
        maze = grid
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
    if upscale != '1':
        img = img.resize((maze.shape[0] * int(upscale), maze.shape[0] * int(upscale)), Image.NEAREST)
    img.save(filename)

def create_gif(gif_arr, filename, upscale, duration, low_mem):
    img_arr = []
    print(len(gif_arr), "images required for this gif")
    if not low_mem:
        for img in gif_arr:
            x = Image.fromarray(img)
            if upscale != '1':
                x = x.resize((x.size[0] * int(upscale), x.size[0] * int(upscale)), Image.NEAREST)
            img_arr.append(x)
        duration = (int(duration) * 1000)/len(img_arr)
        img = img_arr[0]
        duration_arr = [max(int(duration), 20)] * (len(img_arr) - 1)
        duration_arr.append(2000)
        img.save(filename, save_all=True, append_images=img_arr[1:], loop=0, duration=duration_arr, optimize=True)
    else:
        img = Image.fromarray(gif_arr[0])
        if upscale != '1':
            img = img.resize((img.size[0] * int(upscale), img.size[0] * int(upscale)), Image.NEAREST)
        img.save(filename)
        count = 0
        while count != len(gif_arr):
            img = Image.open(filename)
            if count + 100 < len(gif_arr):
                end = count + 100
            else:
                end = len(gif_arr)
            for i in range(count, end):
                x = Image.fromarray(gif_arr[i])
                if upscale != '1':
                    x = x.resize((x.size[0] * int(upscale), x.size[0] * int(upscale)), Image.NEAREST)
                img_arr.append(x)
            count = end
            img.save(filename, save_all=True, append_images=img_arr[:], loop=0, duration=(int(duration) * 1000 / len(img_arr))/len(gif_arr), optimize=True)

main()