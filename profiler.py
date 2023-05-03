import os
import time
import csv
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from copy import deepcopy
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
        self.source_dir: str   = args['sourceDirectory'].pop()
        self.sample_size: int = args['sampleSize'].pop()
        self.display_mode: int = args['displayMode']
        self.csv_path: str     = args['csvPath'].pop() 
        self.graph_path: str   = args['graphPath'].pop() 

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
            print(self.solve({'file_provided':i,'solverChoice':'wavefront'}))
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
        temp_list = []
        copied_dict = deepcopy(self.timings)
        for ind,i in enumerate(copied_dict.values()):
            key = list(copied_dict.keys())[ind]
            values = i
            values.insert(0,key)
            temp_list.append(values)

        temp_list = list(np.array(temp_list).transpose())
        temp_list = [list(i) for i in temp_list]
        temp_list[0].insert(0,'pass_number')

        for ind,i in enumerate(temp_list[1:]):
            i.insert(0,str(ind+1))
        try:
            with open(self.csv_path,'w',newline='') as file:
                writer = csv.writer(file)
                
                writer.writerows(temp_list)
        except OSError:
            return 'Write unable to complete! moving on...'

        
        return f'Write completed succesfully! csv is located in {self.csv_path}'

    def display_graph(self):
        data = self.timings
        match self.display_mode:
            case 1:
                fig,axs = plt.subplots(1,len(data.keys()))
                data_list = list(data.values())

                label_list = list(data.keys())
                fig.suptitle(f'Box plot of solver performance for each grid in "{self.source_dir}"')
                fig.supxlabel('Grid path')
                fig.supylabel('Time to solve (ms)')
                for ind,i in enumerate(axs):

                    i: plt.Axes
                    data_list_ms = [round(i*1000,2)for i in data_list[ind]]
                    i.boxplot(data_list_ms,showmeans=True)
                    i.set_xlabel(label_list[ind])
                plt.show()
            case 2:...
            case 3:...
            case 4:...
            case 5:...
        if self.graph_path:
            plt.savefig(self.graph_path,dpi=900)
            return f'Graph saved to {self.graph_path}!'
        else:
            return
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
    profiler.start_profiling()

    if profiler.csv_path:
        print(profiler.write_to_csv())

    profiler.display_graph()


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
