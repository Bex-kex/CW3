def find_n_rows_cols(grid):
    """
    The "find_n_rows_cols" function returns the number of rows and columns in the grid
    :param grid: given grid
    :return: number of rows and columns
    """
    n_rows = len(grid)
    n_cols = len(grid[0])
    return n_rows, n_cols