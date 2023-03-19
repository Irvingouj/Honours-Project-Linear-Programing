from ast import Tuple
from typing import List

import numpy as np
from linear_programming.classes.vector import Vector

from linear_programming.utils.exceptions import NoSolutionException
from .point import Point
from .oneDLinearProgram import solve_1d_linear_program, solve_1d_linear_program_with_left_and_right_index
from .objectiveFunction import ObjectiveFunction
from .solver import Solver
from .constraints import Constraints
from .oneDConstraint import OneDConstraint

import linear_programming.utils.debug as dbg


def corner(obj: ObjectiveFunction) -> Point:
    """
    find the corner point of the objective function
    """
    max_value = 18500
    points = [Point(max_value, max_value), Point(max_value, -max_value),
              Point(-max_value, max_value), Point(-max_value, -max_value)]
    # find the point that minimize obj
    res = None
    val = float('-inf')
    for p in points:
        if obj.value(p) > val:
            val = obj.value(p)
            res = p
    return res


def to_1d_constraint(curr: Constraints, cons: List[Constraints]) -> List[OneDConstraint]:
    # if the constrain is vertical, we rotate all the constraints by 90 degree
    if curr.is_vertical():
        cons = [c.rotate() for c in cons]
        curr = curr.rotate()

    # convert the 2d constraint to 1d constraint
    one_d = []
    for c in cons:
        p = curr.find_intersection(c)
        if c.is_parallel_but_share_no_common_area(curr):
            raise NoSolutionException("No solution as the constraints are parallel and share no common area")

        if p is not None:
            p1 = curr.find_point_with_x(p.x+1)
            if (c.contains(p1)):
                one_d.append(OneDConstraint(-1, -p.x))
            else:
                one_d.append(OneDConstraint(1, p.x))

    return one_d


# M = sys.maxsize/1000
M = 20000000


def get_one_d_optimize_direction(obj: ObjectiveFunction, curr: Constraints) -> bool:
    # projection of objective function on to the constraint
    proj = obj.to_vector().projection_on_to(
        curr.to_edge().to_line().to_vector().find_orthogonal_vector())
    return proj.arr[0] > 0


class ConvexSolver(Solver):
    def solve(self, obj: ObjectiveFunction, cons: List[Constraints]) -> Point:
        v = self._m1(obj).find_intersection(self._m2(obj))
        cons = [self._m1(obj), self._m2(obj)] + cons
        for idx, c in enumerate(cons):
            if not v.is_inside(c):
                one_d_constraints = to_1d_constraint(c, cons[:idx])
                if not c.is_vertical():
                    x = solve_1d_linear_program(
                        one_d_constraints, get_one_d_optimize_direction(obj, c))
                    v = c.find_point_with_x(x)
                else:
                    y = solve_1d_linear_program(
                        one_d_constraints, get_one_d_optimize_direction(obj, c))
                    v = c.find_point_with_y(y)

        return v

    def _m1(self, obj: ObjectiveFunction) -> Constraints:
        if obj.a > 0:
            return Constraints(1, 0, c=M)
        else:
            return Constraints(-1, 0, c=M)

    def _m2(self, obj: ObjectiveFunction) -> Constraints:
        if obj.b > 0:
            return Constraints(0, 1, c=M)
        else:
            return Constraints(0, -1, c=M)
        
    class CheckBoundResult:
        def __init__(self, bounded:bool, unbound_certificate:Vector = None, bound_certificate:Tuple(int,int) = None):
            assert isinstance(bounded,bool)
            assert isinstance(unbound_certificate,Vector) or unbound_certificate == None
            assert isinstance(bound_certificate,tuple) or bound_certificate == None
            
            # if bounded, the bound
            self.bounded = bounded
            self.unbound_certificate = unbound_certificate
            self.bound_certificate = bound_certificate
            
            # only one of them can be None, and at least one of them must be None, XOR
            assert (bound_certificate == None) != (unbound_certificate == None)
        def __str__(self):
            if self.bounded:
                return f"bounded, bound certificate: {self.bound_certificate}"
            else:
                return f"unbounded, unbound certificate: {self.unbound_certificate}"

    def check_unbounded(self, obj: ObjectiveFunction, cons: List[Constraints]) -> CheckBoundResult:
        obj_vector = obj.to_vector()
        degree_needed = obj_vector.degree_needed_to_rotate_to(Vector([0,1]))
        rotated_cons = [c.get_rotate_around_origin(degree_needed) for c in cons]
        cons_facing_normal_vector = [c.facing_normal_vector() for c in rotated_cons]
        one_d_cons = [OneDConstraint(-c.arr[0], c.arr[1]) for c in cons_facing_normal_vector]
        dx,left,right = solve_1d_linear_program_with_left_and_right_index(one_d_cons, True)
        
        # no solution, the problem is bounded
        if dx == None:
            return self.CheckBoundResult(bounded=True,bound_certificate=(left,right))
        

        # dx exist, which means the direction of unboundedness is (dx,1)
        H_prime = []
        for idx,vector in enumerate(cons_facing_normal_vector):
            eta_x = vector.get(0)
            eta_y = vector.get(1)
            # d_x*eta_x + d_y*eta_y = 0 but d_y = 1
            # d_x = -eta_x/eta_y
            #need to do some thing if eta_y is 0 :TODO
            if eta_y != 0 and np.allclose(dx,-eta_x/eta_y):
                H_prime.append(cons[idx])

        # pg 81, convert to 1d again and check for feasibility
        # we ignore paralell constraints for now                
        if len(H_prime) > 1:
            raise NotImplementedError("Not implemented yet")
        
        result = self.CheckBoundResult(bounded=False,unbound_certificate=Vector([dx, 1]).get_rotate(-degree_needed))
        return result


def solve_with_convex(program) -> Point:
    solver = ConvexSolver()
    return solver.solve(program[0], program[1])
