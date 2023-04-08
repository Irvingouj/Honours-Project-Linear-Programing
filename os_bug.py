from ortools.linear_solver import pywraplp
from typing import List, Union
from linear_programming.utils.exceptions import PerceptionException



param = pywraplp.MPSolverParameters()
param.SetIntegerParam(pywraplp.MPSolverParameters.PRESOLVE, pywraplp.MPSolverParameters.PRESOLVE_OFF)
solver = pywraplp.Solver.CreateSolver('GLOP')
x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')


solver.Add(x + y <= 1)
solver.Add(x - y <= 3)
solver.Add(-x - 0.5 * y >= -2)

solver.Minimize(-x - y)

status = solver.Solve(param)
print(status == pywraplp.Solver.OPTIMAL)
print(f"OS: {x.solution_value(), y.solution_value()}")