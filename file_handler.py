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