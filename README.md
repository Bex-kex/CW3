# README
## To Run:

  Run **"python main.py"**  in the source directory, with or without any of the optional flags listed below.
As this program uses the Argparse module, all help on flags is also present in the command line. Simply add **-h** or **--help** to the command-line arguments when running the program.
**TO CHECK TASK 1**
to check the solver for task 1, use the flag **--solver recursive** , in order to select the solver that has been written according to task 1. \n
**TO CHECK TASK 3**
the default solving algorithm it 'wavefront', which is the solver completed in task 3. However you can force use it by using **--solver wavefront**
  ## Flags:
  

 -  **-h, --help:** Display the help for each flag.
 
 - **-f, --file: Takes 2 positional arguments {str,str}.** Import a grid from a text file, solve it, then write it to a separate output file, with or without an explanation.
 
 - **-ht, --hint: Takes 1 positional argument {int}.** Only fill in the grid with the specified amount of empty cells filled. Can be combined with -e and ---file.
 
 - **-e, --explain: Toggle.** Add an explanation to the end of the grid which provides instructions on which numbers to put in each empty space. 
 
 - **-s,--solver: {str}. Takes 1 positional argument. Defaults to *'wavefront'*.** Choose a specific solving algorithm to solve the grid.
 
 NOTE: if no --file flag is provided, the program will default to one of the built-in grids, and print the solved grid, including any explanation, to the grid.
 ## Profiling mode:
 Access Profiling mode by using the keyword "profiling" as the first argument. E.G: **python main.py profiling -dir {str} {optional flags}**.
 
  **NOTE**: The above arguments will have no effect in profiling mode.
 The flag ---dir is required in order to run profiling mode.
 ## Profiling specific flags:
  -  **-h, --help:** Display the help for each flag.
  
  - **-dir, --directory: {str}. Takes 1 positional argument.** Specify the directory name which contains the test grids. Required argument.
  
 - **--display: {int} 1-5. Takes 1 positional argument.** Choose a display mode for the output graph, default 1. The integer input determines which display mode you choose.
 
 - **--samplesize: {int}. Takes 1 positional argument. Defaults to 10.** Adjust the sample size of the profiler. Adjusting this value higher means the profiler will solve each grid more times, meaning the average is more accurate, but may take longer to execute. Lowering this value means the profiler will solve each grid a fewer number of times, increasing performance at the expense of a potentially less accurate average.
 
 - **--csv: {str}. Takes 1 positional argument.** Write the results of the profiler to the path specified.
 
 - **-g, --graph: {str}. Takes 1 positional argument.** Save the output graph as a PNG to the path specified.


