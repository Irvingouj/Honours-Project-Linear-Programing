from typing import List
from Classes.ObjectiveFunction import ObjectiveFunction
from Classes.Constraints import Constraints
from Classes.Point import Point
from Classes.Solver import Solver

class SimplexSolver(Solver):
    def solve(self, obj:ObjectiveFunction, cons:List[Constraints]) -> Point:
        pass