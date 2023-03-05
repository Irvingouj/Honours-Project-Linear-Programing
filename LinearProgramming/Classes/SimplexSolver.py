from typing import List
from LinearProgramming.Classes.ObjectiveFunction import ObjectiveFunction
from Classes.Constraints import Constraints
from LinearProgramming.Classes.Point import Point
from Classes.Solver import Solver

class SimplexSolver(Solver):
    def solve(self, obj:ObjectiveFunction, cons:List[Constraints]) -> Point:
        pass