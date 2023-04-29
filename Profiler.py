import time
import matplotlib.pyplot as plt
import main
import os
from pathlib import Path
class Profiler():
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
    def startProfiling(self) -> None:
        list_of_paths = []
        timings = {}
        
        start_time = time.time()
        for i in os.listdir(self.input_path):
                list_of_paths.append([self.input_path+'\\'+i,self.output_path + '\\' + i])
        
        for i in list_of_paths:
            args = {'file_provided':i}
            start = time.time()
            try:
                print(self.solve(args))
            except:
                continue
            stop = time.time()
            print(f'time taken for grid "{i[0]}" : {round(stop-start,5)}s')

            timings.update({i[0]:stop-start})
        print(timings)
        
        

def profilinghandler(*args):
    profiler = Profiler(*args)
    profiler.startProfiling()
    return f'Profiling done! output saved to {profiler.output_path}'


if __name__ == '__main__':
    profiler = Profiler('grids')
    profiler.startProfiling()