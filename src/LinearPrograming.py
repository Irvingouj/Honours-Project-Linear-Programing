from io import TextIOWrapper
from typing import List, Tuple
from Classes.Constrains import Constrains
from Classes.ObjectiveFunction import ObjectiveFunction
from Classes.Convex import Convex
import os

def main():
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "LinearPrograms","bounded_problem1")
    file = open(file_path, 'r')
    program = parse_file(file)
    c:Convex = Convex([])
    for constrains in program[1]:
        c.add_edge(constrains.to_edge())
    edges = c.get_edges()

    for edge in edges:
        print(edge)
    print(c.find_optimal(program[0]))
    


def parse_file(file:TextIOWrapper) -> Tuple[ObjectiveFunction,List[Constrains]]:
    lines = file.readlines()
    ## remove \n at the end of the line
    lines = [line.strip() for line in lines]
    objective_function = ObjectiveFunction.from_string(lines[0])
    constrains = []
    for line in lines[1:]:
        constrains.append(Constrains.from_string(line))
    return objective_function, constrains
    


if __name__ == "__main__":
    main()