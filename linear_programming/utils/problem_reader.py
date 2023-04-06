import os
from pathlib import Path
from typing import List, Tuple
from io import TextIOWrapper
from linear_programming.classes import ObjectiveFunction, Constraints
from linear_programming.classes.three_d.constraint_3d import Constraints3D
from linear_programming.classes.three_d.objective_function_3d import ObjectiveFunction3D
from linear_programming.utils.types import Program, Program3d
import pathlib

BOUNDED_PREFIX = "bounded_problem"
INFEASIBLE_PREFIX = "infeasible_problem"
UNBOUNDED_PREFIX = "unbounded_problem"
PROGRAM_DATA_DIR_NAME = "linear_program_data"
PROJECT_ROOT = Path(__file__).parent.parent.parent

class ProblemType:
    BOUNDED = "bounded"
    INFEASIBLE = "infeasible"
    UNBOUNDED = "unbounded"


def read_problem(p_type:ProblemType ,problem_number):
    prefix = f"{p_type}_problem"
    file_path = os.path.join(
        PROJECT_ROOT, PROGRAM_DATA_DIR_NAME, prefix + str(problem_number))
    file = open(file_path, 'r', encoding='utf-8')
    program = parse_file(file)
    return program


def read_unexpected_problem(filename: str) -> Program:
    file_path = os.path.join(
        PROJECT_ROOT, PROGRAM_DATA_DIR_NAME, 'problems_unexpected', filename)
    if not os.path.isfile(file_path):
        file_path = os.path.join(
        PROJECT_ROOT, PROGRAM_DATA_DIR_NAME, 'problems_unexpected', filename+".txt")
    if not os.path.isfile(file_path):
        file_path = os.path.join(
        PROJECT_ROOT, PROGRAM_DATA_DIR_NAME, 'problems_unexpected', filename.removesuffix(".txt"))
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {filename} not found")
            
    file = open(file_path, 'r', encoding='utf-8')
    program = parse_file(file)
    return program

def parse_file_3d(file: TextIOWrapper) -> Program3d:
    def parse_objective_function_3d(line: str) -> ObjectiveFunction3D:
        line = line.strip()
        line = line.removesuffix(";")
        line = line.removesuffix(" ")
        line = line.removesuffix("\n")
        return ObjectiveFunction3D.from_string(line)
        
    def parse_constraints_3d(lines: List[str]) -> List[Constraints3D]:
        constraints_list = []
        for line in lines:
            line = line.strip()
            line = line.removesuffix(";")
            line = line.removesuffix(" ")
            line = line.removesuffix("\n")
            constraints_list.append(Constraints3D.from_string(line))
        return constraints_list
    
    lines = file.readlines()
    lines = [l for l in lines if len(l) > 0 and l[0] != '#' and l[0] != '\n']
    obj = parse_objective_function_3d(lines[0])
    cons = parse_constraints_3d(lines[1:])
    return obj, cons

def read_unexpected_problem_3d(filename: str) -> Program3d:
    file_path = os.path.join(
        PROJECT_ROOT, PROGRAM_DATA_DIR_NAME, 'problems_unexpected', filename)
    if not os.path.isfile(file_path):
        file_path = os.path.join(
        PROJECT_ROOT, PROGRAM_DATA_DIR_NAME, 'problems_unexpected', filename+".txt")
    if not os.path.isfile(file_path):
        file_path = os.path.join(
        PROJECT_ROOT, PROGRAM_DATA_DIR_NAME, 'problems_unexpected', filename.removesuffix(".txt"))
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {filename} not found")
            
    file = open(file_path, 'r', encoding='utf-8')
    program = parse_file_3d(file)
    
    return program

def parse_file(file: TextIOWrapper) -> Tuple[ObjectiveFunction, List[Constraints]]:
    lines = file.readlines()
    # remove \n at the end of the line
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if len(line) > 0 and line[0] != '#']
    objective_function = ObjectiveFunction.from_string(lines[0])
    constraints_list = []
    for line in lines[1:]:
        constraints_list.append(Constraints.from_string(line))
    return objective_function, constraints_list

def read_all_problem_in_dir(dir_name: str) -> List[Program]:
    dir_path = os.path.join(PROJECT_ROOT, PROGRAM_DATA_DIR_NAME, dir_name)
    files = os.listdir(dir_path)
    programs = []
    for file in files:
        file_path = os.path.join(dir_path, file)
        file = open(file_path, 'r', encoding='utf-8')
        program = parse_file(file)
        programs.append((file.name,program))
    return programs

    
def read(path,dimension):
    file_path = os.path.join(PROJECT_ROOT,path)
    file = open(file_path, 'r', encoding='utf-8')
    
    if dimension == 2:
        program = parse_file(file)
        return program
    if dimension == 3:
        program = parse_file_3d(file)
        return program
    
    raise ValueError("Dimension must be 2 or 3")