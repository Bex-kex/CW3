import copy

class SudokuBoard:
    '''
    Class for storing all sorts of info about the sudoku given, as well as methods for solving the sudoku.
    
    '''


    def __init__(self,grid) -> 'SudokuBoard':
        '''
        sets up everything, including finding the location of all the zeros, and separating the columns and the squares.
        '''
        self.grid = grid
        self.unsolved_grid = copy.deepcopy(self.grid)

        self.gridsize = len(grid)
        match self.gridsize:
            case 4:
                self.subgrid_rows = self.subgrid_cols = 2
            
            case 6:
                self.subgrid_rows = 3
                self.subgrid_cols = 2
            
            case 9:
                self.subgrid_rows = self.subgrid_cols = 3
    
        self.gridsize = self.subgrid_cols*self.subgrid_rows
        
        self.row_list,self.column_list = self.create_lists()
        self.subgrid_list,self.lookup_table = self.create_squarelist_and_lookup()
        self.list_of_zeros = self.create_zero_objects()


    def __repr__(self):
        '''
        overloads printing behaviour when it is in a list. A more powerful overload than __str__ for some reason.
        '''
        return str(self.grid)


    def create_zero_objects(self):
        '''
        creates a new SudokuNumber object for every number in the grid, passing the correct information for each one.
        returns a list containing all of the objects.
        '''
        list_of_zeros = []
        
        for index_y in range(self.gridsize):
            
            for index_x,j in enumerate(self.grid[index_y]):
                    if j == 0:
                        list_of_zeros.append(zero(self,index_y,index_x))
                    
            
        return list_of_zeros


    def create_lists(self):
        '''
        function called during __init__. This function creates separate lists of rows, columns and subgrids. 
        Subgrid list generation is outsourced to self.create_subgrid_list().

        '''
        column_list = []
        row_list = []

        for i in self.grid:
            #creating row list
            row_list.append(i)

        for i in range(self.gridsize):
            #creating column list
            column = []
            column.extend([j[i]for j in self.grid])
            column_list.append(column)

        #creating subgrid list    
        

        return row_list,column_list


    def create_squarelist_and_lookup(self) -> tuple[list, list]:
        """
        this function is called on creation of the board and generates the list of subgrids, 
        as well as a look-up table to allow the program to easily determine which subgrid a number is in by looking it up in the table.

        this function should work for all grid sizes.
        """
        
        #creating a list of zeros of the correct dimensions for the lookup table
        lookup = [0 for x in range(self.gridsize)]
        lookup_table_y = [lookup.copy() for y in range(self.gridsize)]
        lookup_table_x = [lookup.copy() for y in range(self.gridsize)]
        

        #define starting conditions
        square_list = []
        list_number = 0

        for anchor_point_y in range(0,self.gridsize,self.subgrid_cols):
            for anchor_point_x in range(0,self.gridsize,self.subgrid_rows):
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

                # for example, the co ordinate of the value located abose the '^' symbol can be written as (anchor_point_x + 2, anchor_point_y + 2)
                

                little_list = []
                index_number = 0
                for offset_y in range(0,self.subgrid_cols):
                    for offset_x in range(0,self.subgrid_rows):
                        
                        coord_y = anchor_point_y  + offset_y                        
                        coord_x = anchor_point_x  + offset_x                 
                        #adding element to each sub-list of squares
                        little_list.append(self.grid[coord_y][coord_x])
                        #changing the element of the lookup table from a 0 to whatever square number that co-ordinate will be in. explained below.
                        lookup_table_y[coord_y][coord_x] = list_number
                        lookup_table_x[coord_y][coord_x] = index_number
                        index_number += 1

                
                square_list.append(little_list)
                list_number += 1
        
        # at the end of the functions running, the look-up table in y dimension would look something like this:

        #    [0, 0, 0, 1, 1, 1, 2, 2, 2]
        #    [0, 0, 0, 1, 1, 1, 2, 2, 2]
        #    [0, 0, 0, 1, 1, 1, 2, 2, 2]
        #    [3, 3, 3, 4, 4, 4, 5, 5, 5]
        #    [3, 3, 3, 4, 4, 4, 5, 5, 5]
        #    [3, 3, 3, 4, 4, 4, 5, 5, 5]
        #  > [6, 6, 6, 7, 7, 7, 8, 8, 8]
        #    [6, 6, 6, 7, 7, 7, 8, 8, 8]
        #    [6, 6, 6, 7, 7, 7, 8, 8, 8]
        #                       ^
        # As you can see, if you queried any co-ordinate of the sudoku using this lookup table, 
        # you would get a value which corresponds to what subgrid list it is in.
        # for example, if I wanted to know which subgrid list the number at (row 6, column 6) was in, 
        # i would simply query the value at subgrid[6][6], which happens to be an 8. So then i could easily check subgrid[3] without any troubles.
        # the list lookup_table_x is used to exactly select the location of a value within a subgrid. on a 3x3 grid it will look something like this:
        
        #   [0, 1, 2, 0, 1, 2, 0, 1, 2]
        #   [3, 4, 5, 3, 4, 5, 3, 4, 5]
        #   [6, 7, 8, 6, 7, 8, 6, 7, 8]
        #   [0, 1, 2, 0, 1, 2, 0, 1, 2]
        #   [3, 4, 5, 3, 4, 5, 3, 4, 5]
        #   [6, 7, 8, 6, 7, 8, 6, 7, 8]
        # > [0, 1, 2, 0, 1, 2, 0, 1, 2]
        #   [3, 4, 5, 3, 4, 5, 3, 4, 5]
        #   [6, 7, 8, 6, 7, 8, 6, 7, 8]
        #                      ^
        #Again, if i queried the position of the number at (row 6, col 6) in lookup_table_x, i would get a 0, meaning that
        #the position of the number within the subgrid is a 0, i.e. the first item in the subgrid list.
        # with the two lookup tables, the number at row 6, col 6 is actually in position [8][0] in the self.subgrid_list list.
        # the lookup tables are constant so only need to be generated once, and they are queried every time the grids are updated.
        lookup_table = []
        for ind_y,i in enumerate(lookup_table_y):
            tmplist = []
            for ind_x,j in enumerate(i):
                tmplist.append(str(j)+':'+str(lookup_table_x[ind_y][ind_x]))
            lookup_table.append(tmplist)
        #for i in lookup_table:print(i)
        return square_list, lookup_table


    def query_lookup(self,**kwargs) -> list[int] | None:
        get_real_pos = get_index = False
        for i in kwargs.keys():
            if i == 'pos':
                get_real_pos = True
            elif i == 'x' or i == 'y':
                get_index = True
            else:
                raise 'invalid arguments. you messed it up!!!! >:('
        if get_real_pos:
            pos_str = kwargs.get('pos')
            for ind_y,i in enumerate(self.lookup_table):
                for ind_x,j in enumerate(i):
                    if pos_str == j:
                        return [ind_y,ind_x]
        if get_index:
            ind_y,ind_x = kwargs.get('y'),kwargs.get('x')
            self.lookup_table[ind_y][ind_x]: str
            coords_list = [int(i) for i in self.lookup_table[ind_y][ind_x].split(':')]
            return coords_list
            
                         
    def check_section(self,section) -> True | False:
        '''
        used for only checking if the relevant rows, columns and squares are solved,
        instead of checking the entire grid.
        '''
        if len(set(section)) == len(section) and sum(section) == sum([i for i in range(1,self.gridsize+1)]):
            return True
        return False


    def check_solution(self) -> True | False:
        for i in self.row_list:
            if not self.check_section(i):
                return False
        for j in self.column_list:
            if not self.check_section(j):
                return False
        for k in self.subgrid_list:
            if not self.check_section(k):
                return False
        return True


    def get_possible(self,y: int,x: int) -> list[int]:
            """
            this function will take a certain co ordinate of an empty cell, and return a list of values
            that the empty cell can take. returns a list of all the possibilities.
            """
            # create the base range of all allowed numbers, i.e. 1,2,3,4,5,6,7,8,9
            base_range = set([i for i in range(1,self.gridsize+1)])

            #get the set of all the numbers currently in the cells row,column and square
            row_set = set(self.row_list[y])
            col_set= set(self.column_list[x])
            square_set = set(self.subgrid_list[self.query_lookup(y=y,x=x)[0]])
            #find the set difference of all these 4 lists and return them as a list.
            #this list is all the numbers that could possibly be in the cell.
            all_possible = base_range.difference(row_set,col_set,square_set)
            return list(all_possible)


    def update_gridlists(self,y,x,i) -> None:
        """
        simple function to 
        """
        self.column_list[x][y] = i
        self.row_list[y][x] = i
        sq_y,sq_x = self.query_lookup(y=y,x=x)
        self.subgrid_list[sq_y][sq_x] = i
            
        
    def recursive_solve_wavefront(self) -> list[list[int]] | None:
        global depth
        
        try:
            #try to find the location of the next zero
            next_zero:zero = self.list_of_zeros[depth]
            

        except IndexError:
            #if the program couldnt find any more zeros
            if self.check_solution():
                return self.grid
        #get the x and y co ords of the zero
        coord_y,coord_x = next_zero.loc_y,next_zero.loc_x
        
            
            
        #find the possible values that it could be.
        possible_digits = self.get_possible(coord_y,coord_x)
        
        for i in possible_digits:
            #loop through all the possible values the zero can be, once it picks a value, call itsself on the next zero.
            self.grid[coord_y][coord_x] = i
            self.update_gridlists(coord_y,coord_x,i)
            next_zero.wave_propogate()
            
            
            depth += 1
            ans = self.recursive_solve_wavefront()
            if ans:
                return ans
            
            depth -= 1
            self.grid[coord_y][coord_x] = 0
            self.update_gridlists(coord_y,coord_x,0)
        
        return None


    def recursive_solve_normal(self) -> list[list[int]] | None:
        global depth
        
        try:
            #try to find the location of the next zero
            next_zero:zero = self.list_of_zeros[depth]

        except IndexError:
            #if the program couldnt find any more zeros
            if self.check_solution():
                return self.grid
        #get the x and y co ords of the zero
        coord_y,coord_x = next_zero.loc_y,next_zero.loc_x
        #find the possible values that it could be.
        possible_digits = self.get_possible(coord_y,coord_x)

        for i in possible_digits:
            #loop through all the possible values the zero can be, once it picks a value, call itsself on the next zero.
            self.grid[coord_y][coord_x] = i
            self.update_gridlists(coord_y,coord_x,i)
            
            depth += 1
            ans = self.recursive_solve_normal()
            if ans:
                return ans
            
            depth -= 1
            self.grid[coord_y][coord_x] = 0
            self.update_gridlists(coord_y,coord_x,0)
        
        return None

  
    def solve(self,wavefront_mode=True) -> list[list[int]]:
        """
        Wrapper function for the different recursive solve algorithms.

        """
        global depth
        if wavefront_mode:
            depth = 0
            return self.recursive_solve_wavefront()
        else:
            
            depth=0
            return self.recursive_solve_normal()
        
        
        





class zero():
    def __init__(self,parent,location_y,location_x):
        self.parent:SudokuBoard = parent
        self.loc_y = location_y
        self.loc_x = location_x
        self.changed = False
        #self.possibilities = self.parent.get_possible(self.loc_y,self.loc_x)

    def __repr__(self) -> str:
        return f'zero at {self.loc_y},{self.loc_x}'
    
    
    def find_your_brethren(self,y,x) -> 'zero':
        """
        function for finding the zero object that corresponds to a certain co ordinate.
        the most holy function.
        """
        brother:zero
        for brother in [i for i in self.parent.list_of_zeros if not self]:
            if (brother.loc_x,brother.loc_y) == (y,x):
                return brother
            
    def lookup(self,y,x): 
        ...
    def wave_propogate(self):
        """
        called when zero's value has changed.


        go through current square look for a single zero.
        """
        current_row =    self.parent.row_list[self.loc_y]
        current_column = self.parent.column_list[self.loc_x]
        current_square = self.parent.subgrid_list[self.parent.lookup_table_y[self.loc_y][self.loc_x]]
        if 0 in current_row and current_row.count(0) == 1:
            other_zero = self.find_your_brethren(self.loc_y,current_row.index(0))
            if not other_zero.changed:
                other_zero.changed = True
                other_zero.wave_propogate()
            #this means that there is only one other zero in its row
        if 0 in current_column and current_column.count(0) == 1:
            other_zero = self.find_your_brethren(current_column.index(0),self.loc_x)
            if not other_zero.changed:
                other_zero.changed = True
                other_zero.wave_propogate()
        if 0 in current_square and current_square.count(0) == 1:...
            #other_zero = self.find_your_brethren(self.loc_y,current_square.)
            #get the zero object that it is

        
        
        





if __name__ == '__main__':
    testlist = [
        [0, 0, 6, 0, 0, 3],
        [5, 0, 0, 0, 0, 0],
        [0, 1, 3, 4, 0, 0],
        [0, 0, 0, 0, 0, 6],
        [0, 0, 1, 0, 0, 0],
        [0, 5, 0, 0, 6, 4]
        ]
    testlist2 = [
        [9, 0, 6, 0, 0, 1, 0, 4, 0],
        [7, 0, 1, 2, 9, 0, 0, 6, 0],
        [4, 0, 2, 8, 0, 6, 3, 0, 0],
        [0, 0, 0, 0, 2, 0, 9, 8, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 9, 4, 0, 8, 0, 0, 0, 0],
        [0, 0, 3, 7, 0, 8, 4, 0, 9],
        [0, 4, 0, 0, 1, 3, 7, 0, 6],
        [0, 6, 0, 9, 0, 0, 1, 0, 8]
    ]
    testlist3 = [
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
    sudoku = SudokuBoard(testlist3)
    sudoku.query_lookup(pos='2.3',x=2,y=3)
    print(sudoku.solve(wavefront_mode=False))