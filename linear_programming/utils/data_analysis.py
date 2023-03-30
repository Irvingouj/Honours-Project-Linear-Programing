import pandas as pd
import matplotlib.pyplot as plt
from .problem_reader import PROJECT_ROOT
import pathlib

def plot_data(file_name:str):
    bounded_file = pathlib.Path(PROJECT_ROOT, "time_data", file_name)
    bounded_data = open(bounded_file, "r")
    data = [[], [], []]
    for line in bounded_data:
        if line.startswith("\n") or line.startswith("n"):
            continue
        
        line = line.split(",")
        print(line)
        data[0].append(int(line[0]))
        data[1].append(float(line[1]))
        data[2].append(float(line[2]))
    
    data_arr = [data[0][1:], data[1][1:], data[2][1:]]
    x = data_arr[0]
    y = data_arr[1]
    z = data_arr[2]

    plt.title("Time comparison for " + file_name)
    plt.plot(x, y, label="Convex")
    plt.plot(x, z, label="OsTool")

    plt.legend()
    plt.show()
