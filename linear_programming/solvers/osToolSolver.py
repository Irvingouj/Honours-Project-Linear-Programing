from ortools.linear_solver import pywraplp
from typing import List, Union
from linear_programming.utils.exceptions import PerceptionException
from linear_programming.classes.two_d import Point, ObjectiveFunction, Constraints
from linear_programming.solvers.solver import Solver
from linear_programming.classes.three_d import Point3D, ObjectiveFunction3D, Constraints3D
from linear_programming.classes.one_d import OneDConstraint



class OsToolSolver(Solver):
    param = pywraplp.MPSolverParameters()
    param.SetIntegerParam(pywraplp.MPSolverParameters.PRESOLVE, pywraplp.MPSolverParameters.PRESOLVE_OFF)
    def get_solver(self):
        solver = pywraplp.Solver.CreateSolver('GLOP')
        
        return solver
    
    def solve(self, obj: ObjectiveFunction, cons: List[Constraints]) -> Point:
        solver = self.get_solver()

        x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
        y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')

        for c in cons:
            solver.Add(eval(c.to_or_string()))

        solver.Maximize(eval(obj.to_or_string()))

        status = solver.Solve(OsToolSolver.param)

        if status == pywraplp.Solver.OPTIMAL:
            return Point(x.solution_value(), y.solution_value())
        if status == pywraplp.Solver.INFEASIBLE:
            return "INFEASIBLE"
        if status == pywraplp.Solver.UNBOUNDED:
            return "UNBOUNDED"

        if status == pywraplp.Solver.ABNORMAL:
            #https://github.com/google/or-tools/issues/1986
            raise PerceptionException("Abnormal status returned from solver")

    def solve_one_dimension(self, one_d_constraints: List[OneDConstraint], objective: bool) -> float:
        solver = self.get_solver()
        
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
        solver = self.get_solver()
        
        x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
        y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')
        z = solver.NumVar(-solver.infinity(), solver.infinity(), 'z')

        for con in three_d_cons:
            solver.Add(eval(con.to_or_string()))
            
        solver.Maximize(eval(obj.to_or_string()))
        
        status = solver.Solve(OsToolSolver.param)
        if status == pywraplp.Solver.OPTIMAL:
            return Point3D(x.solution_value(),y.solution_value(),z.solution_value())
        if status == pywraplp.Solver.UNBOUNDED:
            return "UNBOUNDED"
        if status == pywraplp.Solver.INFEASIBLE:
            return "INFEASIBLE"
            


def solve_with_os_tool(program) -> Point:
    solver = OsToolSolver()
    return solver.solve(program[0], program[1])
