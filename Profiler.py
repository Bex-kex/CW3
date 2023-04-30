import os
import time
from pathlib import Path
import matplotlib.pyplot as plt
import main




class Profiler():
    """
    class for handling the perfomance logging of the solver for many different grids, 
    as well as multiple tries in the same grid. 

    """
    def __init__(self,input_path) -> None:
        """
        sets up the profiler, by reading the input directory and making an output directory
        inside it for storing the grids and the output graphs to.
        """
        self.input_path:  str  =  input_path
        self.solve = main.main
        self.output_path = Path(self.input_path+'\\output')
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

    def start_profiling(self, number_of_passes:int) -> dict:
        """
        main profiling function. executes the solver for each grid in the folder x amount of times 
        and returns the time taken in the form of a dict, with the keys being the paths to each grid
        and the values being a list of the time taken for each "pass" of the grid.
        """
        list_of_paths = []



        #disgustingly long listcomp ahead
        list_of_paths = [
            [self.input_path+'\\'+ i,self.output_path + '\\' + i] for
            i in [j for j in os.listdir(self.input_path) if j != 'output']
                         ]

        timings = {filename[0]:[]for filename in list_of_paths} #creating empty dict of the results
        #dict will have filenams as keys, and temporarily an empty list as a placeholder value

        annoyingly_huge_list = []
        #program will spend most of its execution time on this loop.
        #runs each solver x times according to value in range()
        for i in range(number_of_passes):
            print('\n----------------------------------')
            print(f'\tPASS {i+1}:')
            print('----------------------------------\n')
            annoyingly_huge_list.append(self.single_pass(list_of_paths))

        for i in annoyingly_huge_list:
            for j in i:
                timings[j[0]].append(j[1])
        return timings





def profilinghandler(args):
    """
    main entry point for the profiler sub-program.
    takes the command line arguments relevant to the profiler, parses them and does operations 
    as required. probably better if included in the Profiler class instead of 
    being a standalone function.
    """
    #create profiler object
    profiler = Profiler(args['sourceDirectory'].pop())
    print('successfully made profiler object')
    print('STARTING PROFILING...')
    #delay, get ready for terminal spam!
    time.sleep(0.5) 
    print('---------------------------------------')
    # integer arg is amount of times to run over the list of grids.
    dict_of_results:dict = profiler.start_profiling(args['sampleSize'].pop())
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
