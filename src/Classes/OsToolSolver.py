from typing import List
from Classes.ObjectiveFunction import ObjectiveFunction
from Classes.Constraints import Constraints
from Classes.Convex import Convex
from Classes.Point import Point
from Classes.Solver import Solver
from Classes.OneDConstraint import OneDConstraint
from Classes import OneDLinearProgram
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
        
