import numpy as np
from typing import Tuple


sudokuboard = list[list[int]]
class SudokuBoard:
    def __init__(self,grid,subgrid_dims_y,subgrid_dims_x):
        self.grid = grid
        self.subgrid_dims_y = subgrid_dims_y
        self.subgrid_dims_x = subgrid_dims_x
        self.main_grid_dims = self.subgrid_dims_y*self.subgrid_dims_x
        self.row_list, self.column_list = self.create_lists()
        self.square_list, self.hashmap = self.create_hashmap()
    def create_hashmap(self) -> Tuple[sudokuboard,list[list[str]]]:
        
        #creating a grid of zeros of same size as the grid
        lookup = [0 for x in range(self.main_grid_dims)]
        lookup = [lookup.copy() for y in range(self.main_grid_dims)]
        
        square_list = []
        list_number = 0

        for anchor_point_y in range(0,self.main_grid_dims,self.subgrid_dims_y):
            for anchor_point_x in range(0,self.main_grid_dims,self.subgrid_dims_x):
                # The two loops above determine the 'anchor point' for each subgrid, i.e. the top left element of each subgrid. 
                # The two loops below add an 'offset' to this anchor point in order to get the other elements in each subgrid.
                # The diagram below should help:

                #       +0 +1 +2
                #    +0 [x, o, o]           x: anchor point
                #    +1 [o, o, o]           ^: any arbitrary point
                #    +2 [0, 0, 0]
                #              ^ 
                # Where x is the anchor point for each subgrid, every other value in the subgrid(the 'o's) can be accessed by using
                # the co-ordinate of the anchor point + the offset in both x and y dimensions.

                
                

                little_list = []
                index_number = 0
                for offset_y in range(0,self.subgrid_dims_y):
                    for offset_x in range(0,self.subgrid_dims_x):
                        
                        coord_y = anchor_point_y  + offset_y                        
                        coord_x = anchor_point_x  + offset_x                 
                        #adding element to each sub-list of squares
                        little_list.append(self.grid[coord_y][coord_x])
                        
                        lookup[coord_y][coord_x] = f'{list_number}{index_number}'
                        
                        index_number += 1

                
                square_list.append(little_list)
                list_number += 1
        return (square_list,lookup)


    def create_lists(self) -> Tuple[sudokuboard,sudokuboard]:
        column_list = []
        for i in range(self.main_grid_dims):
                #creating column list
                column = []
                column.extend([j[i]for j in self.grid])
                column_list.append(column)

        row_list = self.grid

        return (row_list,column_list)


    def lookup_hashmap(self,y,x,return_list=False) -> list:
        
        if return_list:
            square_index = int(self.hashmap[y][x][0])
            return self.square_list[square_index]
        else:
            square_index = int(self.hashmap[y][x][0])
            position_in_square = int(self.hashmap[y][x][1])
            return (square_index, position_in_square)


    def get_possible_values(self,y: int,x: int) ->list[int]:
        expected_range = set([i for i in range(1,self.main_grid_dims+1)])
        
        
        row_set    = set(self.row_list[y])
        col_set    = set(self.column_list[x])
        square_set = set(self.lookup_hashmap(y,x,True))
        
        return list(expected_range.difference(row_set,col_set,square_set))
        
    
    def get_next_zero(self):
        zero_list: list[dict] = []
        for y,i in enumerate(self.grid):
            for x,j in enumerate(i):
                if j == 0:
                    possibilities: list = self.get_possible_values(y,x)
                    zero_list.append({'x':x,'y':y,'possibilities':possibilities})
        if len(zero_list) == 0:
            return None
        def amount_of_possibilities(zerodict: dict) -> int:
            return len(zerodict['possibilities'])
        

            
        zero_list.sort(key=amount_of_possibilities)
        return zero_list[0]


    def check_solution(self):
        checksum = sum([i for i in range(1,self.main_grid_dims+1)])

        def check_section(sec):
            if len(set(sec)) == self.main_grid_dims and sum(sec) == checksum:
                return True
            else:
                return False
            
        for i in self.row_list:
            if not check_section(i):
                return False
        for j in self.column_list:
            if not check_section(j):
                return False
        for k in self.square_list:
            if not check_section(k):
                return False
        return True

    def update_lists(self,y,x,value):
        self.row_list[y][x] = value
        self.column_list[x][y] = value
        y_sq, x_sq = self.lookup_hashmap(y,x)
        self.square_list[y_sq][x_sq] = value

    def solve(self) -> sudokuboard:
        next_zero = self.get_next_zero()
        
        
        if not next_zero:
            if self.check_solution():
                return self.grid
        x,y,possibilties = [next_zero[i] for i in next_zero.keys()]
        for i in possibilties:
            self.grid[y][x] = i
            self.update_lists(y,x,i)

            ans = self.solve()
            if ans:
                return ans
            
            self.grid[y][x] = 0
            self.update_lists(y,x,0)
        
        return None

        
    



if __name__ == '__main__':
    testlist6x6 = [
    [0, 3, 0, 4, 0, 0],
    [0, 0, 5, 6, 0, 3],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 3, 0, 5],
    [0, 6, 4, 0, 3, 1],
    [0, 0, 1, 0, 4, 6]
    ]
    
    testlist9x9 = [
    [0, 2, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 6, 0, 4, 0, 0, 0, 0],
    [5, 8, 0, 0, 9, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 3, 0, 0, 4],
    [4, 1, 0, 0, 8, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 9, 5],
    [2, 0, 0, 0, 1, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 1, 0, 0, 8, 0, 5, 7]
    ]
    board = SudokuBoard(testlist9x9,3,3)
    solution = board.solve()
    for i in solution:print(i)