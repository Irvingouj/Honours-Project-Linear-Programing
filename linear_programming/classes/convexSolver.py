from typing import List
from linear_programming.classes.vector import Vector

from linear_programming.utils.exceptions import NoSolutionException
from .point import Point
from .oneDLinearProgram import solve_1d_linear_program
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
                # print(f"v: {v} is not inside {c}")
                one_d_constraints = to_1d_constraint(c, cons[:idx])
                if not c.is_vertical():
                    x = solve_1d_linear_program(
                        one_d_constraints, get_one_d_optimize_direction(obj, c))
                    v = c.find_point_with_x(x)
                else:
                    y = solve_1d_linear_program(
                        one_d_constraints, get_one_d_optimize_direction(obj, c))
                    v = c.find_point_with_y(y)
                # print(f"v: {v} is updated")

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

    def check_unbounded(self, obj: ObjectiveFunction, cons: List[Constraints]) -> Vector:
        obj_vector = obj.to_vector()
        degree_needed = obj_vector.degree_needed_to_rotate_to(Vector([0,1]))
        rotated_cons = [c.get_rotate_around_origin(degree_needed) for c in cons]
        dbg.print_cons(rotated_cons, "rotated_cons")
        cons_facing_normal_vector = [c.facing_normal_vector() for c in rotated_cons]
        dbg.print_cons(cons_facing_normal_vector, "cons_facing_normal_vector")
        one_d_cons = [OneDConstraint(-c.arr[0], c.arr[1]) for c in cons_facing_normal_vector]
        dbg.print_cons(one_d_cons, "one_d_cons")
        try:
            res = solve_1d_linear_program(one_d_cons, True)
        except NoSolutionException:
            # do something here
            pass
        
        
        return Vector([res, 1]).get_rotate(-degree_needed)


def solve_with_convex(program) -> Point:
    solver = ConvexSolver()
    return solver.solve(program[0], program[1])
