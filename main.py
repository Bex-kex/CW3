import time
import argparse
from copy import deepcopy
import Profiler

easy1 = [
    [9, 0, 6, 0, 0, 1, 0, 4, 0],
    [7, 0, 1, 2, 9, 0, 0, 6, 0],
    [4, 0, 2, 8, 0, 6, 3, 0, 0],
    [0, 0, 0, 0, 2, 0, 9, 8, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 9, 4, 0, 8, 0, 0, 0, 0],
    [0, 0, 3, 7, 0, 8, 4, 0, 9],
    [0, 4, 0, 0, 1, 3, 7, 0, 6],
    [0, 6, 0, 9, 0, 0, 1, 0, 8]]

easy2 = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]]

easy3 = [
    [0, 3, 0, 4, 0, 0],
    [0, 0, 5, 6, 0, 3],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 3, 0, 5],
    [0, 6, 4, 0, 3, 1],
    [0, 0, 1, 0, 4, 6]]

hard1 = [
    [0, 2, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 6, 0, 4, 0, 0, 0, 0],
    [5, 8, 0, 0, 9, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 3, 0, 0, 4],
    [4, 1, 0, 0, 8, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 9, 5],
    [2, 0, 0, 0, 1, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 1, 0, 0, 8, 0, 5, 7]]

med1 = [
    [0, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 0, 1],
    [3, 6, 9, 0, 8, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 6, 8, 0, 0],
    [0, 0, 0, 1, 3, 0, 0, 0, 9],
    [4, 0, 5, 0, 0, 9, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 0, 6, 0, 0, 7, 0, 0, 0],
    [1, 0, 0, 3, 4, 0, 0, 0, 0]]

med2 = [
    [8, 0, 9, 0, 2, 0, 3, 0, 0],
    [0, 3, 7, 0, 6, 0, 5, 0, 0],
    [0, 0, 0, 4, 0, 9, 7, 0, 0],
    [0, 0, 2, 9, 0, 1, 0, 6, 0],
    [1, 0, 0, 3, 0, 6, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 3],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [5, 0, 0, 0, 0, 0, 0, 1, 4],
    [0, 0, 0, 2, 8, 4, 6, 0, 5]]


def check_section(section, n) -> bool:
    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True

    return False


def split_into_squares(sub_grid, n):
    split = []
    boundary = 0
    for i in range(sub_grid):
        split.append(boundary)
        boundary += n // sub_grid

    return split


def get_squares(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
    squares = []

    row_split = split_into_squares(n_loc_rows, n_rows)
    col_split = split_into_squares(n_loc_cols, n_cols)

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


def bubble_sort(any_list) -> list[int]:
    length = len(any_list)
    for i in range(0, length):
        for j in range(0, length - i - 1):
            if any_list[j][2] > any_list[j + 1][2]:
                buffer = any_list[j]
                any_list[j] = any_list[j + 1]
                any_list[j + 1] = buffer

    return any_list


def find_empty(grid, n_loc_rows, n_loc_cols, n_rows, n_cols) -> list[int]:
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
    for k in col_split:
        if j >= k:
            index = col_split.index(k)
    boundary_j = col_split[index]

    square = []
    for q in range(n_rows // n_loc_rows):
        for w in range(n_cols // n_loc_cols):
            if grid[boundary_i + q][boundary_j + w] != 0:
                square.append(grid[boundary_i + q][boundary_j + w])

    all_present = row + col + square

    return set(all_present)


def get_possible(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, i, j) -> list[int]:
    all_possible = [i for i in range(1, n_rows + 1)]
    all_present = get_all(grid, n_loc_rows, n_loc_cols, i, j, n_rows, n_cols)
    only_suitable = list(set(all_possible) - set(all_present))

    return only_suitable


def recursive_solve(grid, n_loc_rows, n_loc_cols,\
        n_rows, n_cols, explain=False, steps=None) -> list[list[int]] | None:
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

    if the find_empty() function does not find any zeros (sudoku completely filled), it will check the grid, and if valid it will
    return the grid back to the top of the recursion stack via {if ans: return ans}
    
    
    """
    #finding the next empty space, and the possibilities that it can be
    zeros = find_empty(grid, n_loc_rows, n_loc_cols, n_rows, n_cols)

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
        
        if explain and steps is not None:
            steps.append(f"Place value {i} in position {row,col}")

        ans = recursive_solve(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, explain, steps)
        #this if statement is only true once the bottom of the recursion depth has been reached AND 
        #the grid is solved. basically just passes the grid back up the stack.
        if ans:
            return ans
        #if there were no solutions with the current choice of numbers, then reset the number back to zero,
        #and try again with a different value.
        if explain and steps is not None:
            steps.pop()

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
        
    n_rows = len(grid)
    n_cols = len(grid[0])
    if n_rows == 9:
        n_loc_rows = n_loc_cols = int(n_rows ** 0.5)
    else:
        n_loc_rows = 3
        n_loc_cols = 2
    
    return (grid,n_loc_rows,n_loc_cols,n_rows,n_cols)


def print_grid(grid,**kwargs) -> str:
    """
    Function to print the grid to the terminal in a readable format.

    """
    for row in grid:
        print(" ".join(str(cell) for cell in row))
    if kwargs.get('explainstring'):
        print('\nEXPLANATION:\n')
        for i in kwargs.get('explainstring'):
            print(i)
    return 'Finished execution! output printed to terminal.'



def write_grid_to_file(grid, file_name,**kwargs) -> str:
    """
    function for writing the solved (or partially solved) sudoku to the text file
    """
    with open(file_name, 'w') as file:
        try:
            for row in grid:
                file.write(" ".join(str(cell) for cell in row) + "\n")
        except TypeError:
            return f'failed to write, grid does not exist!!'
        if kwargs.get('explainstring'):
            file.write('\nEXPLANATION:\n')
            for i in kwargs.get('explainstring'):
                file.write(i+'\n')
    return f'Finished execution! output saved to {file_name}'



def generate_hints(unsolved: list,solved: list,hintnum: int) -> list:

    partially_solved = deepcopy(unsolved)
    counter = 0

    for ind,i in enumerate(solved):
        for ind2,j in enumerate(i):
            if not(j == unsolved[ind][ind2]) and counter <= hintnum:
                partially_solved[ind][ind2] = solved[ind][ind2]
                counter += 1

            else:
                partially_solved[ind][ind2] = unsolved[ind][ind2]

    return partially_solved


def write_explanation(unsolved: list,solved: list) -> list[str]:
    finalstr = []
    for ind_y, i in enumerate(solved):
        for ind_x, j in enumerate(i):
            if not unsolved[ind_y][ind_x] == j:
                finalstr.append(f'Place value {j} in position{ind_y,ind_x}')
    return finalstr

def main(args:dict):
    """
    Wrapper function, responsible for handling the command line arguments,
    and performing the subroutines in the correct combination according to the arguments.
    """
    file_in,file_out = args.get('file_provided') if args.get('file_provided') else [None,None]
    hint: int = int(args.get('doHint')[0]) if args.get('doHint') else None
    explain: bool = args.get('doExplain') if args.get('doExplain') else False
    profile_source = args.get('doProfiling') if args.get('doProfiling') else None

    #try: file_in, file_out = files 
    #except: file_in = file_out = None
    steps=[]
    if profile_source: return Profiler.profilinghandler(profile_source)
    if file_in:
        #if files have been provided, read it.
        print(f'Reading grid from {file_in}...')
        grid: tuple = read_grid_from_file(file_in)
        unsolved = deepcopy(grid[0])
        solution = recursive_solve(*grid,explain=explain,steps=steps)
        
    else:

        #if no input file has been provided, just default to a built-in sudoku
        print(f'WARNING: invalid/none input file has been provided, defaulting to built in grid.')
        unsolved = deepcopy(easy3)
        solution = recursive_solve(easy3,3,2,6,6,explain=explain,steps=steps)

    if hint:
        #If hints are toggled on
        
        #generate the partially solved grid according to how many need to be filled in.
        partially_solved_grid = generate_hints(unsolved,solution,hint)
        
        if explain:
             #if hints on and explanation
             #requires a different explanation function to work properly \(0_0)/
             explanation = write_explanation(unsolved,partially_solved_grid)
             
             if file_out:
                return write_grid_to_file(partially_solved_grid,file_out,explainstring=explanation)
             else:
                return print_grid(partially_solved_grid,explainstring=explanation)
            
        else:
            #if hints only, no explanation
            if file_out:
                return write_grid_to_file(partially_solved_grid,file_out)
            else:
                return print_grid(partially_solved_grid)
            
    else:
        if explain:
            #explanation = write_explanation(unsolved,solution)
            explanation = steps
            if file_out:
                #if grid from file, and explanation on, but no hints
                return write_grid_to_file(solution,file_out,explainstring=explanation)
            else:
                #if explanation, no hints and no in/out file
                return print_grid(solution,explanation=explanation)
        else:
            if file_out:
                return write_grid_to_file(solution,file_out)
            else:
                return print_grid(solution)
        
    
    
    



 
if __name__ == "__main__":
    """
    main function
    """

    parser = argparse.ArgumentParser(description="Solve a Sudoku grid from a text file, \
                                     with additional options such as profiling and explaining the solution")
    
    parser.add_argument('-f','--file',dest='file_provided', 
                        help= "The input Sudoku grid file.", nargs=2,action='extend')
    parser.add_argument('-e','--explain',dest='doExplain',     
                        help= "Toggles whether an explanation is added",action='store_true')
    parser.add_argument('-ht','--hint'   ,dest='doHint',        
                        help= 'only fill in the grid with x amount of correct values',action='store',nargs=1)
    
    """
    profiling_subparser = parser.add_subparsers(help='subparser for the profiling mode.')
    profiling_subparser.add_parser('profiling',help='arguments for the profiling mode. all other arguments will not work from now on!')
    profiling_subparser.add_argument("--graph",dest='doProfiling',  
                        help= 'the output file of the graph image if you would like to save it.',
                            action='extend',nargs=1)
    profiling_subparser.add_argument("--display",dest='doProfiling',  
                        help='which graph preset mode you want the program to display. there are 5 different display modes',
                        action ='extend',choices = [i for i in range(5)],nargs= 1,type=int)
    #parser.add_argument("--csv"),dest='doProfiling'
    """

                    
    args: dict = vars(parser.parse_args())
    print(main(args))
    

    


        


        
