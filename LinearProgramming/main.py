from io import TextIOWrapper
from typing import List, Tuple
from termcolor import colored
from LinearProgramming.Classes.Constraints import Constraints
from LinearProgramming.Classes.ObjectiveFunction import ObjectiveFunction
from LinearProgramming.Classes.Convex import Convex
from LinearProgramming.Classes.ConvexSolver import ConvexSolver
from LinearProgramming.Classes.OsToolSolver import OsToolSolver
import os

from LinearProgramming.Classes.Point import Point

bounded_prefix = "bounded_problem"
infeasible_prefix = "infeasible_problem"
unbounded_prefix = "unbounded_problem"

def main():
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "LinearPrograms",bounded_prefix + "9")
    file = open(file_path, 'r')
    program = parse_file(file);
    point = solve_with_convex(program)
    point2 = solve_with_os_tool(program)
    print("the maximum point is: Convex solver",point)
    print("the maximum point is: OS Solver ",point2)
    
def test_all():
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "LinearPrograms")
    for file in os.listdir(file_path):
        if file.startswith(bounded_prefix):
            print("testing file: ", file)
            test_file(file)

        if file.startswith(infeasible_prefix):
            print("testing file: ", file)
            test_file(file)

def test_file(file_name):
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "LinearPrograms",file_name)
    file = open(file_path, 'r')
    program = parse_file(file);
    point2 = solve_with_os_tool(program)
    try:
        point = solve_with_convex(program)
    except:
        if point2 is None:
            print("the problem is infeasible and the solver found it")
        else:
            print(colored("the problem is feasible but solution gives as infeasible", "red"))
    else:
        print("the maximum point is: Convex solver",point)
        print("the maximum point is: OS Solver ",point2)
        if point != point2:
            print(colored("the two solvers found different points", "red"))

def solve_with_convex(program) -> Point:
    solver = ConvexSolver()
    return solver.solve(program[0], program[1])
    
def solve_with_os_tool(program):
    solver = OsToolSolver()
    return solver.solve(program[0], program[1]) 


def parse_file(file:TextIOWrapper) -> Tuple[ObjectiveFunction,List[Constraints]]:
    lines = file.readlines()
    ## remove \n at the end of the line
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if len(line) > 0 and line[0] != '#' ]
    objective_function = ObjectiveFunction.from_string(lines[0])
    Constraints_list = []
    for line in lines[1:]:
        Constraints_list.append(Constraints.from_string(line))
    return objective_function, Constraints_list
    


if __name__ == "__main__":
    main()