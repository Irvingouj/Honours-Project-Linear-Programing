from io import TextIOWrapper
from typing import List, Tuple

from LinearProgramming.Classes.Constraints import Constraints
from LinearProgramming.Classes.ObjectiveFunction import ObjectiveFunction
from LinearProgramming.Classes.ConvexSolver import ConvexSolver
import os

from LinearProgramming.Classes.Point import Point

bounded_prefix = "bounded_problem"
infeasible_prefix = "infeasible_problem"
unbounded_prefix = "unbounded_problem"

def main():
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "LinearPrograms",bounded_prefix + "3")
    file = open(file_path, 'r')
    point = solve_with_convex(file)
    print("the maximum point is ",point)
    
def solve_with_convex(file:TextIOWrapper) -> Point:
    program = parse_file(file)
    solver = ConvexSolver()
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