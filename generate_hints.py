from copy import deepcopy

def generate_hints(unsolved: list, solved: list, hintnum: int) -> list:
    """
    this function will take the completely solved grid, and remove some of the elements of the
    solved grid, until it is left with a partially solved grid, with the amount of solved cells
    equal to the {solved} argument.

    :param unsolved: a copy of the unsolved grid used as reference.
    :param solved: the solved list to be subtracting from
    :return: a partially solved grid with {hintnum} amount of empty cells filled in.
    """
    # make a deep copy of the unsolved grid.
    # needed as a simple copy with nested lists will make a copy but the lists inside will still
    # point to the same list in memory, so a deepcopy is needed to make a completely unlinked list.
    partially_solved: list[list[int]] = deepcopy(unsolved)
    counter: int = 0

    # loop through y dimensions of grid.
    for ind, i in enumerate(solved):
        # loop through x dimensions of grid.
        for ind2, j in enumerate(i):
            # if the unsolved grid is different from the solved grid (i.e. a cell filled by the solver)
            # and the number of hints required has not been reached, add it to the partially solved grid.
            if not (j == unsolved[ind][ind2]) and counter <= hintnum:
                partially_solved[ind][ind2] = solved[ind][ind2]
                counter += 1

            # otherwise, keep it unsolved.
            else:
                partially_solved[ind][ind2] = unsolved[ind][ind2]

    return partially_solved