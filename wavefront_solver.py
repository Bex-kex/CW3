def check_section(section, n):
    """
    The "check_section" function is responsible for checking if a section of the grid is filled according to
    the rules of Sudoku.
    :param section: row or column
    :param n: product of the numbers of sub-columns and sub-rows
    :return: True if a row or a column meets the requirements of the game, otherwise False
    """
    # The following if statement is used to check whether a section contains any repetitive values and whether the
    # sum of values in the section is equal to the sum of the numbers from 1 to n (the maximum allowed value).
    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True

    return False


def split_into_squares(sub_grid, n):
    """
    The "split_into_squares" function defines the anchor points in the grid, which will be used to split the grid
    into equally-sized squares. For instance, in a 9x9 grid with 9 rows and 9 columns, the anchor points will be 0,
    3, and 6. These anchor points determine where the grid should be split to form 3x3 squares
    :param sub_grid: row or column dimension of the grid
    :param n: number of rows or columns
    :return: list of anchor points
    """
    split = []
    # The variable boundary is set to 0 and acts as a starting point
    boundary = 0
    # The loop below defines the number of anchor points depending on the dimensions of the grid.
    for i in range(sub_grid):
        split.append(boundary)
        # This line increments the "boundary" variable by the width of the grid.
        boundary += n // sub_grid

    return split


def find_n_rows_cols(grid):
    """
    The "find_n_rows_cols" function returns the number of rows and columns in the grid
    :param grid: given grid
    :return: number of rows and columns
    """
    n_rows = len(grid)
    n_cols = len(grid[0])
    return n_rows, n_cols


def bubble_sort(any_list: list) -> list:
    """
    Ordinary bubble sort function that is used to sort zeros starting from the one with the least possible values to
    the one with the most
    :param any_list: given list
    :return: sorted list
    """
    
    
    any_list.sort(key=lambda a: a[2])
    
    
    # length = len(any_list)
    # for i in range(0, length):
    #     for j in range(0, length - i - 1):
    #         if any_list[j][2] > any_list[j + 1][2]:
    #             buffer = any_list[j]
    #             any_list[j] = any_list[j + 1]
    #             any_list[j + 1] = buffer
    
    

    return any_list


def get_squares(grid, n_sub_rows, n_sub_cols):
    """
    The "get_squares" function divides the grid in equally-sized squares
    :param grid: given grid
    :param n_sub_rows: row dimension of the grid
    :param n_sub_cols: column dimension of the grid
    :return: list where each sublist represents one square in the grid
    """
    # The number of columns and rows is defined.
    n_rows, n_cols = find_n_rows_cols(grid)
    squares = []

    # The anchor points for the rows and columns are calculated.
    row_split = split_into_squares(n_sub_rows, n_rows)
    col_split = split_into_squares(n_sub_cols, n_cols)

    # The nested loop below forms squares by adding a certain number to an anchor positions of the grid.
    for row in row_split:
        for col in col_split:
            square = []
            # The maximum number being added to an anchor position depends on the width of a square in the grid. The
            # loop picks one row first and then goes through all the column values in that row.
            for i in range(n_rows // n_sub_rows):
                for j in range(n_cols // n_sub_cols):
                    square.append(grid[row + i][col + j])
            squares.append(square)

    return squares


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
    zeros_outer.sort(key=lambda a: a[2])
    

    return zeros_outer


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
            if explain: 
                return grid,steps
            else:
                return grid,None

    # We define the coordinates of the zero.
    row, col = zeros[0][0], zeros[0][1]
    possible_digits = [zeros[0][i] for i in range(3, len(zeros[0]))]

    # The for loop below loops through every possible value and calls the "solve" function again once it has swapped
    # out the zero.
    for i in possible_digits:
        grid[row][col] = i

        if explain and steps is not None:
            steps.append(f"Place value {i} in position {row, col}")
        ans = solve(grid, n_sub_rows, n_sub_cols,explain,steps)
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
