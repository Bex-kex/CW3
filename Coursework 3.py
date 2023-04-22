import argparse
import sys
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


def find_empty(grid, n_rows, n_cols):
    for i in range(n_rows):
        for j in range(n_cols):
            if grid[i][j] == 0:
                return i, j


def get_all(grid, n_loc_rows, n_loc_cols, i, j, n_rows, n_cols):
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
    #print(set(all_present))
    return set(all_present)


def get_possible(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, i, j):
    all_possible = [i for i in range(1, n_rows + 1)]
    all_present = get_all(grid, n_loc_rows, n_loc_cols, i, j, n_rows, n_cols)
    only_suitable = list(set(all_possible) - set(all_present))

    return only_suitable


def recursive_solve(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
    global depth
    global EXPLAIN
    empty = find_empty(grid, n_rows, n_cols)

    if not empty:
        if check_solution(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
            if EXPLAIN:...
            return grid
        else:
            return None
    else:
        row, col = empty

    possible_digits = get_possible(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, row, col)

    for i in possible_digits:
        grid[row][col] = i
        depth += 1
        ans = recursive_solve(grid, n_loc_rows, n_loc_cols, n_rows, n_cols)
        if ans:
            return ans
        grid[row][col] = 0
    
    return None


# print(check_solution(grid1, 2, 2, 4, 4), check_solution(grid2, 2, 2, 4, 4), check_solution(grid3, 2, 2, 4, 4),
#       check_solution(grid4, 2, 2, 4, 4), check_solution(grid5, 3, 3, 9, 9),
#       check_solution(grid6, 3, 3, 9, 9), check_solution(grid7, 3, 3, 9, 9), check_solution(grid8, 3, 2, 6, 6),
#       check_solution(grid9, 3, 2, 6, 6),
#       check_solution(grid10, 3, 2, 6, 6))
depth = 0
def parsed() -> tuple:
    """
    simple function which parses the grid in the file provided,
    into a nested list which is compatible with the solver.
    also determines the dimensions of the given grid.
    """
    output_list = []
    with open(FILE_IN) as file:
        #opening the txt file specified by the FILE_IN cmdline argument
        for i in file.readlines():
            #reading each line of the txt file and formatting the grid
            line:list = [int(j) for j in i.strip('\n').split(', ')]
            output_list.append(line)
            #appending the formatted list to the final output list

    main_dims = len(output_list[0])
    subgrid_dims = int(main_dims**(1/2))
            
    return (output_list,subgrid_dims,subgrid_dims,main_dims,main_dims)


def write_to_file(ans:list,explanation=None) -> None:
    """
    This function takes the answer grid and also if available the explanation of the answer,
    and writes it to a new file, the filepath and filename given in the cmdline argument:
    FILE_OUT
    """
    with open(FILE_OUT,'w') as output_file:
        for line in ans:
            line = str(line).strip('[]') + '\n'
            output_file.writelines(line)
        if explanation:
            for i in explanation:
                output_file.writelines(i)
    print(f'Output saved to \"{FILE_OUT}\"')




def main(CLA:list)-> None:
    """
    Wrapper function which parses the command line arguments and runs
    the main script with the users selected settings, (e.g. hints=on, profiling=on)
    """
    global EXPLAIN
    global FILE_IN
    global FILE_OUT
    global HINT
    global PROFILE
    default_args = [False,None,None,0,False]
    #take command-line arguments and parse them into a dict
    if not CLA:
        EXPLAIN,FILE_IN,FILE_OUT,HINT,PROFILE = default_args
        print(recursive_solve(gridtest,3,3,9,9))
    args: dict = vars(parser.parse_args(CLA))
    
    for i in args.keys():
        #turning dict values into constants to be used in rest of program
        match i:
            #assigning constants values, based on what was inputted as arguments
            case 'explain':
                EXPLAIN = args.get(i)

            case 'file':
                try:
                    FILE_IN, FILE_OUT = args.get(i)

                except TypeError:
                    FILE_IN,FILE_OUT = None, None

            case 'hint':
                try:
                    HINT = int(args.get(i).pop())

                except:
                    HINT = 0

            case 'profile':
                PROFILE = args.get(i)
    if FILE_IN:
        #if there is a filepath given, solve the sudoku in the text file and...
        #save the output to a separate text file
        write_to_file(recursive_solve(*parsed()))
      
    else:...
        #else, just print the results to the terminal
        #print(recursive_solve(gridtest,3,3,9,9))
    
    
    #print(recursive_solve(gridtest, 3, 3, 9, 9))
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #adding args using argparse module
    parser.add_argument("-e","--explain",action='store_true')
    parser.add_argument("--file",nargs=2,action='extend')
    parser.add_argument("--hint",nargs=1,action='store')
    parser.add_argument("-p","--profile",action='store_true')
    test_args = ['--file','grids/easy1.txt','out.txt']
    main(test_args)
    #main(sys.argv[1:])




