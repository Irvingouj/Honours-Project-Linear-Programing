import os
from pathlib import Path
from typing import List, Tuple
from io import TextIOWrapper
from linear_programming.classes import ObjectiveFunction, Constraints
from linear_programming.utils.types import Program

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
    file = open(file_path, 'r', encoding='utf-8')
    program = parse_file(file)
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
