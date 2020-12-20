import numpy as np

class disjoint_set:
    def __init__(self, numCells, row_size):
        self.rowSize = row_size
        self.numCells = numCells
        self.parents = np.full(self.numCells, -1)
    
    #Returns the highest ancestor index of cell passed to it and updates parents of things in set
    def find(self, cell_index):        
        if self.parents[cell_index] == -1:
            return self
        result = self.find(self.parents[cell_index])
        self.parents[cell_index] = result
        return result
    
    #returns True if items from distinct sets, false if the items were in the same set
    def union(self, cell_indexA, cell_indexB):
        ancestorA = self.find(cell_indexA)
        ancestorB = self.find(cell_indexB)
        if (ancestorA == ancestorB):
            return
        self.parents[ancestorB] = ancestorA
