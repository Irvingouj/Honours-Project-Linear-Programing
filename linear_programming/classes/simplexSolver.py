from typing import List
from .edge import Edge
from .point import Point
from .line import Line
from .objectiveFunction import ObjectiveFunction, MaxOrMin
from .constraints import Constraints
from .oneDConstraint import OneDConstraint
from .oneDLinearProgram import solve_1d_linear_program
from .solver import Solver


class SimplexSolver(Solver):
    def solve(self, obj: ObjectiveFunction, cons: List[Constraints]) -> Point:
        pass
