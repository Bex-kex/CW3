import argparse

grid1 = [
    [1, 0, 4, 2],
    [4, 2, 1, 3],
    [2, 1, 3, 4],
    [3, 4, 2, 1]]

grid2 = [
    [1, 0, 4, 2],
    [4, 2, 1, 3],
    [2, 1, 0, 4],
    [3, 4, 2, 1]]

grid3 = [
    [1, 0, 4, 2],
    [4, 2, 1, 0],
    [2, 1, 0, 4],
    [0, 4, 2, 1]]

grid4 = [
    [1, 0, 4, 2],
    [0, 2, 1, 0],
    [2, 1, 0, 4],
    [0, 4, 2, 1]]

grid5 = [
    [1, 0, 0, 2],
    [0, 0, 1, 0],
    [0, 1, 0, 4],
    [0, 0, 0, 1]]

grid6 = [
    [0, 0, 6, 0, 0, 3],
    [5, 0, 0, 0, 0, 0],
    [0, 1, 3, 4, 0, 0],
    [0, 0, 0, 0, 0, 6],
    [0, 0, 1, 0, 0, 0],
    [0, 5, 0, 0, 6, 4]]
gridtest = [
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


def check_section(section, n):
    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True

    return False


def get_squares(grid, n_loc_rows:int, n_loc_cols:int, n_rows:int, n_cols:int):
    """
    this function takes the grid, dimensions of the subgrid, 
    and the dimensions of the main grid, and outputs a nested list, 
    containing the numbers in each square.
    
    """
    squares:list[list[int]] = []
    row_split = []
    col_split = []
    boundary = 0

    for i in range(n_loc_rows):

        row_split.append(boundary)
        boundary += n_rows // n_loc_rows
    boundary = 0
    for j in range(n_loc_cols):
        col_split.append(boundary)
        boundary += n_cols // n_loc_cols

    for row in row_split:
        for col in col_split:
            square = []
            for i in range(n_rows // n_loc_rows):
                for j in range(n_cols // n_loc_cols):
                    square.append(grid[row + i][col + j])
            squares.append(square)

    return squares


def check_solution(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
    n = n_loc_rows * n_loc_cols
    for row in grid:
        if not check_section(row, n):
            return False

    for i in range(n_rows):

        column = []
        for row in grid:
            column.append(row[i])

        if not check_section(column, n):
            return False

    squares = get_squares(grid, n_loc_rows, n_loc_cols, n_rows, n_cols)
    for square in squares:
        if not check_section(square, n):
            return False

    return True

def bubble_sort(any_list):
    length = len(any_list)
    for i in range(0, length):
        for j in range(0, length - i - 1):
            if any_list[j][2] > any_list[j + 1][2]:
                buffer = any_list[j]
                any_list[j] = any_list[j + 1]
                any_list[j + 1] = buffer

    return any_list

def find_empty(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
    zeros_outer = []
    zeros_inner = []
    for i in range(n_rows):
        for j in range(n_cols):
            if grid[i][j] == 0:
                zeros_inner.append(i)
                zeros_inner.append(j)
                zeros_outer.append(zeros_inner)
                zeros_inner = []

    for k in range(len(zeros_outer)):
        i = zeros_outer[k][0]
        j = zeros_outer[k][1]
        only_suitable = get_possible(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, i, j)
        zeros_outer[k].append(len(only_suitable))
        for m in only_suitable:
            zeros_outer[k].append(m)

    zeros_sorted = bubble_sort(zeros_outer)

    return zeros_sorted


def get_all(grid, n_loc_rows, n_loc_cols, i, j, n_rows, n_cols) -> set:
    """

    """
    row = []
    for k in range(n_cols):
        if grid[i][k] != 0:
            row.append(grid[i][k])

    col = []
    for k in range(n_rows):
        if grid[k][j] != 0:
            col.append(grid[k][j])

    row_split = []
    col_split = []
    boundary = 0

    for x in range(n_loc_rows):
        row_split.append(boundary)
        boundary += n_rows // n_loc_rows
    boundary = 0
    for y in range(n_loc_cols):
        col_split.append(boundary)
        boundary += n_cols // n_loc_cols

    for k in row_split:
        if i >= k:
            index = row_split.index(k)
    boundary_i = row_split[index]
    for k in row_split:
        if j >= k:
            index = row_split.index(k)
    boundary_j = row_split[index]

    square = []
    for i in range(n_rows // n_loc_rows):
        for j in range(n_cols // n_loc_cols):
            if grid[boundary_i + i][boundary_j + j] != 0:
                square.append(grid[boundary_i + i][boundary_j + j])

    all_present = row + col + square

    return set(all_present)


def get_possible(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, i, j) -> list[int]:
    all_possible = [i for i in range(1, n_rows + 1)]
    all_present = get_all(grid, n_loc_rows, n_loc_cols, i, j, n_rows, n_cols)
    only_suitable = list(set(all_possible) - set(all_present))

    return only_suitable


def recursive_solve(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
    """
    MAIN SOLVE FUNCTION 
    function that is called recursively. 
    It first checks if there is an empty space to put a number in,
    then it will replace that space with the first possible value, 
    then call itsself again to find the next zero.
    
    if there are no other possibilities available, it will exit with value of None,
    and go back to the previous zero and try other values.

    if the top level of recursion (i.e depth 0) returns none, it means that it has 
    been through every single possibility and there are no valid solutions to the sudoku.

    if the program does not find any zeros (sudoku completely filled), it will check the grid, and if valid it will
    return the grid back to the top of the recursion stack via {if ans: return ans}
    
    
    """
    #finding the next empty space, and the possibilities that it can be
    zeros = find_empty(grid, n_rows, n_cols, n_rows, n_cols)

    #if the grid is full already:
    if not zeros:
        if check_solution(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):# checks the grid 
            return grid
        #if the grid is full but not correct, it has failed and will return None back to the top.
        

    #define the coordinates of the zero
    row, col = zeros[0][0], zeros[0][1] 
    #create a list of possible digits that would be valid in that position
    possible_digits = [zeros[0][i] for i in range(3, len(zeros[0]))] 
    
    #loop through every possible digit and calls function again once it has swapped out the zero.
    for i in possible_digits:
        grid[row][col] = i
        
        ans = recursive_solve(grid, n_loc_rows, n_loc_cols, n_rows, n_cols)
        #this if statement is only true once the bottom of the recursion depth has been reached AND 
        #the grid is solved. basically just passes the grid back up the stack.
        if ans:
            return ans
        #if there were no solutions with the current choice of numbers, then reset the number back to zero,
        #and try again with a different value.
        grid[row][col] = 0
    
    return None


#print(recursive_solve(grid6, 3, 2, 6, 6))


def read_grid_from_file(file_name:str) -> list:
    """
    Function to read the grid from a text file    .

    """
    with open(file_name, 'r') as file:
        #formatting the raw text in order to extract just the numbers.
        grid = [[int(num) for num in line.strip().split(',')] for line in file]
    return grid


def print_grid(grid) -> None:
    """
    Function to print the grid to the terminal in a readable format.

    """
    for row in grid:
        print(" ".join(str(cell) for cell in row))

def write_grid_to_file(grid, file_name):
    """
    function for writing the solved (or partially solved) sudoku to the text file
    """
    with open(file_name, 'w') as file:
        for row in grid:
            file.write(" ".join(str(cell) for cell in row) + "\n")


print(recursive_solve(gridtest,3,3,9,9))
if __name__ == "__main__":
    """
    main function 
    """
    
    parser = argparse.ArgumentParser(description="Solve a Sudoku grid from a text file.")
    parser.add_argument('--file', help="The input Sudoku grid file.",nargs=2,action='extend')
    args = vars(parser.parse_args())
    print(args.get('file'))
    #try to open the file if the file argument is given:
    try:
        input_grid = read_grid_from_file(args.get('file')[0])
        n_rows = len(input_grid)
        n_cols = len(input_grid[0])
        n_loc_rows = n_loc_cols = int(n_rows ** 0.5)
        solution = recursive_solve(input_grid, n_loc_rows, n_loc_cols, n_rows, n_cols)
        if solution:
            #self explanatory, if the solve function returned the grid instead of None
            print("Solved Sudoku grid:")
            print_grid(solution)
            # Save the solution to a text file
            output_file_name: str = args.get('file')[1]
            write_grid_to_file(solution, output_file_name)
            print(f"Solution saved to file: {output_file_name}")
        else:
            print("The provided Sudoku grid has no solution.")
    except:
        #if there wasnt a file provided or the program could not find the file:
        print('improper file name given!')
    
    
    


    
