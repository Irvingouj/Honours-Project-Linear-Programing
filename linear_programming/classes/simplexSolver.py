from typing import List
from .point import Point
from .objectiveFunction import ObjectiveFunction, MaxOrMin
from .constraints import Constraints
from .solver import Solver


class SimplexSolver(Solver):
    def solve(self, obj: ObjectiveFunction, cons: List[Constraints]) -> Point:
        pass
