from typing import List
from Classes.ObjectiveFunction import ObjectiveFunction
from Classes.Constraints import Constraints
from Classes.Convex import Convex
from Classes.Point import Point
from Classes.Solver import Solver
from Classes.OneDConstraint import OneDConstraint
from Classes import OneDLinearProgram


def corner(obj:ObjectiveFunction)->Point:
    max = 18500
    points = [Point(max,max),Point(max,-max),Point(-max,max),Point(-max,-max)]
    #find the point that minimize obj
    res = None;
    val = float('inf')
    for p in points:
        if obj.value(p) < val:
            val = obj.value(p)
            res = p;
    return res

def to_1d_constraint(cons:List[Constraints])->List[Constraints]:
    # convert the 2d constraint to 1d constraint
    res = []
    for c in cons:
        res.append(OneDConstraint.from_constraint(c))
    return res


class ConvexSolver(Solver):
    def solve(self, obj:ObjectiveFunction, cons:List[Constraints]) -> Point:
        v = corner(obj)
        for idx,c in enumerate(cons):
            if not v.is_inside(c):
                one_d_constraints = to_1d_constraint(cons[:idx+1])
                x = OneDLinearProgram.solve_1d_linear_program(one_d_constraints,obj.a >= 0);
                v = c.find_point_with_x(x)
            else:
                # placeholder, not doing anything
                continue
        return v
        
