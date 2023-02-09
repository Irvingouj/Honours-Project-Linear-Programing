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
    val = float('-inf')
    for p in points:
        if obj.value(p) > val:
            val = obj.value(p)
            res = p;
    return res

def to_1d_constraint(curr:Constraints,cons:List[Constraints])->List[OneDConstraint]:

    # if the constrain is vertical, we rotate all the constraints by 90 degree
    if curr.is_vertical():
        cons = [c.rotate() for c in cons]
        curr = curr.rotate()

    # convert the 2d constraint to 1d constraint
    one_d = []
    for c in cons:
        p = curr.find_intersection(c)
        if p is not None:
            # TODO: figure out the direction, how do I know which side of the constraint is facing
            p1 = curr.find_point_with_x(p.x+1)
            if(c.is_inside(p1)):
                one_d.append(OneDConstraint(-1,-p.x))
            else:
                one_d.append(OneDConstraint(1,p.x))


    return one_d

M = 18500

class ConvexSolver(Solver):
    def solve(self, obj:ObjectiveFunction, cons:List[Constraints]) -> Point:
        v = corner(obj);
        cons = [self._m1(obj),self._m2(obj)] + cons
        
        for idx,c in enumerate(cons):
            if not v.is_inside(c):
                one_d_constraints = to_1d_constraint(c,cons[:idx])
                x = OneDLinearProgram.solve_1d_linear_program(one_d_constraints,objective=obj.get_direction_for_x_axis());
                v = c.find_point_with_x(x)
            else:
                # placeholder, not doing anything
                continue
        return v
    


    def _m1(self,obj:ObjectiveFunction)->Constraints:
        if (obj.a > 0):
            return Constraints(1,0,M)
        else:
            return Constraints(-1,0,M)
        
    def _m2(self,obj:ObjectiveFunction)->Constraints:
        if (obj.b > 0):
            return Constraints(0,1,M)
        else:
            return Constraints(0,-1,M)
        
        
