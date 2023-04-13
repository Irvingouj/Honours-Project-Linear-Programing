from ast import Tuple
from typing import List
import numpy as np
from linear_programming.classes.two_d import Point, ObjectiveFunction, Constraints
from linear_programming.classes.one_d import OneDConstraint
from linear_programming.utils.exceptions import NoSolutionException2D, PerceptionException, UnboundedException2D
from linear_programming.solvers.solver import Solver
from linear_programming.classes.one_d.one_d_LinearProgram import solve_1d_linear_program, solve_1d_linear_program_with_left_and_right_index
from linear_programming.classes.vector import Vector
from linear_programming.utils.types import CheckBoundResult2D


def to_1d_constraint(curr: Constraints, cons: List[Constraints]) -> List[OneDConstraint]:
    # if the constrain is vertical, we rotate all the constraints by 90 degree
    if curr.is_vertical():
        cons = [c.rotate() for c in cons]
        curr = curr.rotate()

    # convert the 2d constraint to 1d constraint
    one_d = []
    for h in cons:
        if h.is_parallel_but_share_no_common_area(curr):
            # What should the three d bound certificate be?
            raise NoSolutionException2D(stage="Parallel Checking", three_d_bounded_certificate=None)

        p = curr.find_intersection(h)
        if p is not None:
            # plus 10000 to get the direction of the one dimension constraint,
            # there's gotta be a better way, this suffers heavily from floating point error
            p1 = curr.find_point_with_x(p.x+100000)
            p2 = curr.find_point_with_x(p.x-100000)

            if (h.contains(p1) and h.contains(p2)) or (not h.contains(p1) and not h.contains(p2)):
                raise PerceptionException(
                    "Abnormal situation, float precision error")

            if (h.contains(p1)):
                # if h contains p1, then h must facing right
                # x >= p.x
                one_d.append(OneDConstraint(-1, -p.x))
            else:
                # x <= p.x
                one_d.append(OneDConstraint(1, p.x))

    return one_d


def get_one_d_optimize_direction(obj: ObjectiveFunction, curr: Constraints) -> bool:
    c_x = obj.a
    c_y = obj.b
    a_k = curr.a
    b_k = curr.b
    
    return c_x - (c_y*a_k)/b_k >= 0



class ConvexSolver(Solver):

    def solve(self, obj: ObjectiveFunction, cons: List[Constraints]) -> Point:
        bound_res = self.check_unbounded(obj, cons)
        if not bound_res.bounded:
            raise UnboundedException2D(stage="Solve",unbounded_index=bound_res.unbounded_index)
        h1,h2 = self.switch_index(bound_res.bound_certificate[0], bound_res.bound_certificate[1], cons)

        v = h1.find_intersection(h2)
        for idx, c in enumerate(cons):
            if v.is_inside(c):
                continue
            one_d_constraints = to_1d_constraint(c, cons[:idx])
            one_d_obj =  get_one_d_optimize_direction(obj, c)
            find_func = c.find_point_with_x if not c.is_vertical() else c.find_point_with_y
            x = solve_1d_linear_program(one_d_constraints, one_d_obj)
            v = find_func(x)

        return v

    def check_unbounded(self, obj: ObjectiveFunction, cons: List[Constraints]) -> CheckBoundResult2D:
        obj_vector = obj.to_vector()
        degree_needed = obj_vector.degree_needed_to_rotate_to(Vector([0, 1]))
        rotated_cons = [c.get_rotate_around_origin(
            degree_needed) for c in cons]
        cons_facing_normal_vector = [
            c.facing_normal_vector() for c in rotated_cons]
        one_d_cons = [OneDConstraint(-c.arr[0], c.arr[1])
                      for c in cons_facing_normal_vector]
        dx, left, right = solve_1d_linear_program_with_left_and_right_index(
            one_d_cons, True)

        # no solution, the problem is bounded
        if dx is None:
            return CheckBoundResult2D(bounded=True, bound_certificate=(left, right))

        # dx exist, which means the direction of unboundness is (dx,1)
        H_prime: List[Constraints] = []
        for idx, vector in enumerate(cons_facing_normal_vector):
            eta_x = vector.get(0)
            eta_y = vector.get(1)
            # d_x*eta_x + d_y*eta_y = 0 but d_y = 1
            # d_x = -eta_x/eta_y
            if eta_y != 0 and np.allclose(dx, -eta_x/eta_y):
                H_prime.append(rotated_cons[idx])

        # pg 81, convert to 1d again and check for feasibility
        if len(H_prime) > 1:
            one_d_again = []
            for h_i in H_prime:
                one_d = OneDConstraint(h_i.a, h_i.c)
                one_d_again.append(one_d)
            dx_prime, __, _ = solve_1d_linear_program_with_left_and_right_index(
                one_d_again, True)
            if dx_prime == None:
                # what should the three D certificate be?
                raise NoSolutionException2D(stage="Check Unboundness", three_d_bounded_certificate=None)

        result = CheckBoundResult2D(
            bounded=False, unbound_certificate=cons[left], unbounded_index=left)
        return result

    def solve_with_3d_certificate(self, obj: ObjectiveFunction, cons: List[Constraints]) -> Point:
        bound_res = self.check_unbounded(obj, cons)
        if not bound_res.bounded:
            raise UnboundedException2D(stage="Solve For Certificate",unbounded_index=bound_res.unbounded_index)

        h1_idx = bound_res.bound_certificate[0]
        h2_idx = bound_res.bound_certificate[1]
        h1 = cons[h1_idx]
        h2 = cons[h2_idx]
        altered_index = [i for i in range(len(cons))]
        cons[0], cons[h1_idx] = cons[h1_idx], cons[0]
        altered_index[0], altered_index[h1_idx] = altered_index[h1_idx], altered_index[0]

        # h2 might be changed after h1 is changed
        h2_read_idx = cons.index(h2)
        cons[1], cons[h2_read_idx] = cons[h2_read_idx], cons[1]
        altered_index[1], altered_index[h2_read_idx] = altered_index[h2_read_idx], altered_index[1]

        point_find_func = None
        v = h1.find_intersection(h2)
        for idx, c in enumerate(cons):
            assert not np.isinf(v.x) and not np.isnan(
                v.y), "v never should be inf or nan"
            if v.is_inside(c):
                continue

            one_d_constraints = to_1d_constraint(c, cons=cons[:idx])
            point_find_func = c.find_point_with_x if not c.is_vertical() else c.find_point_with_y
            x, left, right = solve_1d_linear_program_with_left_and_right_index(
                one_d_constraints, get_one_d_optimize_direction(obj, c))
            if x is None:
                d3_certificate = (altered_index[idx], altered_index[left], altered_index[right])
                raise NoSolutionException2D(stage="Solve For Three D Certificate", three_d_bounded_certificate=d3_certificate)
            v = point_find_func(x)

        return v

    def switch_index(self, h1_idx: int, h2_idx: int, cons: List[Constraints]) -> Tuple(Constraints, Constraints):
        h1,h2 = cons[h1_idx],cons[h2_idx]
        cons[0], cons[h1_idx] = cons[h1_idx], cons[0]
        h2_read_idx = cons.index(h2)
        cons[1], cons[h2_read_idx] = cons[h2_read_idx], cons[1]
        return h1,h2
    
    @staticmethod    
    def solve_with_convex(obj,cons) -> Point:
        solver = ConvexSolver()
        try:
            return solver.solve(obj, cons)
        except NoSolutionException2D:
            return "INFEASIBLE"
        except UnboundedException2D:
            return "UNBOUNDED"
