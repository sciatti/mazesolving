import random
import generator_utils as util
import numpy as np

class cell:
    def __init__(self, row, col):
        self.location = (row, col)
    
    def __eq__(self, other):
        return self.location == other.location

class wall:
    def __init__(cell_1, cell_2):
        separate = (cell_1, cell_2)

class node:
    def __init__(self, walls_in):
        self.walls = walls_in

def random_kruskals(rows, cols):
    #1
    wall_arr = []
    for i in range(rows):
        for j in range(cols):
            for direction in ['L', 'R', 'T', 'D']:
                wall_arr.append([(i,j), util.nbr_index((i,j), direction)])
    cells = [[{(i,j)} for j in range(cols)] for i in range(rows)]
    
    #[row][col]
    #for testing purposes set the seed to 0
    random.seed(0)
    #TODO: delete the previous line when done testing
    sequence = random.sample(range(rows*cols*4), cols*rows*4)
    #2
    count = 0
    for i in sequence:
        index = util.convert_2d(i // 4, cols)
        wall_num = i % 4
        div_cell = util.nbr_index(index, wall_arr[index[0]][index[1]].walls[wall_num])
        if util.bounds_check(div_cell, rows, cols):
            continue
        #1
        if cells[index[0]][index[1]].intersection(cells[div_cell[0]][div_cell[1]]) == set():
            #1
            #nbr_wall_num = conv_nbr_wall(wall_arr[index[0]][index[1]].walls[wall_num])
            wall_arr[index[0]][index[1]].walls[wall_num] = 'X'
            #wall_arr[div_cell[0]][div_cell[1]].walls[nbr_wall_num] = 'X'
            #2
            cells[index[0]][index[1]] = cells[index[0]][index[1]].union(cells[div_cell[0]][div_cell[1]])
            #cells[div_cell[0]][div_cell[1]] = cells[index[0]][index[1]]
            cells[div_cell[0]][div_cell[1]] = cells[div_cell[0]][div_cell[1]].union(cells[index[0]][index[1]])
            
            maze = np.zeros(((2 * rows) + 1, (2 * cols) + 1), dtype=np.uint8)
            util.create_image(maze, wall_arr, 'SNAPSHOT'+str(count)+'.png', True, False)
            count+=1
        print(cells)
        #print_grid(wall_arr)
        print()
    print(cells)
    x = random.randint(0, cols - 1)
    wall_arr[rows - 1][x].walls[3] = 'X'
    return wall_arr