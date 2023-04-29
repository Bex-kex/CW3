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
        self.input_path:  str  =  input_path
        self.solve: function = main.main
        self.output_path = Path(self.input_path+'\\output')
        if not self.output_path.is_dir():
            self.output_path.mkdir()
        else:
            for child in self.output_path.iterdir():
                child.unlink()
            print([i for i in self.output_path.iterdir()])
            

        self.output_path = str(self.output_path)
    

    def singlePass(self,list_of_paths):
        ls = []
        for i in list_of_paths:
            start_time = time.time()
            print(self.solve({'file_provided':i}))
            time_taken = time.time()-start_time
            ls.append([i[0],time_taken])
        return ls

    def startProfiling(self) -> None:
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
    profiler = Profiler(*args)
    dict_of_results = profiler.startProfiling()
    return f'Profiling done! output saved to {profiler.output_path}'


if __name__ == '__main__':
    profilinghandler('grids')