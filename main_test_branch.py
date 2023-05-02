import argparse
from copy import deepcopy
import Profiler
from functions.write_explanation_func import write_explanation
from functions.check_section_func import check_section
from functions.split_into_squares_func import split_into_squares
from functions.find_n_rows_cols_func import find_n_rows_cols
from functions.get_squares_func import get_squares

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








def check_solution(grid, n_sub_rows, n_sub_cols):
    """
    The "check_solution" function assesses whether the given grid satisfies the rules of Sudoku or not
    :param grid: given grid
    :param n_sub_rows: row dimension of the grid
    :param n_sub_cols: column dimension of the grid
    :return: True if the grid is solved, otherwise False
    """
    # The number of columns and rows is defined.
    n_rows, n_cols = find_n_rows_cols(grid)
    n = n_sub_rows * n_sub_cols
    # Every row of the grid is checked if it satisfies the required conditions of the game
    for row in grid:
        if not check_section(row, n):
            return False

    # Every column of the grid is checked if it satisfies the required conditions of the game
    for i in range(n_rows):
        n_cols = []
        for row in grid:
            n_cols.append(row[i])
        if not check_section(n_cols, n):
            return False

    # Every square in the grid is checked if it satisfies the required conditions of the game
    squares = get_squares(grid, n_sub_rows, n_sub_cols)
    for square in squares:
        if not check_section(square, n):
            return False

    return True


def get_all(grid, n_sub_rows, n_sub_cols, i, j):
    """
    The "get_all" function returns all the values present in the row, column, and square that contain the zero,
    which is given as an argument
    :param grid: given grid
    :param n_sub_rows: row dimension of the grid
    :param n_sub_cols: column dimension of the grid
    :param i: row that contains the zero
    :param j: column that contains the zero
    :return: list of all the values present in the row, column, and square that contain the zero
    """
    # The number of columns and rows is defined.
    n_rows, n_cols = find_n_rows_cols(grid)
    # These list comprehensions retrieve all the values in the row and column that contain the zero.
    row = [grid[i][k] for k in range(n_cols) if grid[i][k] != 0]
    col = [(grid[k][j]) for k in range(n_rows) if grid[k][j] != 0]

    # The anchor points for the rows and columns are calculated.
    row_split = split_into_squares(n_sub_rows, n_rows)
    col_split = split_into_squares(n_sub_cols, n_cols)

    # The loops below determine which square contains the zero being evaluated, based on its position. If we assume
    # that the variable row_split has the values [0, 3, 6], and the position of the zero is denoted by i and j (for
    # instance, i=0 and j=0), we need the code to return (0, 3) as the anchor points for the square that
    # contains the zero.
    for k in row_split:
        # The position of the zero must be greater than its anchor point
        if i >= k:
            ind = row_split.index(k)
    base_i = row_split[ind]
    for k in col_split:
        if j >= k:
            ind = col_split.index(k)
    base_j = col_split[ind]

    # Depending on the anchor points of the zero, the values of the respective square are retrieved.
    square = []
    for a in range(n_rows // n_sub_rows):
        for b in range(n_cols // n_sub_cols):
            if grid[base_i + a][base_j + b] != 0:
                square.append(grid[base_i + a][base_j + b])

    # Combining all the values in the row, column, and square that contain the zero, we get all the values that must
    # be considered when solving a Sudoku board.
    all_present = row + col + square

    # Set data type helps get rid of the repeated values in a list
    return set(all_present)


def get_possible(grid, n_sub_rows, n_sub_cols, i, j):
    """
    The "get_possible function" returns only the values that could be placed instead of the zero for a
    Sudoku grid to be solved.

    :param grid: given grid
    :param n_sub_rows: row dimension of the grid
    :param n_sub_cols: column dimension of the grid
    :param i: row that contains the zero
    :param j: column that contains the zero
    :return: list of possible values instead of the zero
    """
    # The number of columns and rows is defined.
    n_rows, n_cols = find_n_rows_cols(grid)
    # All possible values that could be contained in the grid.
    all_possible = [i for i in range(1, n_rows + 1)]
    # All the values that are present in the row, column, and square that contain the zero
    all_present = get_all(grid, n_sub_rows, n_sub_cols, i, j)
    # By employing minus, we exclude all the values that are present, leaving only a list of the values that could
    # fit in place of the zero.
    only_suitable = list(set(all_possible) - set(all_present))

    return only_suitable


def bubble_sort(any_list: list) -> list:
    """
    Ordinary bubble sort function that is used to sort zeros starting from the one with the least possible values to
    the one with the most
    :param any_list: given list
    :return: sorted list
    """
    length = len(any_list)
    for i in range(0, length):
        for j in range(0, length - i - 1):
            if any_list[j][2] > any_list[j + 1][2]:
                buffer = any_list[j]
                any_list[j] = any_list[j + 1]
                any_list[j + 1] = buffer

    return any_list


def find_empty(grid: int, n_sub_rows: int, n_sub_cols: int) -> list:
    """
    The "find_empty" function looks for all zeros in the grid and returns the list representing each zero in the
    form [[i-position, j-position, number of possible values, possible value 1, possible value2...][...]]
    :param grid: given grid
    :param n_sub_rows: row dimension of the grid
    :param n_sub_cols: column dimension of the grid
    :return: list with all zeros in the grid
    """
    # The number of columns and rows is defined.
    n_rows, n_cols = find_n_rows_cols(grid)
    # List with all sub-lists included.
    zeros_outer = []
    # Sub-list containing information about one zero.
    zeros_inner = []
    # The nested loop below adds i and j-positions to the sublist of the zero.
    for i in range(n_rows):
        for j in range(n_cols):
            if grid[i][j] == 0:
                zeros_inner.append(i)
                zeros_inner.append(j)
                zeros_outer.append(zeros_inner)
                zeros_inner = []

    # The given nested loop adds the number of possible values in addition to i and j-positions and lists all of them
    # after the third element of the sub-list.
    for a in range(len(zeros_outer)):
        i, j = zeros_outer[a]

        only_suitable = get_possible(grid, n_sub_rows, n_sub_cols, i, j)
        zeros_outer[a].append(len(only_suitable))
        for b in only_suitable:
            zeros_outer[a].append(b)

    # The zeros are sorted from the easiest to the hardest to solve based on the number of possible values (third
    # element in the sub-list).
    zeros_sorted = bubble_sort(zeros_outer)

    return zeros_sorted


def solve(grid: list, n_sub_rows: int, n_sub_cols: int, explain: bool = None, steps: list = None) -> list[list[int]]:
    """
    The "solve" function is called recursively to find the solution for the grid.

    The function first checks whether there is an empty space to place a number. If such space exists,
    the function will replace that space with the first possible value and call itself again to find the next zero.

    If no other possibilities are available, the function will exit with a value of None and go back to the previous
    zero to try other values.

    If the top level of recursion (i.e., depth 0) returns None, it means that the function has gone through every
    possibility, and there are no valid solutions to the Sudoku.

    If the "find_empty" function does not find any zeros (i.e., the Sudoku is completely filled), the function will
    check the grid. If it is valid, the function will return the grid to the top of the recursion stack via the line
    "if ans: return ans."

    :param grid: given grid
    :param n_sub_rows: row dimension of the grid
    :param n_sub_cols: column dimension of the grid
    :param explain: whether to add explanation instructions to the output.
    :param steps: list of explanation instructions to be fed into the function when called recursively

    :return: solved grid
    """
    # Finding the empty space, and the possibilities that it can be.
    zeros = find_empty(grid, n_sub_rows, n_sub_cols)

    # if the grid is full already, the if statement checks it through the game requirements.
    if not zeros:
        if check_solution(grid, n_sub_rows, n_sub_cols):
            return grid

    # We define the coordinates of the zero.
    row, col = zeros[0][0], zeros[0][1]
    possible_digits = [zeros[0][i] for i in range(3, len(zeros[0]))]

    # The for loop below loops through every possible value and calls the "solve" function again once it has swapped
    # out the zero.
    for i in possible_digits:
        grid[row][col] = i

        if explain and steps is not None:
            steps.append(f"Place value {i} in position {row, col}")
        ans = solve(grid, n_sub_rows, n_sub_cols)
        # This if statement is only true once the bottom of the recursion depth has been reached AND
        # the grid is solved. basically just passes the grid back up the stack.
        if ans:
            return ans
        # If there were no solutions with the current choice of numbers, then reset the number back to zero,
        # and try again with a different value.
        if explain and steps is not None:
            steps.pop()

        grid[row][col] = 0

    return None


def read_grid_from_file(file_name: str) -> list:
    """
    Function to read the grid from a text file. and to return the grid in a format that is understandable by the
    solve() function.

    :param file_name: the given file name.
    :return: the grid as a nested list.

    """
    with open(file_name, 'r') as file:
        # formatting the raw text in order to extract just the numbers.
        grid = [[int(num) for num in line.strip().split(',')] for line in file]

    # determining the grid dimensions.
    grid_dims_y = len(grid)
    grid_dims_x = len(grid[0])

    # if the grid is a 9x9 or a 4x4 grid, subgrid dimensions are simply squares with length 3 or 2 respectively.
    if grid_dims_y in [9, 4]:
        subgrid_dims_x = subgrid_dims_y = int(grid_dims_y ** 0.5)

    # if the grid is a 6x6, slightly different procedure. subgrids are now 3x2 rectangles instead of squares.
    elif grid_dims_y == 6:
        subgrid_dims_x = 2
        subgrid_dims_y = 3

    return (grid, subgrid_dims_y, subgrid_dims_x)


def print_grid(grid: list, **kwargs) -> str:
    """
    Function to print the grid to the terminal in a readable format.

    :param grid: the grid to be printed.
    :return: a string which confirms execution of the printing process has finished.

    """
    print('SOLUTION:\n')
    for row in grid:
        print(" ".join(str(cell) for cell in row))

    if kwargs.get('explainstring'):
        print('\nEXPLANATION:\n')
        for i in kwargs.get('explainstring'):
            print(i)

    return 'Finished execution! output printed to terminal.'


def write_grid_to_file(grid, file_name, **kwargs) -> str:
    """
    function for writing the solved (or partially solved) sudoku to the text file.

    :param grid: the grid to write to the file.
    :param file_name: the path to the file which will be created or overwritten.
    :return: a string confirming the success or failiure of the write operation.
    """
    with open(file_name, 'w') as file:
        try:
            for row in grid:
                file.write(" ".join(str(cell) for cell in row) + "\n")

        # if it cant iterate over the grid as its a NoneType, it means the solver failed to solve the grid.
        except TypeError:
            return 'failed to write, grid does not exist!!'

        # if an explain string is given, write it to the file, after the solved grid.
        if kwargs.get('explainstring'):
            file.write('\nEXPLANATION:\n')
            for i in kwargs.get('explainstring'):
                file.write(i + '\n')

    return f'Finished execution! output saved to {file_name}'


def generate_hints(unsolved: list, solved: list, hintnum: int) -> list:
    """
    this function will take the completely solved grid, and remove some of the elements of the
    solved grid, until it is left with a partially solved grid, with the amount of solved cells
    equal to the {solved} argument.

    :param unsolved: a copy of the unsolved grid used as reference.
    :param solved: the solved list to be subtracting from
    :return: a partially solved grid with {hintnum} amount of empty cells filled in.
    """
    # make a deep copy of the unsolved grid.
    # needed as a simple copy with nested lists will make a copy but the lists inside will still
    # point to the same list in memory, so a deepcopy is needed to make a completely unlinked list.
    partially_solved: list[list[int]] = deepcopy(unsolved)
    counter: int = 0

    # loop through y dimensions of grid.
    for ind, i in enumerate(solved):
        # loop through x dimensions of grid.
        for ind2, j in enumerate(i):
            # if the unsolved grid is different from the solved grid (i.e. a cell filled by the solver)
            # and the number of hints required has not been reached, add it to the partially solved grid.
            if not (j == unsolved[ind][ind2]) and counter <= hintnum:
                partially_solved[ind][ind2] = solved[ind][ind2]
                counter += 1

            # otherwise, keep it unsolved.
            else:
                partially_solved[ind][ind2] = unsolved[ind][ind2]

    return partially_solved



def main(args: dict):
    """
    Wrapper function, responsible for handling the command line arguments,
    and performing the subroutines in the correct combination according to the arguments.

    :param args: the parsed arguments, in the form of a dictionary.
    :return: whatever the return string of the write_grid_to_file() function or the print_grid() function.
    """
    file_in, file_out = args.get('file_provided') if args.get('file_provided') else [None, None]
    hint: int = int(args.get('doHint')[0]) if args.get('doHint') else None
    explain: bool = args.get('doExplain') if args.get('doExplain') else False
    profile_mode = args.get('doProfiling') if args.get('doProfiling') else None

    steps = []
    if profile_mode:
        print('Profile mode selected!')
        profiling_relevant_arguments = ['csvPath', 'displayMode', 'sourceDirectory', 'graphPath', 'sampleSize']
        profiling_relevant_arguments = {k: args[k] for k in args.keys() if k in profiling_relevant_arguments}
        return Profiler.profilinghandler(profiling_relevant_arguments)

    if file_in:
        # if files have been provided, read it.
        print(f'Reading grid from {file_in}...')
        grid: tuple = read_grid_from_file(file_in)
        unsolved = deepcopy(grid[0])
        solution = solve(*grid, explain=explain, steps=steps)

    else:

        # if no input file has been provided, just default to a built-in sudoku
        print('WARNING: invalid/none input file has been provided, defaulting to built in grid.')
        unsolved = deepcopy(easy3)
        solution = solve(easy3, 3, 2, explain, steps)

    if hint:
        # If hints are toggled on

        # generate the partially solved grid according to how many need to be filled in.
        partially_solved_grid = generate_hints(unsolved, solution, hint)

        if explain:
            # if hints on and explanation
            # requires a different explanation function to work properly \(0_0)/
            explanation = write_explanation(unsolved, partially_solved_grid)

            if file_out:
                return write_grid_to_file(partially_solved_grid, file_out, explainstring=explanation)
            else:
                return print_grid(partially_solved_grid, explainstring=explanation)

        else:
            # if hints only, no explanation
            if file_out:
                return write_grid_to_file(partially_solved_grid, file_out)
            else:
                return print_grid(partially_solved_grid)

    else:
        if explain:
            # explanation = write_explanation(unsolved,solution)
            explanation = steps
            if file_out:
                # if grid from file, and explanation on, but no hints
                return write_grid_to_file(solution, file_out, explainstring=explanation)
            else:
                # if explanation, no hints and no in/out file
                return print_grid(solution, explanation=explanation)
        else:
            if file_out:
                return write_grid_to_file(solution, file_out)
            else:
                return print_grid(solution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a Sudoku grid from a text file, \
            with additional options such as profiling and explaining the solution")

    profiling_subparser = parser.add_subparsers(description=
                                                'Assess the performance of the solving algorithm across many grids and many attempts. \
                                                use "main.py profiling -h/--help" for help on profiling-specific arguments',
                                                dest='doProfiling', title='Profiling')
    profiling = profiling_subparser.add_parser('profiling',
                                               description='Arguments for the profiling mode. all other arguments will not work from now on!')

    parser.add_argument('-f', '--file', dest='file_provided',
                        help="The input Sudoku grid file.", nargs=2, action='extend')
    parser.add_argument('-e', '--explain', dest='doExplain',
                        help="Toggles whether an explanation is added", action='store_true')
    parser.add_argument('-ht', '--hint', dest='doHint',
                        help='only fill in the grid with x amount of correct values', action='store', nargs=1)

    profiling.add_argument("-g", "--graph", dest='graphPath',
                           help='the output path of the graph image if you would like to save it.',
                           action='extend', nargs=1, type=str)
    profiling.add_argument("-dir", "--directory", dest='sourceDirectory',
                           help='the source of the directory of the test grids.',
                           action='extend', required=True, nargs=1, type=str)
    profiling.add_argument("--display", dest='displayMode',
                           help='which graph preset mode you want the program to display. there are 5 different display modes',
                           action='extend', choices=[i for i in range(1, 6)], nargs=1, type=int, default=1)
    profiling.add_argument("--samplesize", dest='sampleSize',
                           help='how many times to loop through the directory containing the grids. \
            Higher value means profiling takes longer, but will more precise timing info. Default value:10',
                           action='store', nargs=1,
                           type=int, default=10)
    profiling.add_argument("--csv", dest='csvPath',
                           help='the output path of the csv file containing timings if you would like to save it.',
                           action='extend', nargs=1, type=str)

    args: dict = vars(parser.parse_args())

    print(main(args))
