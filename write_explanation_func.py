def write_explanation(unsolved: list, solved: list) -> list[str]:
    """
    this function will write the explanation of what numbers have been filled in and where,
    in order to get to the solved grid. This function is only used when hints is enabled, as the
    other implementation of the explain procedure would not match with the partially solved grid.

    :param unsolved: the unsolved grid used to compare what has changed.
    :param solved: the solved, or partially solved grid used as the reference.
    :return: a list of strings, the strings containing the co ordinate of the empty cell and the value to put in it.

    """
    finalstr: list[str] = []
    for ind_y, i in enumerate(solved):
        for ind_x, j in enumerate(i):
            if not unsolved[ind_y][ind_x] == j:
                finalstr.append(f'Place value {j} in position{ind_y, ind_x}')
    return finalstr
