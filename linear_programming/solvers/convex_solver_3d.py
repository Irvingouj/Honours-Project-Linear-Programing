
from typing import List

import numpy as np
from linear_programming.classes.three_d.line_3d import Line3d
from linear_programming.classes.two_d import Constraints, GreaterOrLess, ObjectiveFunction
from linear_programming.classes.two_d.point import Point
from linear_programming.classes.vector import Vector
from .solver import Solver
from .convexSolver import ConvexSolver
from ..classes.three_d import Constraints3D, ObjectiveFunction3D, Point3D
from ..utils.exceptions import NoSolutionException, UnboundedException
from ..utils.types import Program3d
from ..utils.exceptions import NoSolutionException, UnboundedException
from ..utils import dbg


class CheckBoundResult:
    def __init__(self, is_bounded, ray, certificates):
        self.is_bounded = is_bounded
        self.ray = ray
        self.certificates = certificates

    def __str__(self):
        if self.is_bounded:
            return f"bounded by {str(self.certificates)}"
        else:
            return f"unbounded by {str(self.certificates)}"


def convert_to_2d(curr: Constraints3D, cons: List[Constraints3D]) -> List[Constraints]:
    res = []
    for c_i in cons:
        intersection: Line3d = curr.find_intersection(c_i)
        p_3d = intersection.point
        p_x, p_y = p_3d.x, p_3d.y
        u = [-p_x, -p_y]
        p_positive, p_negative = [p_x+u[0], p_y+u[1]], [p_x-u[0], p_y-u[1]]
        p_positive_3d, p_negative_3d = curr.find_point_with_x_y(
            p_positive[0], p_positive[1]), curr.find_point_with_x_y(p_negative[0], p_negative[1])
        p_posi_3d_proj, p_neg_3d_proj = Point(
            p_positive_3d.x, p_positive_3d.y), Point(p_negative_3d.x, p_negative_3d.y)
        c_i_2d = Constraints.from_line_and_point(intersection.get_projection_on_x_y_plane(
        ), p_posi_3d_proj if c_i.contains(p_positive_3d) else p_neg_3d_proj)
        res.append(c_i_2d)
    return res


def find_two_d_obj(obj: ObjectiveFunction3D, curr: Constraints3D) -> ObjectiveFunction:
    l1, l2, l3 = obj.a, obj.b, obj.c
    a, b, c = curr.a, curr.b, curr.c

    d2_a = l1-(l3*a)/c
    d2_b = l2-(l3*b)/c
    return ObjectiveFunction(d2_a, d2_b, obj.maxOrMin)


class Convex3DSolver(Solver):

    def solve(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> List[Point3D]:
        res = self.check_bounded(obj, cons)
        if not res.is_bounded:
            raise UnboundedException(
                unbounded_certificate=res.ray, unbounded_index=None)

        c1_idx, c2_idx, c3_idx = res.certificates[0], res.certificates[1], res.certificates[2]
        c1, c2, c3 = cons[c1_idx], cons[c2_idx], cons[c3_idx]
        cons[0], cons[c1_idx] = cons[c1_idx], cons[0]
        c2_idx = cons.index(c2)
        cons[1], cons[c2_idx] = cons[c2_idx], cons[1]
        c3_idx = cons.index(c3)
        cons[2], cons[c3_idx] = cons[c3_idx], cons[2]

        v = self.find_intersection_point(c1, c2, c3)

        for idx, c in enumerate(cons):
            if c.contains(v):
                continue

            two_d_cons = convert_to_2d(c, cons[:idx])
            two_d_obj = find_two_d_obj(obj, c)

            try:
                res = ConvexSolver().solve(two_d_obj, two_d_cons)
            except NoSolutionException as err:
                raise NoSolutionException(stage="3d solver, result is the same, problem infeasible") from err
            except UnboundedException as err:
                # we should never get here
                raise err

            v = c.find_point_with_x_y(res.x, res.y)
        return v

    def rotate_program(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> Program3d:
        """
        returns the rotated program so that the objective function is facing up the z-axis
        """
        theta, phi = obj.get_angle_needed_for_rotation()
        x_rotated_cons = [c.get_rotate_z(theta) for c in cons]
        y_rotated_cons = [c.get_rotate_x(phi) for c in x_rotated_cons]
        return ObjectiveFunction3D(a=0, b=0, c=1), y_rotated_cons

    def check_bounded(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> CheckBoundResult:
        """
        returns true if the problem is bounded, false otherwise
        """

        theta, phi = obj.get_angle_needed_for_rotation()
        z_rotated_cons = [c.get_rotate_z(theta) for c in cons]
        x_rotated_cons = [c.get_rotate_x(phi) for c in z_rotated_cons]
        facing_direction_vecs = [c.facing_direction_vector()
                                 for c in x_rotated_cons]
        two_d_cons = [Constraints(
            v[0], v[1], lessOrGreater=GreaterOrLess.GREATER, c=-v[2]) for v in facing_direction_vecs]
        try:
            res = ConvexSolver().solve_with_3d_certificate(
                ObjectiveFunction(1, 1), two_d_cons)
        except NoSolutionException as err:
            return CheckBoundResult(is_bounded=True, ray=None, certificates=err.three_d_bound_certificate)
        except UnboundedException as err:
            return CheckBoundResult(is_bounded=False, ray=f"TODO:find ray {err}", certificates=None)

        return CheckBoundResult(is_bounded=False, ray=f"TODO:find ray {res}", certificates=None)

    @staticmethod
    def find_intersection_point(c1: Constraints3D, c2: Constraints3D, c3: Constraints3D) -> Point3D:
        A = np.array([
            [c1.a, c1.b, c1.c],
            [c2.a, c2.b, c2.c],
            [c3.a, c3.b, c3.c]
        ])
        try:
            A_inv = np.linalg.inv(A)
        except np.linalg.LinAlgError as err:
            # we should have some solution here
            raise NoSolutionException(
                stage="3d find intersection point") from err

        x = A_inv @ np.array([c1.d, c2.d, c3.d])
        return Point3D(x[0], x[1], x[2])

    @staticmethod
    def con_solve(obj, cons):
        try:
            return Convex3DSolver().solve(obj, cons)
        except NoSolutionException as err:
            return "INFEASIBLE" 
        except UnboundedException as err:
            return "UNBOUNDED"
