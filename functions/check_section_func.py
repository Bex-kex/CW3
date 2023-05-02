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
