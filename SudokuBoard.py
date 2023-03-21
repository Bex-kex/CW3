from typing import List
class SudokuBoard():
    def __init__(self,grid,n_rows,n_cols):
        
        self.dims_y = n_rows
        self.dims_x  = n_cols
        self.grid_size = self.dims_x*self.dims_y
        self.__object_list = self.create_number_objects(grid)
        self.expected_order = set([i+1 for i in range(self.grid_size)])
        
        self.row_list = self.__object_list
        self.column_list = self.create_column_list()
        
        self.square_list = self.create_square_list()
        self.generate_possibilities()
      
        
        
    def create_number_objects(self,grid: List[int]) -> List['SudokuNumber']:
        big_object_list = []
        for i in range(len(grid)):
            object_list = []
            for j in range(len(grid[i])):
                newitem = SudokuNumber(i,j,grid[i][j])
                
                object_list.append(newitem)
            big_object_list.append(object_list)
        return big_object_list
    def create_column_list(self) -> list:
        column_list = []
        for i in range(self.grid_size):
            column = []
            column.extend([j[i]for j in self.__object_list])
            column_list.append(column)
        return column_list



    def create_square_list(self) -> list:
        
        grid = []
        for x in range(self.dims_x):
            x = x * self.dims_y
            for y in range(self.dims_y):
                y = y* self.dims_x
                subgrid = []
                for i in range(self.dims_y):
                    for j in range(self.dims_x):
                        val = self.__object_list[x+i][y+j]
                        
                        subgrid.append(val)
                
                grid.append(subgrid)
        return grid
                
            

            




    def generate_possibilities(self) -> None:
        for a in self.__object_list:
            for number  in a:
                number: SudokuNumber
                if number.current_value == 0:
                    
                    row: List[SudokuNumber] = [i.current_value for i in self.__object_list[number.pos_y]]
                    col: List[SudokuNumber] = [i.current_value for i in self.column_list[number.pos_x]]
                    square: List[SudokuNumber] = [i.current_value for i in number.find_position(self.square_list)]

                    if number.find_possible_values(row,col,square,self.expected_order):
                        self.generate_possibilities()
        print(self.__object_list)


class SudokuNumber():
    def __init__(self,pos_y,pos_x,current_value):
        self.pos_y = pos_y
        self.pos_x = pos_x
        
        self.current_value = current_value
        self.available_values: List[int]
    
    def find_position(self,square_list) -> int:
        for i in square_list:
            if self in i:
                return i
    def find_possible_values(self,row,col,square,expected_order:set):
        changed: bool
        for i in (row,col,square):
            difference = expected_order.difference(i)
            if len(difference) == 1:
                self.current_value = difference.pop()
                print(self.current_value)
                changed = True
                return changed
            else:
                self.available_values = list(difference)
    def __repr__(self) -> str:
        return str(self.current_value)



grid5 = [
		[1, 0, 0, 2],
		[0, 0, 1, 0],
		[0, 1, 0, 4],
		[0, 0, 0, 1]]
grid7 = [
		[6, 1, 9, 8, 4, 2, 5, 3, 7,],
		[7, 4, 5, 3, 6, 9, 1, 8, 2,],
		[8, 3, 2, 1, 7, 5, 4, 6, 9,],
		[1, 5, 8, 6, 9, 7, 3, 2, 4,],
		[9, 6, 4, 2, 3, 1, 8, 7, 5,],
		[2, 7, 3, 5, 8, 4, 6, 9, 1,],
		[4, 8, 7, 9, 5, 6, 2, 1, 3,],
		[3, 9, 1, 4, 2, 8, 7, 5, 6,],
		[5, 2, 6, 7, 1, 3, 9, 4, 8,]]
grid10 = [
		[1, 2, 6, 5, 4, 3],
		[5, 3, 4, 6, 2, 1],
		[6, 1, 3, 4, 5, 2],
		[2, 4, 5, 3, 1, 6],
		[4, 6, 1, 2, 3, 5],
		[3, 5, 2, 1, 6, 4]]




if __name__ == '__main__':
    x = SudokuBoard(grid5,2,2)
    