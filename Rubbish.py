import time

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


def check_section(section, n):
    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True

    return False


def get_squares(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
    squares = []
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

    return set(all_present)


def get_possible(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, i, j):
    all_possible = [i for i in range(1, n_rows + 1)]
    all_present = get_all(grid, n_loc_rows, n_loc_cols, i, j, n_rows, n_cols)
    only_suitable = list(set(all_possible) - set(all_present))

    return only_suitable


def recursive_solve(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
    zeros = find_empty(grid, n_rows, n_cols, n_rows, n_cols)

    if not zeros:
        if check_solution(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
            return grid

    row, col = zeros[0][0], zeros[0][1]
    possible_digits = [zeros[0][i] for i in range(3, len(zeros[0]))]

    for i in possible_digits:
        grid[row][col] = i
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


start_time = time.time()
print(recursive_solve(grid1, 2, 2, 4, 4))
print(recursive_solve(grid2, 2, 2, 4, 4))
print(recursive_solve(grid3, 2, 2, 4, 4))
print(recursive_solve(grid4, 2, 2, 4, 4))
print(recursive_solve(grid5, 2, 2, 4, 4))
elapsed_time = time.time() - start_time
print(elapsed_time)
