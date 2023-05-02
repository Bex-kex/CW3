from find_n_rows_cols_func import find_n_rows_cols
from split_into_squares_func import split_into_squares

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
