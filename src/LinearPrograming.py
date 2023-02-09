from io import TextIOWrapper
from typing import List, Tuple

from Classes.Constraints import Constraints
from Classes.ObjectiveFunction import ObjectiveFunction
from Classes.Convex import Convex
from Classes.ConvexSolver import ConvexSolver
from Classes.OsToolSolver import OsToolSolver
import os

from Classes.Point import Point

bounded_prefix = "bounded_problem"
infeasible_prefix = "infeasible_problem"
unbounded_prefix = "unbounded_problem"

def main():
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "LinearPrograms",bounded_prefix + "1")
    file = open(file_path, 'r')
    program = parse_file(file);
    point = solve_with_convex(program)
    point2 = solve_with_os_tool(program)
    print("the maximum point is: Convex solver",point)
    print("the maximum point is: OS Solver ",point2)
    
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