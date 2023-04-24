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
    [0, 4, 0, 0, 1, 3, 7, 0, 6]
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
    empty = find_empty(grid, n_rows, n_cols)

    if not empty:
        if check_solution(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
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
print(recursive_solve(grid6, 3, 3, 6, 6))

#  Function to read the grid from a text file
def read_grid_from_file(file_name):
    with open(file_name, 'r') as file:
        grid = [[int(num) for num in line.strip().split(',')] for line in file]
    return grid

#  Function to print the grid in a readable format
def print_grid(grid):
    for row in grid:
        print(" ".join(str(cell) for cell in row))

def write_grid_to_file(grid, file_name):
    with open(file_name, 'w') as file:
        for row in grid:
            file.write(" ".join(str(cell) for cell in row) + "\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a Sudoku grid from a text file.")
    parser.add_argument("file_name", help="The input Sudoku grid file.")
    args = parser.parse_args()

    input_grid = read_grid_from_file(args.file_name)
    n_rows = len(input_grid)
    n_cols = len(input_grid[0])
    n_loc_rows = n_loc_cols = int(n_rows ** 0.5)

    solution = recursive_solve(input_grid, n_loc_rows, n_loc_cols, n_rows, n_cols)

    if solution:
        print("Solved Sudoku grid:")
        print_grid(solution)
        # Save the solution to a text file
        output_file_name = args.file_name.replace(".txt", "_solution.txt")
        write_grid_to_file(solution, output_file_name)
        print(f"Solution saved to file: {output_file_name}")
    else:
        print("The provided Sudoku grid has no solution.")


