import argparse
from copy import deepcopy
import Profiler
from write_explanation_func import write_explanation
from wavefront_funcs import *
from file_handler import *

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


def main(args: dict):
    """
    Wrapper function, responsible for handling the command line arguments,
    and performing the subroutines in the correct combination according to the arguments.

    :param args: the parsed arguments, in the form of a dictionary.
    :return: whatever the return string of the write_grid_to_file() function or the print_grid() function.
    """
    file_in, file_out = args.get('file_provided') if args.get('file_provided') else [None, None]
    hint: int = int(args.get('doHint')[0]) if args.get('doHint') else None
    explain: bool = args.get('doExplain') if args.get('doExplain') else False
    profile_mode = args.get('doProfiling') if args.get('doProfiling') else None

    steps = []
    if profile_mode:
        print('Profile mode selected!')
        profiling_relevant_arguments = ['csvPath', 'displayMode', 'sourceDirectory', 'graphPath', 'sampleSize']
        profiling_relevant_arguments = {k: args[k] for k in args.keys() if k in profiling_relevant_arguments}
        return Profiler.profilinghandler(profiling_relevant_arguments)

    if file_in:
        # if files have been provided, read it.
        print(f'Reading grid from {file_in}...')
        grid: tuple = read_grid_from_file(file_in)
        unsolved = deepcopy(grid[0])
        solution = solve(*grid, explain=explain, steps=steps)

    else:

        # if no input file has been provided, just default to a built-in sudoku
        print('WARNING: invalid/none input file has been provided, defaulting to built in grid.')
        unsolved = deepcopy(easy3)
        solution = solve(easy3, 3, 2, explain, steps)

    if hint:
        # If hints are toggled on

        # generate the partially solved grid according to how many need to be filled in.
        partially_solved_grid = generate_hints(unsolved, solution, hint)

        if explain:
            # if hints on and explanation
            # requires a different explanation function to work properly \(0_0)/
            explanation = write_explanation(unsolved, partially_solved_grid)

            if file_out:
                return write_grid_to_file(partially_solved_grid, file_out, explainstring=explanation)
            else:
                return print_grid(partially_solved_grid, explainstring=explanation)

        else:
            # if hints only, no explanation
            if file_out:
                return write_grid_to_file(partially_solved_grid, file_out)
            else:
                return print_grid(partially_solved_grid)

    else:
        if explain:
            # explanation = write_explanation(unsolved,solution)
            explanation = steps
            if file_out:
                # if grid from file, and explanation on, but no hints
                return write_grid_to_file(solution, file_out, explainstring=explanation)
            else:
                # if explanation, no hints and no in/out file
                return print_grid(solution, explanation=explanation)
        else:
            if file_out:
                return write_grid_to_file(solution, file_out)
            else:
                return print_grid(solution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a Sudoku grid from a text file, \
            with additional options such as profiling and explaining the solution")

    profiling_subparser = parser.add_subparsers(description=
                                                'Assess the performance of the solving algorithm across many grids and many attempts. \
                                                use "main.py profiling -h/--help" for help on profiling-specific arguments',
                                                dest='doProfiling', title='Profiling')
    profiling = profiling_subparser.add_parser('profiling',
                                               description='Arguments for the profiling mode. all other arguments will not work from now on!')

    parser.add_argument('-f', '--file', dest='file_provided',
                        help="The input Sudoku grid file.", nargs=2, action='extend')
    parser.add_argument('-e', '--explain', dest='doExplain',
                        help="Toggles whether an explanation is added", action='store_true')
    parser.add_argument('-ht', '--hint', dest='doHint',
                        help='only fill in the grid with x amount of correct values', action='store', nargs=1)

    profiling.add_argument("-g", "--graph", dest='graphPath',
                           help='the output path of the graph image if you would like to save it.',
                           action='extend', nargs=1, type=str)
    profiling.add_argument("-dir", "--directory", dest='sourceDirectory',
                           help='the source of the directory of the test grids.',
                           action='extend', required=True, nargs=1, type=str)
    profiling.add_argument("--display", dest='displayMode',
                           help='which graph preset mode you want the program to display. there are 5 different display modes',
                           action='extend', choices=[i for i in range(1, 6)], nargs=1, type=int, default=1)
    profiling.add_argument("--samplesize", dest='sampleSize',
                           help='how many times to loop through the directory containing the grids. \
            Higher value means profiling takes longer, but will more precise timing info. Default value:10',
                           action='store', nargs=1,
                           type=int, default=10)
    profiling.add_argument("--csv", dest='csvPath',
                           help='the output path of the csv file containing timings if you would like to save it.',
                           action='extend', nargs=1, type=str)

    args: dict = vars(parser.parse_args())

    print(main(args))
