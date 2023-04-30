import time
import matplotlib.pyplot as plt
import main
import os
from pathlib import Path


class Profiler():
    """
    class for handling the perfomance logging of the solver for many different grids, 
    as well as multiple tries in the same grid. 

    """
    def __init__(self,input_path) -> None:
        """
        sets up the profiler, by reading the input directory and making an output directory inside it, for storing the grids and the output graphs to.
        """
        self.input_path:  str  =  input_path
        self.solve: function = main.main
        self.output_path = Path(self.input_path+'\\output')
        if not self.output_path.is_dir():
            self.output_path.mkdir()
        else:
            for child in self.output_path.iterdir():
                child.unlink()
            
            

        self.output_path = str(self.output_path)
    

    def singlePass(self,list_of_paths):
        """
        runs through the solving algorithm for each grid exactly once, and returns
        the time taken in the form of a nested list, with the filenames added to keep track
        of which timing is which.
        """
        ls = []
        for i in list_of_paths:
            #go through each filename and solve
            start_time = time.time()
            #the actual solving part \/\/
            print(self.solve({'file_provided':i}))
            time_taken = time.time()-start_time
            ls.append([i[0],time_taken])
        return ls

    def startProfiling(self) -> dict:
        list_of_paths = []
        
        
        start_time = time.time()
        #disgustingly long listcomp ahead
        list_of_paths = [
            [self.input_path+'\\'+ i,self.output_path + '\\' + i] for 
            i in [j for j in os.listdir(self.input_path) if j != 'output']
                         ]
        timings = {filename[0]:[]for filename in list_of_paths}
        
        print(timings)

        annoyingly_huge_list = [self.singlePass(list_of_paths)for i in range(10)]
        out1 = []
        for i in annoyingly_huge_list:
            for j in i:
                timings[j[0]].append(j[1])
        return timings
        
        
        
        

def profilinghandler(*args):
    print(*args)
    profiler = Profiler(*args)
    print('STARTING PROFILING...')
    time.sleep(0.5)
    print('---------------------------------------')
    dict_of_results:dict = profiler.startProfiling()
    fig, ax = plt.subplots()
    ax.boxplot(dict_of_results.values(),labels=dict_of_results.keys())
    plt.show()
    return f'Profiling done! output saved to {profiler.output_path}'


if __name__ == '__main__':
    profilinghandler('grids')



    """
    args to add
    --graph {path}.pngsave output graphs to file
    --display {int}cycle graphs to display ( int)
    --csv profiling data to csv
    ""
    
    
    """