import time

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


def check_section(section, n):
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


def get_all(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, i, j):
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


def get_possible(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, i, j):
    all_possible = [i for i in range(1, n_rows + 1)]
    all_present = get_all(grid, n_loc_rows, n_loc_cols, n_rows, n_cols, i, j)
    only_suitable = list(set(all_possible) - set(all_present))

    return only_suitable


def recursive_solve(grid, n_loc_rows, n_loc_cols, n_rows, n_cols):
    zeros = find_empty(grid, n_loc_rows, n_loc_cols, n_rows, n_cols)

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
print(recursive_solve(easy3, 3, 2, 6, 6))
elapsed_time = time.time() - start_time
print(elapsed_time)