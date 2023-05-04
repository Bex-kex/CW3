"""
RECURSIVE SOLVER MODULE
-----------------------
This module holds the SudokuBoard class used for solving the sudoku using a modified recursive search method,
according to Task 1 of the coursework.

Also holds the solve() function which acts as a wrapper for instantiating a SudokuBoard object and solving it.
"""


import numpy as np
from typing import Tuple

#type-hint macro.
sudokuboard = list[list[int]]

class SudokuBoard:
    """
    Main class for the board. Holds information such as the main grid, 
    information about its dimensions, and other lists formed as transformations of the original grid, such as
    column_list and square_list.
    also contains a hashmap for easily looking up an arbitraray location in the grid and getting 
    the index and position of the subgrid it belongs to.
    """
    def __init__(self,grid: sudokuboard,subgrid_dims_y: int,subgrid_dims_x: int,explain: bool,steps: list) -> None:
        """
        Constructor method. storing the grid, as well as pre-generating the list of columns, squares and 
        a hashmap for easy lookup of square locations.

        :param grid: the given grid
        :param subgrid_dims_y: the amount of rows per subgrid.
        :param subgrid_dims_x: the amount of columns per subgrid.
        :param explain: boolean argument whether to add an explanation to the solution.
        :return: None.

        """
        self.grid = grid
        self.subgrid_dims_y = subgrid_dims_y
        self.subgrid_dims_x = subgrid_dims_x
        self.main_grid_dims = self.subgrid_dims_y*self.subgrid_dims_x
        self.row_list, self.column_list = self.create_lists()
        self.square_list, self.hashmap = self.create_hashmap()
        self.explain = explain
        self.steps = steps

    def create_hashmap(self) -> Tuple[sudokuboard,list[list[str]]]:
        """
        This function loops through the unsolved grid and makes another nested list, 
        with each list containing all the elements in each sub-grid.
        It also makes a hashmap which is another nested list with the same dimensions as the sudoku board, and consists of strings in each location.
        basically is a look-up table. enter an arbitrary point in the grid and the string will correspond to the index the number is in the square list.
        for example:
            for a 3x3 grid, self.hashmap[0][5] is '12', which means the point 0,5 is mapped to square_list[1][2],
            or the 3rd element in the 2nd list inside self.square_list.
        
        :return: The square_list and hashmap.
        """
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
                        #adding offset to the anchor point to get to each element in the subgrid.
                        coord_y = anchor_point_y  + offset_y                        
                        coord_x = anchor_point_x  + offset_x                 
                        #adding element to each sub-list of squares
                        little_list.append(self.grid[coord_y][coord_x])

                        #adding the subgrid-coordinates to the lookup table.
                        lookup[coord_y][coord_x] = f'{list_number}{index_number}'
                        
                        index_number += 1

                square_list.append(little_list)
                #moving on to the next list.
                list_number += 1
                

        return (square_list,lookup)


    def create_lists(self) -> Tuple[sudokuboard,sudokuboard]:
        """
        Small function which handles creating the row_list and column_list.
        row_list is identical to the grid but still useful as a copy.
        column_list is a list where each column is in one row of the list,
        basically a transpose of the grid if it were a matrix.

        :return: Tuple containing row_list and column_list.
        """
        column_list = []
        for i in range(self.main_grid_dims):
                #creating column list
                column = []
                column.extend([j[i]for j in self.grid])
                column_list.append(column)

        row_list = self.grid

        return (row_list,column_list)


    def lookup_hashmap(self,y,x,return_list=False) -> list | Tuple[int,int]:
        """
        Function which looks up a co-ordinate on the grid and returns its index inside the square_list.
        this function needs to be created as the transform between the grid and square_list is complicated,
        not as simple as looking up a co ordinate in column_list.
        l
        :param y: the y co-ordinate of the point.
        :param x: the x co-ordinate of the point.
        :param return_list: boolean whether to return the exact co ordinate within the square list, \
        or just the entire square it belongs to.
        :return: either an entire list, or a tuple containing co-ordinates.
        """
        
        if return_list:
            # If return_list = True, instead of returning the co-ordinates inside the square_list, 
            # just return the entire sublist it belongs to.
            square_index = int(self.hashmap[y][x][0])
            return self.square_list[square_index]
        else:
            # Return the co ordinates of the given y and x values, 
            # translated into the square_list co ordinates through querying the hashmap.
            square_index = int(self.hashmap[y][x][0])
            position_in_square = int(self.hashmap[y][x][1])
            return (square_index, position_in_square)


    def get_possible_values(self,y: int,x: int) ->list[int]:
        """
        Function which examines the row, column and subgrid that a particular empty cell belongs to, 
        and returns a list of the possible values that can go in that cell.

        :param y: the y co ordinate of the empty cell.
        :param x: the x co ordinate of the empty cell.
        :return: list of all the possible values that can go in that cell.

        """
        # The expected set of numbers that should be in every row,column and square.
        # for a 3x3, looks like {1,2,3,4,5,6,7,8,9}
        expected_range = set([i for i in range(1,self.main_grid_dims+1)])
        
        
        row_set    = set(self.row_list[y]) # generate the set of values currently in the row
        col_set    = set(self.column_list[x]) # generate the set of values currently in the column
        square_set = set(self.lookup_hashmap(y,x,True)) # generate the set of values currently in the square.
        
        # return the difference of all of these sets in the form of a list.
        # the difference should be the numbers that are present in the expected range 
        # but are not yet present in the grid.
        return list(expected_range.difference(row_set,col_set,square_set))
        
    
    def get_next_zero(self) -> dict | None:
        """
        This function searches through the entire grid and looks for empty cells. When it finds an empty cell,
        it will generate the possible values that can go there and append this information as a dict to the list
        called 'zero_list'. After every empty cell has been visited, it will sort 'zero_list' by the amount of possibilities in each zero,
        therefore ordering the cells with the least amount of possibilities first.
        it doesnt need to return all of these empty zero's, just the one with the least of possibilities,
        so it returns the first zero in the sorted list.

        :return: dictionary relating to an empty space, containing its co ordinates and the list of possibilities it can be.
        """
        zero_list: list[dict] = []
        for y,i in enumerate(self.grid):
            for x,j in enumerate(i):
                #loop through whole grid.
                if j == 0:
                    # If it is an empty cell, make a new dictionary, 
                    # add its x & y values to it, and also generate the possible values it can be.
                    possibilities: list = self.get_possible_values(y,x)
                    # Add this dicionary to the zero list.
                    zero_list.append({'x':x,'y':y,'possibilities':possibilities})

        # If there are no empty spaces left, return None. 
        if len(zero_list) == 0:
            return None
        
        #sort by length of the list of each cells possible values.
        zero_list.sort(key=lambda a: len(a['possibilities']))
        
        # Return the first value in the list.
        return zero_list[0]


    def check_solution(self) -> True | False:
        """
        This function is used when the grid is fully filled in and checks whether the solution is valid or not.
        it will return either True or False.
        :return: boolean whether grid is correctly solved (True) or not (False).
        """
        # unlikely to be needed as the set comparison should be enough to tell if section is valid,
        # but just to be sure, checksum is an integer which is the correct sum of all the numbers in the grid.
        # if the sum of the filled in section is not the same as the checksum, the section is incorrect and the grid is incorrect.
        checksum: int = sum([i for i in range(1,self.main_grid_dims+1)])
        
        def check_section(sec):
            """
            micro-function for determining if a section (single list) is valid.
            makes sure the list contains all unique numbers and has the same sum as the checksum.
            """
            if len(set(sec)) == self.main_grid_dims and sum(sec) == checksum:
                return True
            else:
                return False
            
        #check each row section
        for i in self.row_list:
            if not check_section(i):
                return False
            
        #check each column section
        for j in self.column_list:
            if not check_section(j):
                return False
            
        #check each square section.    
        for k in self.square_list:
            if not check_section(k):
                return False
        return True

    def update_lists(self,y,x,value) -> None:
        """
        small function to update the other lists with a new value. 
        Needed, as these lists are used to determine the possibilities of other cells in the future.
        if the grids were never updated as the grid was filled in, the possible values might be invalid.
        :param y: y co-ordinate of the updated cell.
        :param x: x co-ordinate of the updated cell.
        :param value: the new value of the updated cell.
        """
        #update the row list with the new value
        self.row_list[y][x] = value

        #update the column list with the new value
        self.column_list[x][y] = value

        #update the square list with the new value
        y_sq, x_sq = self.lookup_hashmap(y,x)
        self.square_list[y_sq][x_sq] = value

    def recurse(self) -> sudokuboard:
        """
        main solver function. mostly unchanged from CW2.
        gets the position of a zero, fills it with one of its possible values, 
        then calls recurse() again, which will find the next zero and fill it.
        if there are no possible values for a zero, it means one of the previous choices was invalid,
        so it returns back to the previous recursion level and chooses a different value.
        keeps doing this until every cell is filled with a value, then it checks the grid, and returns the grid if it
        is valid.

        :return: Either the successfully solved grid or None.

        """
        
        # find the next zero, with the least amount of possibilities.
        next_zero = self.get_next_zero()
        
        #if there are no more zero's to fill, the grid is full, so check it.
        if not next_zero:
            #return the grid if the solution if valid.
            if self.check_solution():
                return self.grid
        
        #next_zero is a dictionary so unpack it for ease of use.
        x,y,possibilties = [next_zero[i] for i in next_zero.keys()]

        for i in possibilties:
            #replace the empty cell with one of the possible values.
            self.grid[y][x] = i

            #update the auxilary lists with this value.
            self.update_lists(y,x,i)
            
            if self.explain and self.steps is not None:
                #add an instruction to the explain list if explain == True.
                self.steps.append(f"Place value {i} in position {y, x}")
            
            #recursively call self to move on to the next square.
            ans = self.recurse()

            # this statement passes the completed grid back up the recursion stack to return the solution to solve.
            if ans:
                return ans
            #if this placement is invalid, remove the instruction from the explanation list, as it is a wrong instruction.
            if self.explain and self.steps is not None:
                self.steps.pop()

            # program will reach here if this value is not valid, so set the value back to zero and update the gridlists with zero, 
            # to make it ready to try another value
            self.grid[y][x] = 0
            self.update_lists(y,x,0)
        #if no possible values anymore, return None and go back to previous recursion level.
        return None

        
def solve(grid,n_sub_rows,n_sub_cols,explain=None,steps=None) -> sudokuboard:
    """
    Mainn and only function to be called outside of this file.
    solves the sudoku given, using the recursive mode, and returns the solution
    and/or the explanation.
    """
    #create SudokuBoard object
    board_to_solve = SudokuBoard(grid,n_sub_rows,n_sub_cols,explain,steps)
    #calling the actual solve method and storing the result as solution.
    solution = board_to_solve.recurse()
    
    if explain and steps is not None:
        #return both explanation and solved grid if explanation = True.
        return solution,board_to_solve.steps
    else:
        return solution,None



