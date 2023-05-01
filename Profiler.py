import os
import time
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import main




class Profiler():
    """
    class for handling the perfomance logging of the solver for many different grids, 
    as well as multiple tries in the same grid. 

    """
    def __init__(self,args: dict) -> None:
        """
        sets up the profiler, by reading the input directory and making an output directory
        inside it for storing the grids and the output graphs to.
        """
        print(args)
        self.source_dir: str   = args['sourceDirectory'].pop() if args['sourceDirectory'] else None
        self.sample_size: int = args['sampleSize'] if args['sampleSize'] else None
        self.display_mode: int = args['displayMode'] if args['displayMode'] else None
        self.csv_path: str     = args['csvPath'].pop() if args['csvPath'] else None
        self.graph_path: str   = args['graphPath'].pop() if args['graphPath'] else None

        self.timings: dict = {}
        self.solve = main.main
        self.output_path = Path(self.source_dir+'\\output')

        if not self.output_path.is_dir():
            self.output_path.mkdir()
        else:
            for child in self.output_path.iterdir():
                child.unlink()

        self.output_path = str(self.output_path)


    def single_pass(self,list_of_paths):
        """
        runs through the solving algorithm for each grid exactly once, and returns
        the time taken in the form of a nested list, with the filenames added to keep track
        of which timing is which.
        """
        timing_list = []
        for i in list_of_paths:
            #go through each filename and solve
            start_time = time.time()
            #the actual solving part \/\/
            print(self.solve({'file_provided':i}))
            time_taken = time.time()-start_time
            timing_list.append([i[0],time_taken])
        return timing_list

    def start_profiling(self) -> dict:
        """
        main profiling function. executes the solver for each grid in the folder x amount of times 
        and returns the time taken in the form of a dict, with the keys being the paths to each grid
        and the values being a list of the time taken for each "pass" of the grid.
        """
        list_of_paths = []



        #disgustingly long listcomp ahead
        list_of_paths = [
            [self.source_dir+'\\'+ i,self.output_path + '\\' + i] for
            i in [j for j in os.listdir(self.source_dir) if j != 'output']
                         ]

        timings = {filename[0]:[]for filename in list_of_paths} #creating empty dict of the results
        #dict will have filenams as keys, and temporarily an empty list as a placeholder value

        annoyingly_huge_list = []
        #program will spend most of its execution time on this loop.
        #runs each solver x times according to value in range()
        for i in range(self.sample_size):
            print('\n----------------------------------')
            print(f'\tPASS {i+1}:')
            print('----------------------------------\n')
            annoyingly_huge_list.append(self.single_pass(list_of_paths))

        for i in annoyingly_huge_list:
            for j in i:
                timings[j[0]].append(j[1])
        self.timings = timings
        return timings

    def write_to_csv(self) -> str:
        temp_list = [i.insert(0,list(self.timings.keys())[ind]) for ind,i in enumerate(self.timings.values())]
        print(temp_list)
        return f'Write completed succesfully! csv is located in {self.csv_path}'



def profilinghandler(args: dict):
    """
    main entry point for the profiler sub-program.
    takes the command line arguments relevant to the profiler, parses them and does operations 
    as required. probably better if included in the Profiler class instead of 
    being a standalone function.
    """
    #create profiler object
    
    profiler = Profiler(args)

    
    print('STARTING PROFILING...')
    #delay, get ready for terminal spam!
    print('---------------------------------------')
    time.sleep(0.5) 
    # integer arg is amount of times to run over the list of grids.
    dict_of_results:dict = profiler.start_profiling()
    if profiler.csv_path:
        profiler.write_to_csv()

    #profiler.display_graph()
    
    fig, ax = plt.subplots()
    ax.boxplot(dict_of_results.values(),labels=dict_of_results.keys())
    print(f'Profiling done! output saved to {profiler.output_path}')
    time.sleep(0.5)
    print('Showing graph...')
    plt.show()
    return 'Finished execution! graphing and data export complete.'


if __name__ == '__main__':
    profilinghandler('grids')



    """
    args to add
    --graph {path}.pngsave output graphs to file
    --display {int}cycle graphs to display ( int)
    --csv profiling data to csv
    ""
    
    
    """
