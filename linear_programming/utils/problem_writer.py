import os
import random
from typing import List
from linear_programming.classes.two_d import *
from linear_programming.classes.three_d import *
from linear_programming.utils.linear_program_generator import LINEAR_PROGRAMS_DIR
from linear_programming.utils.problem_reader import PROJECT_ROOT
from linear_programming.utils.types import Program

def save_to_file(file_type:str,obj:ObjectiveFunction,constraints:List[Constraints])->str:
    assert file_type in ["bounded", "unbounded", "infeasible"]
    file_prefix = f"{file_type}_problem"
    
    files = [f for f in os.listdir(
        LINEAR_PROGRAMS_DIR) if f.startswith(file_prefix)]
    
    file_name = f"{file_prefix}{len(files)+1}"
    file_path = os.path.join(LINEAR_PROGRAMS_DIR, file_name)
    file = open(file_path, 'w', encoding='utf-8')
    file.write(f"# type = {file_type} problem generated randomly,n = {len(constraints)}\n")
    file.write(str(obj))
    for con in constraints:
        file.write("\n")
        file.write(str(con))
    file.close()
    return file_path   

def write_bad_program(program:Program, con_res:Point, os_res:Point, err,name = None):
    print("writing bad program")
    bad_program_dir = PROJECT_ROOT.joinpath("linear_program_data", "problems_unexpected")
    filename = f"{con_res}!={os_res}__{random.random()}.txt"
    if name is not None:
        filename = bad_program_dir.joinpath(f"{name}.txt")
    program_path = bad_program_dir.joinpath(filename)
    with open(program_path, 'a+',encoding='utf-8') as f:
        f.write("#" +str(err)+"\n")
        f.write(f"# convex result: {con_res} os tool result: {os_res}\n")
        f.write(str(program[0])+"\n")
        for line in program[1]:
            f.write(str(line)+"\n")
        f.write("#-----------------program end-----------------")

def write_bad_3d_program(program:Program):
    print("writing bad program")
    bad_program_dir = PROJECT_ROOT.joinpath("linear_program_data", "gogogo")
    filename = f"{random.random()}.txt"
    program_path = bad_program_dir.joinpath(filename)
    with open(program_path, 'a+',encoding='utf-8') as f:
        f.write(str(program[0])+"\n")
        for line in program[1]:
            f.write(str(line)+"\n")
        f.write("#-----------------program end-----------------")
      
def write_bad_program_no_analysis(program:Program, con_res:Point = None, os_res:Point = None, err = None,name = None):
    print("writing bad program")
    bad_program_dir = PROJECT_ROOT.joinpath("linear_program_data", "problems_unexpected")
    filename = f"{con_res}!={os_res}__{random.random()}.txt"
    if name is not None:
        filename = bad_program_dir.joinpath(f"{name}.txt")
    program_path = bad_program_dir.joinpath(filename)
    with open(program_path, 'a+',encoding='utf-8') as f:
        f.write("#" +str(err)+"\n")
        f.write(f"# convex result: {con_res} os tool result: {os_res}\n")
        f.write(str(program[0])+"\n")
        for line in program[1]:
            f.write(str(line)+"\n")
        f.write("#-----------------program end-----------------")

        
def write(relative_path,program:Program):
    program_path = PROJECT_ROOT.joinpath(relative_path)
    with open(program_path, 'a+',encoding='utf-8') as f:
        f.write(str(program[0])+"\n")
        for line in program[1]:
            f.write(str(line)+"\n")
        f.write("#-----------------program end-----------------")
    return program_path
        
def write_report(name,report):
    bad_program_dir = PROJECT_ROOT.joinpath("linear_program_data", "gogogo")
    filename = f"report_{name}.txt"
    program_path = bad_program_dir.joinpath(filename)
    with open(program_path, 'a+',encoding='utf-8') as f:
        for line in report:
            f.write(str(line)+"\n")