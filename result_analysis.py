from typing import Dict, List, Tuple
from sklearn.linear_model import LinearRegression
import os
import pathlib
import re
import matplotlib.pyplot as plt
import numpy as np

curr_dir = pathlib.Path(__file__).parent.absolute()
data_dir = curr_dir.joinpath('time_data')

row = Tuple[int,float,float]
file_data = List[row]

def read_data(type:str):
    """
    this method will read the data from the file
    """
    file_name_pattern = type+"_result_\d{1,2}.txt"
    file_list = os.listdir(data_dir)
    target_list = [file for file in file_list if re.fullmatch(file_name_pattern,file) != None]
    data_list:file_data = []
    for file in target_list:
        single_file_data:file_data = []
        with open(data_dir.joinpath(file),'r',encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line == '' or line.startswith('n'):
                    continue
                line = line.split(',')
                single_file_data.append((int(line[0]),float(line[1]),float(line[2])))
            
        data_list.append(single_file_data)
    return data_list

def find_mean_between_files(files_data:List[file_data]) -> Tuple[List[Tuple[int,float]],List[Tuple[int,float]]]:
    convex_for_each_n:Dict[int,List[float]] = {}
    or_for_each_n:Dict[int,List[float]] = {}
    for file in files_data:
        for row in file:
            n,convex,or_ = row
            if n not in convex_for_each_n:
                convex_for_each_n[n] = []
                or_for_each_n[n] = []
            convex_for_each_n[n].append(convex)
            or_for_each_n[n].append(or_)
            
    mean_data_con:Tuple[int,float] = []
    for n,con_data in convex_for_each_n.items():
        mean = sum(con_data)/len(con_data)
        mean_data_con.append((n,mean))
        
    mean_data_or:Tuple[int,float] = []
    for n,or_data in or_for_each_n.items():
        mean = sum(or_data)/len(or_data)
        mean_data_or.append((n,mean))
        
    return mean_data_con,mean_data_or

problem = 'infeasible'

res = read_data(problem)
mean_data_con,mean_data_or = find_mean_between_files(res)
x_value = [x[0] for x in mean_data_con]
y_value = [x[1] for x in mean_data_con]

x_value_or = [x[0] for x in mean_data_or]
y_value_or = [x[1] for x in mean_data_or]

X_con = [[i] for i in x_value]

model = LinearRegression().fit(X_con,y_value)
score = model.score(X_con,y_value)
slope = model.coef_[0]

x_plot = np.linspace(min(x_value), max(x_value), len(x_value))
y_plot = model.predict(x_plot.reshape(-1, 1))

# Plot the regression line
plt.plot(x_plot, y_plot,color='red',label=f'linear regression, score={score.round(5)},slope={slope.round(5)}')



# Add axis labels and a title
plt.xlabel('n')
plt.ylabel('time')
plt.title(f'Compare between convex and or_tools for {problem} problem')
plt.scatter(x_value,y_value,label='convex')
plt.scatter(x_value_or,y_value_or,label='or_tools')
plt.legend()

# Display the plot
plt.show()

# print(mean_data_con)