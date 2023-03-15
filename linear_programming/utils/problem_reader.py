from pathlib import Path
from typing import List, Tuple
from io import TextIOWrapper
from linear_programming.classes import ObjectiveFunction, Constraints
import os

bounded_prefix = "bounded_problem"
infeasible_prefix = "infeasible_problem"
unbounded_prefix = "unbounded_problem"
program_data_dir_name = "linear_program_data"
project_root = Path(__file__).parent.parent.parent


def read_bounded_problem(problem_number):
    file_path = os.path.join(
        project_root, program_data_dir_name, bounded_prefix + str(problem_number))
    file = open(file_path, 'r')
    program = parse_file(file)
    return program


def read_infeasible_problem(problem_number):
    file_path = os.path.join(
        project_root, program_data_dir_name, infeasible_prefix + str(problem_number))
    file = open(file_path, 'r')
    program = parse_file(file)
    return program

def read_unexpected_problem(filename: str):
    file_path = os.path.join(
        project_root, program_data_dir_name, 'problems_unexpected', filename)
    file = open(file_path, 'r', encoding='utf-8')
    program = parse_file(file)
    return program


Program = Tuple[ObjectiveFunction, List[Constraints]]


def parse_file(file: TextIOWrapper) -> Tuple[ObjectiveFunction, List[Constraints]]:
    lines = file.readlines()
    # remove \n at the end of the line
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if len(line) > 0 and line[0] != '#']
    objective_function = ObjectiveFunction.from_string(lines[0])
    Constraints_list = []
    for line in lines[1:]:
        Constraints_list.append(Constraints.from_string(line))
    return objective_function, Constraints_list
