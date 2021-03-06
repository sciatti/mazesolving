import generator_utils as util
import random
import numpy as np

import copy

class node:
    def __init__(self, walls_in):
        self.walls = walls_in

def chamber_divide(grid, start_row, end_row, start_col, end_col, gif, gif_arr):
    row_size = end_row - start_row
    col_size = end_col - start_col
    
    if(row_size <= 1 or col_size <= 1):
        return
    
    x = random.randint(0, row_size + col_size - 1)
    
    if x > row_size - 1:
        #Column wall will be placed
        col_pos = x - row_size + start_col
        
        wall_char = 'L'
        idx = 0
        
        if col_pos != start_col:
            #Create column-wall
            for r in range(start_row, end_row):
                grid[r][col_pos].walls[idx] = wall_char
                grid[r][col_pos - 1].walls[idx + 1] = 'R'
            
            #Select a random entrance
            entrance = random.randint(start_row, end_row - 1)
            grid[entrance][col_pos].walls[idx] = 'X'
        
            if gif:
                gif_arr.append(recDiv_create_snapshot(gif_arr[-1], start_row, end_row, False, col_pos, entrance))

        chamber_divide(grid, start_row, end_row, start_col, col_pos, gif, gif_arr)
        chamber_divide(grid, start_row, end_row, col_pos, end_col, gif, gif_arr)
        
    else:
        #Row wall will be placed
        row_pos = x + start_row
        
        idx = 2
        wall_char = 'T'
        
        if row_pos != start_row:
            #Create row-wall
            for c in range(start_col, end_col):
                grid[row_pos][c].walls[idx] = wall_char
                grid[row_pos - 1][c].walls[idx + 1] = 'B'
            
            #Select a random entrance
            entrance = random.randint(start_col, end_col - 1)
            grid[row_pos][entrance].walls[idx] = 'X'
        
            if gif:
                gif_arr.append(recDiv_create_snapshot(gif_arr[-1], start_col, end_col, True, row_pos, entrance))

        chamber_divide(grid, start_row, row_pos, start_col, end_col, gif, gif_arr)
        chamber_divide(grid, row_pos, end_row, start_col, end_col, gif, gif_arr)

def recursive_division(rows, cols, gif):
    grid = [[node(['X', 'X', 'X', 'X']) for j in range(cols)] for i in range(rows)]
    
    for r in range(rows):
        grid[r][0].walls[0] = 'L'
        grid[r][cols - 1].walls[1] = 'R'
    for c in range(cols):
        grid[0][c].walls[2] = 'T'
        grid[rows - 1][c].walls[3] = 'B'
    
    x = random.randint(0, cols - 1)
    grid[0][x].walls[2] = 'X'
    
    y = random.randint(0, cols - 1)
    grid[len(grid) - 1][y].walls[3] = 'X'
    
    gif_arr = []
    if gif:
        maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
        maze.fill(255)
        maze[0, :] = 0
        maze[rows*2, :] = 0
        maze[:, 0] = 0
        maze[:, cols * 2] = 0
        maze[0, x*2 + 1] = 255
        maze[rows * 2, y * 2 +1 ] = 255
        gif_arr.append(maze)
    
    chamber_divide(grid, 0, rows, 0, cols, gif, gif_arr)
        
    if gif:
        return gif_arr
    return grid

#Pass copy of previous grid as well as column / row to insert wall
def recDiv_create_snapshot(prev_grid, start, end, is_row, pos, entrance):
    start = 2*start + 1
    end = 2*end + 1
    pos = 2*pos
    entrance = 2*entrance + 1 
    
    grid = prev_grid.copy()
    if is_row:
        for c in range(start, end):
            grid[pos, c] = 0
        grid[pos, entrance] = 255
    else:
        for r in range(start, end):
            grid[r, pos] = 0
        grid[entrance, pos] = 255
    return grid
