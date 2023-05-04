
import argparse
from copy import deepcopy
import profiler

import file_handler
import wavefront_solver
import recursive_solver


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


def generate_hints(unsolved: list,solved: list,hintnum: int) -> list:
    """
    this function will take the completely solved grid, and remove some of the elements of the 
    solved grid, until it is left with a partially solved grid, with the amount of solved cells 
    equal to the {solved} argument.

    :param unsolved: a copy of the unsolved grid used as reference.
    :param solved: the solved list to be subtracting from
    :return: a partially solved grid with {hintnum} amount of empty cells filled in.
    """
    # make a deep copy of the unsolved grid.
    # required to make sure that the changes applied in the rest of the function
    # will only be applied to the partially solved grid.
    
    partially_solved: list[list[int]] = deepcopy(unsolved)
    counter: int = 0

    #loop through y dimensions of grid.
    for ind,i in enumerate(solved):
        #loop through x dimensions of grid.
        for ind2,j in enumerate(i):
            #if the unsolved grid is different from the solved grid (i.e. a cell filled by the solver)
            #and the number of hints required has not been reached, add it to the partially solved grid.
            if not(j == unsolved[ind][ind2]) and counter < hintnum:
                partially_solved[ind][ind2] = solved[ind][ind2]
                counter += 1

            #otherwise, keep it unsolved.
            else:
                partially_solved[ind][ind2] = unsolved[ind][ind2]

    return partially_solved

def solve(solver_choice,grid,n_sub_rows,n_sub_cols,explain=None,steps=None) -> list[list[int]]:
    match solver_choice:
        case 'wavefront':
            return wavefront_solver.solve(grid,n_sub_cols,n_sub_rows,explain,steps)
        case 'recursive':
            return recursive_solver.solve(grid,n_sub_rows,n_sub_cols,explain,steps)
        

def write_explanation(unsolved: list,solved: list) -> list[str]:
    """
    this function will write the explanation of what numbers have been filled in and where,
    in order to get to the solved grid. This function is only used when hints is enabled, as the 
    other implementation of the explain procedure would not match with the partially solved grid.
    
    :param unsolved: the unsolved grid used to compare what has changed.
    :param solved: the solved, or partially solved grid used as the reference.
    :return: a list of strings, the strings containing the co ordinate of the empty cell and the value to put in it.

    """
    finalstr:list[str] = []
    for ind_y, i in enumerate(solved):
        for ind_x, j in enumerate(i):
            if not unsolved[ind_y][ind_x] == j:
                finalstr.append(f'Place value {j} in position{ind_y,ind_x}')
    
    return finalstr

def main(cmdlineargs: dict):
    """
    Wrapper function, responsible for handling the command line arguments,
    and performing the subroutines in the correct combination according to the arguments.

    :param args: the parsed arguments, in the form of a dictionary.
    :return: whatever the return string of the FileHandler.write_grid_to_file() function or the FileHandler.print_grid() function.
    """
    file_in,file_out =  cmdlineargs.get('file_provided') if cmdlineargs.get('file_provided') else [None,None]
    hint: int        =  int(cmdlineargs.get('doHint')[0]) if cmdlineargs.get('doHint') else None
    explain: bool    =  cmdlineargs.get('doExplain') if cmdlineargs.get('doExplain') else False
    profile_mode     =  cmdlineargs.get('doProfiling') if cmdlineargs.get('doProfiling') else None
    solver_choice    =  cmdlineargs.get('solverChoice').pop() if type(cmdlineargs.get('solverChoice')) == list else cmdlineargs.get('solverChoice')

    steps=[]
    if profile_mode:
        print('Profile mode selected!')
        profiling_relevant_arguments = ['csvPath','displayMode','sourceDirectory','graphPath','sampleSize']
        profiling_relevant_arguments = {k:args[k] for k in args.keys() if k in profiling_relevant_arguments}
        return profiler.profilinghandler(profiling_relevant_arguments)

    if file_in:
        #if files have been provided, read it.
        print(f'Reading grid from {file_in}...')
        grid: tuple = file_handler.read_grid_from_file(file_in)
        unsolved = deepcopy(grid[0])
        solution,explain = solve(solver_choice,*grid,explain=explain,steps=steps)

    else:

        #if no input file has been provided, just default to a built-in sudoku
        print('WARNING: invalid/none input file has been provided, defaulting to built in grid.')
        unsolved = deepcopy(easy3)
        solution,explain = solve(solver_choice,easy3,2,3,explain,steps)
        
    if hint:
        #If hints are toggled on

        #generate the partially solved grid according to how many need to be filled in.
        partially_solved_grid = generate_hints(unsolved,solution,hint)

        if explain:
            #if hints on and explanation
            #requires a different explanation function to work properly \(0_0)/
            explanation = write_explanation(unsolved,partially_solved_grid)

            if file_out:
                return file_handler.write_grid_to_file(partially_solved_grid,file_out,explainstring=explanation)
            else:
                return file_handler.print_grid(partially_solved_grid,explainstring=explanation)

        else:
            #if hints only, no explanation
            if file_out:
                return file_handler.write_grid_to_file(partially_solved_grid,file_out)
            else:
                return file_handler.print_grid(partially_solved_grid)

    else:
        if explain:
            #explanation = write_explanation(unsolved,solution)
            explanation = steps
            if file_out:
                #if grid from file, and explanation on, but no hints
                return file_handler.write_grid_to_file(solution,file_out,explainstring=explanation)
            else:
                #if explanation, no hints and no in/out file
                return file_handler.print_grid(solution,explainstring=explanation)
        else:
            if file_out:
                return file_handler.write_grid_to_file(solution,file_out)
            else:
                return file_handler.print_grid(solution)




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Solve a Sudoku grid from a text file, \
            with additional options such as profiling and explaining the solution")
    
    profiling_subparser = parser.add_subparsers(description=
            'Assess the performance of the solving algorithm across many grids and many attempts. \
            use "main.py profiling -h/--help" for help on profiling-specific arguments',dest='doProfiling',title='Profiling')
    profiling = profiling_subparser.add_parser('profiling',
            description='Arguments for the profiling mode. all other arguments will not work from now on!')

    parser.add_argument('-f','--file',dest='file_provided',
            help= "The input Sudoku grid file.", nargs=2,action='extend')
    
    parser.add_argument('-e','--explain',dest='doExplain',
            help= "Toggles whether an explanation is added",action='store_true')
    
    parser.add_argument('-ht','--hint',dest='doHint',
            help= 'only fill in the grid with x amount of correct values',action='store',nargs=1)
    
    parser.add_argument('-s','--solver',dest='solverChoice',
            help='which solving algorithm you want to use.', choices=['wavefront','recursive'],
            action='store',default='wavefront',nargs=1,type=str)
    
    profiling.add_argument("-g","--graph",dest='graphPath',  
            help= 'the output path of the graph image if you would like to save it.',
            action='extend',nargs=1,type=str,default=[None])
    
    profiling.add_argument("-dir","--directory",dest='sourceDirectory',
            help='the source of the directory of the test grids.', 
            action='extend',required=True,nargs=1,type=str)
    
    profiling.add_argument("--display",dest='displayMode',  
            help='which graph preset mode you want the program to display. there are 5 different display modes',
            action ='extend',choices = [i for i in range(1,6)],nargs= 1,type=int,default=1)
    
    profiling.add_argument("--samplesize",dest='sampleSize',
            help='how many times to loop through the directory containing the grids. \
            Higher value means profiling takes longer, but will more precise timing info. Default value:10',action='store',nargs=1,
            type=int,default=[10])
    
    profiling.add_argument("--csv",dest='csvPath',
            help='the output path of the csv file containing timings if you would like to save it.',
            action='extend',nargs=1,type=str,default=[None])


    
    
    args: dict = vars(parser.parse_args())
    

    
    print(main(args))

