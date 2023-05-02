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