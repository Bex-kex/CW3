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
        print(args) #debug

        #storing command line args to profiler object
        self.source_dir: str   = args['sourceDirectory'].pop()
        self.sample_size: int = args['sampleSize'].pop()
        self.display_mode: int = args['displayMode'].pop()
        self.csv_path: str     = args['csvPath'].pop() 
        self.graph_path: str   = args['graphPath'].pop() 
        self.timings: dict = {}
        self.solve = main.main
        self.output_path = Path(self.source_dir+'\\output')
        # setup output path
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
        timing_list_wavefront = []
        timing_list_recursive = []
        for i in list_of_paths:
            #go through each filename and solve
            start_time = time.time()
            #the actual solving part \/\/
            print(self.solve({'file_provided':i,'solverChoice':'wavefront'}))
            #get the time taken for the grid using the wavefront solver
            time_taken = time.time()-start_time
            timing_list_wavefront.append([i[0],time_taken])
            start_time = time.time()
            print(self.solve({'file_provided':i,'solverChoice':'recursive'}))
            #get the time taken for the grid using the recursive solver
            time_taken = time.time() - start_time
            timing_list_recursive.append([i[0],time_taken])
        return timing_list_wavefront, timing_list_recursive

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
            i in [j for j in os.listdir(self.source_dir) if j != 'output'] # generates a list of the paths to each grid in the directory.
                         ]

        dict_wavefront = {filename[0]:[] for filename in list_of_paths} #creating empty dict of the results
        #dict will have filenames as keys, and temporarily an empty list as a placeholder value
        dict_recursive = deepcopy(dict_wavefront)
        annoyingly_huge_list = []
        #program will spend most of its execution time on this loop.
        #runs each solver x times according to value in range()
        for i in range(self.sample_size):
            print('\n----------------------------------')
            print(f'\tPASS {i+1}:')
            print('----------------------------------\n')
            wavefront_timings,recursive_timings = self.single_pass(list_of_paths)
            #append results to a dictionary for each solver.
            for i in wavefront_timings:
                dict_wavefront[i[0]].append(i[1])
            
            for j in recursive_timings:
                dict_recursive[j[0]].append(j[1])


        self.wavefront_results = dict_wavefront
        self.recursive_results = dict_recursive    
        
        return dict_wavefront,dict_recursive

    def write_to_csv(self) -> str:
        """
        function for writing test results to a csv, if a path has been provided.
        """
        recursive_results = []
        wavefront_results = []
        #make a copy of the results so to not affect the existing results when formatting.
        copied_wavefront = deepcopy(self.wavefront_results)
        copied_recursive = deepcopy(self.recursive_results)
        for i in list(copied_wavefront.keys()):
            #convert all values to a string and add the file path to the start of the list
            tmp_list = [str(j)for j in copied_wavefront[i]]
            tmp_list.insert(0,i)
            wavefront_results.append(tmp_list)

        for j in list(copied_recursive.keys()):
            #convert all values to a string and add the file path to the start of the list
            tmp_list = [str(k) for k in copied_recursive[j]]
            tmp_list.insert(0,j)
            recursive_results.append(tmp_list)
        #recursive_results and wavefront_results now ready to write to file.

        header = ['pass '+ str(i) for i in range(1,self.sample_size+1)] #making a simple header
        header.insert(0,'File Path')
        try:
            with open(self.csv_path,'w',newline='') as file:
                #write all the information to the csv file
                writer = csv.writer(file)
                writer.writerow(["WAVEFRONT MODE"])
                writer.writerow(header)
                writer.writerows(wavefront_results)
                writer.writerow(["RECURSIVE MODE"])
                writer.writerow(header)
                writer.writerows(recursive_results)
        except OSError:
            return 'Write unable to complete! moving on...'

        
        return f'Write completed succesfully! csv is located in {self.csv_path}'

    def display_graph(self):
        """
        function used to generate graphs of the data that has been recorded during profiling.
        able to switch between different display modes with the -graphmode flag.
        """
        data1,data2 = deepcopy(self.wavefront_results), deepcopy(self.recursive_results)
        def create_average(data_dict: dict):
                    for i in list(data_dict.keys()):
                        list_to_average = data_dict[i]
                        average = sum(list_to_average)/len(list_to_average)
                        data_dict[i] = average
                    return data_dict
        
        match self.display_mode:
            case 1:
                """
                BAR CHART OF AVERAGE SOLVING TIME ACROSS DIFFERENT GRIDS.
                """
                
                #get the average time to complete each graph.
                data1 = create_average(data1)
                data2 = create_average(data2)
                #make the figure
                fig,ax = plt.subplots()
                width = 0.4
                #align the data so it is halfway past each tick.
                data1_x = [x-0.5*width for x in range(len(list(data1.keys())))]
                data2_x = [x+0.5*width for x in range(len(list(data2.keys())))]
                #convert the times from seconds to milliseconds.
                data1_y = [y*1000 for y in list(data1.values())]
                data2_y = [y*1000 for y in list(data2.values())]

                #ternary operator to determine the absolute maximum solving time across both solvers.
                max_y_value = max(data1_y) if max(data1_y) > max(data2_y) else max(data2_y)
                
                #label each tick with the grid path
                label_list = list(data1.keys())
                #set the x tick formats
                ax.set_xticks([x for x in range(len(list(data1.keys())))],label_list)
                #convert the max y value to an int rounded to the nearest hundred, so the y axis is well formatted.
                max_y_value = int((max_y_value // 100 * 100) + 200)
                
                #plot the actual bars
                ax.bar(data1_x,data1_y,width,label='Wavefront Algorithm')
                ax.bar(data2_x,data2_y,width,label='Recursive Algorithm')
                #adjust the y axis so the correct y range is shown
                ax.set_yticks([y for y in range(0,max_y_value,100)])
                #label each part of the grid, show legend and eventually show the graph.
                ax.set_ylabel('Time to solve(ms)')
                ax.set_xlabel('Grid path')
                ax.set_title(f'Average solving time of grids in "{self.source_dir}" for different solving algorithms.')
                ax.legend()
                
            case 2:
                """
                PIE CHART OF DIFFERENT SOLVING TIMES AS A PERCENTAGE OF TOTAL SOLVING TIME.
                """
                #get average solving time for each grid
                data1 = create_average(data1)
                data2 = create_average(data2)
                #create subplots
                fig, axs = plt.subplots(1,2)
                data =[data1,data2]
                for i,pies in enumerate(axs):
                    #generate a pie chart for each solver
                    pies: plt.Axes
                    pies.pie(list(data[i].values()),labels=list(data[i].keys()),radius=1.25,autopct='%.2f')
                    #set the subtitle of each chart
                    if i == 0: pies.set_title('Wavefront Solver',y=0.05)
                    else: pies.set_title('Recursive Solver',y=0.05)
                
                #main title
                fig.suptitle(f'Share of total time taken for each grid in "{self.source_dir}"')


            case 3:...
            case 4:...
            case 5:...
            
        if self.graph_path:
            plt.savefig(self.graph_path,dpi=900)
            plt.show()
            return f'Graph saved to {self.graph_path}!'
        else:
            plt.show()
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
    # start the profiler
    profiler.start_profiling()

    if profiler.csv_path:
        #write to a csv if a path has been specified
        print(profiler.write_to_csv())
    #display the graphs.
    profiler.display_graph()


    return 'Finished execution! graphing and data export complete.'

