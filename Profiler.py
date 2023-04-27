import time
import matplotlib.pyplot as plt
from  main import main

class Profiler():
    def __init__(self,input_path,output_path) -> None:
        self.input_path:  str  =  input_path
        self.output_path: str = output_path


def profilinghandler(*args):
    profiler = Profiler(*args)
    return f'Profiling done! output saved to {profiler.output_path}'