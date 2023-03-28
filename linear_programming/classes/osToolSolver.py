from ortools.linear_solver import pywraplp
from typing import List, Union
from .point import Point
from .objectiveFunction import ObjectiveFunction
from .constraints import Constraints
from .one_d.one_d_constraint import OneDConstraint
from .solver import Solver
from .three_d import Constraints3D, ObjectiveFunction3D, Point3D



class OsToolSolver(Solver):
    def solve(self, obj: ObjectiveFunction, cons: List[Constraints]) -> Point:
        solver = pywraplp.Solver.CreateSolver('GLOP')
        
        if not solver:
            raise Exception('Could not create solver')

        x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
        y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')

        for c in cons:
            solver.Add(eval(c.to_or_string()))

        solver.Maximize(eval(obj.to_or_string()))

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            return Point(x.solution_value(), y.solution_value())
        if status == pywraplp.Solver.INFEASIBLE:
            return "INFEASIBLE"
        if status == pywraplp.Solver.UNBOUNDED:
            return "UNBOUNDED"

    def solve_one_dimension(self, one_d_constraints: List[OneDConstraint], objective: bool) -> float:
        solver = pywraplp.Solver.CreateSolver('GLOP')
        if not solver:
            raise Exception('Could not create solver')
        
        x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
        for con in one_d_constraints:
            solver.Add(eval(str(con)))
            
        solver.Maximize(x if objective else -x)
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            return x.solution_value()
        
        return None

    result_type = Union[Point3D,"UNBOUNDED","INFEASIBLE"]
    def solve_three_d(self,obj:ObjectiveFunction3D,three_d_cons:List[Constraints3D]):
        solver = pywraplp.Solver.CreateSolver('GLOP')
        if not solver:
            raise Exception('Could not create solver')
        
        x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
        y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')
        z = solver.NumVar(-solver.infinity(), solver.infinity(), 'z')

        for con in three_d_cons:
            solver.Add(eval(con.to_or_string()))
            
        solver.Maximize(eval(obj.to_or_string()))
        
        status = solver.Solve()
        if status == pywraplp.Solver.OPTIMAL:
            return Point3D(x.solution_value(),y.solution_value(),z.solution_value())
        if status == pywraplp.Solver.UNBOUNDED:
            return "UNBOUNDED"
        if status == pywraplp.Solver.INFEASIBLE:
            return "INFEASIBLE"
            


def solve_with_os_tool(program) -> Point:
    solver = OsToolSolver()
    return solver.solve(program[0], program[1])
