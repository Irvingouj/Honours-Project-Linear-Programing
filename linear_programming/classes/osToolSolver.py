from typing import List
from .edge import Edge
from .point import Point
from .line import Line
from .objectiveFunction import ObjectiveFunction,MaxOrMin
from .constraints import Constraints
from .oneDConstraint import OneDConstraint
from .oneDLinearProgram import solve_1d_linear_program
from .solver import Solver

from ortools.linear_solver import pywraplp

class OsToolSolver(Solver):
    def solve(self, obj:ObjectiveFunction, cons:List[Constraints]) -> Point:
        solver = pywraplp.Solver.CreateSolver('GLOP')
        if not solver:
            return
        
        x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
        y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')
 

        for c in cons:
            solver.Add(eval(c.to_or_string()))

        solver.Maximize(eval(obj.to_or_string()))

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            return Point(x.solution_value(),y.solution_value())
        
        return None
        
