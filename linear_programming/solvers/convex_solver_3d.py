
from typing import List, Tuple

import numpy as np
from linear_programming.classes.three_d.line_3d import Line3d
from linear_programming.classes.two_d import Constraints, GreaterOrLess, ObjectiveFunction
from linear_programming.classes.two_d.point import Point
from .solver import Solver
from .convex_solver import ConvexSolver
from ..classes.three_d import Constraints3D, ObjectiveFunction3D, Point3D
from ..utils.exceptions import AbnormalException, NoSolutionException2D, NoSolutionException3D, UnboundedException2D, UnboundedException3D
from ..utils.types import CheckBoundResult3D, Program3d





def convert_to_2d(curr: Constraints3D, cons: List[Constraints3D]) -> List[Constraints]:
    
    res = []
    for c_i in cons:
        intersection: Line3d = curr.find_intersection(c_i)
        p_3d = intersection.point
        p_x, p_y = p_3d.x, p_3d.y
        u = [-p_x, -p_y]
        p_positive, p_negative = [p_x+u[0], p_y+u[1]], [p_x-u[0], p_y-u[1]]
        p_positive_3d, p_negative_3d = curr.find_point_with_x_y(p_positive[0], p_positive[1]), curr.find_point_with_x_y(p_negative[0], p_negative[1])
        p_posi_3d_proj, p_neg_3d_proj = Point(p_positive_3d.x, p_positive_3d.y), Point(p_negative_3d.x, p_negative_3d.y)
        two_d_line = intersection.get_projection_on_x_y_plane()
        c_i_2d = Constraints.from_line_and_point(two_d_line, p_posi_3d_proj if c_i.contains(p_positive_3d) else p_neg_3d_proj)
        res.append(c_i_2d)
    return res

def convert_to_2d_x_z(curr: Constraints3D, cons: List[Constraints3D]) -> List[Constraints]:
    res = []
    for c_i in cons:
        intersection: Line3d = curr.find_intersection(c_i)
        p_3d = intersection.point
        p_x, p_z = p_3d.x, p_3d.z
        u = [-p_x, -p_z]
        p_positive, p_negative = [p_x+u[0], p_z+u[1]], [p_x-u[0], p_z-u[1]]
        p_positive_3d, p_negative_3d = curr.find_point_with_x_z(
            p_positive[0], p_positive[1]), curr.find_point_with_x_z(p_negative[0], p_negative[1])
        
        p_positive_3d_proj, p_negative_3d_proj = Point(
            p_positive_3d.x, p_positive_3d.z), Point(p_negative_3d.x, p_negative_3d.z)
        two_d_line = intersection.get_projection_on_x_z_plane()
        c_i_2d = Constraints.from_line_and_point(two_d_line, p_positive_3d_proj if c_i.contains(p_positive_3d) else p_negative_3d_proj)
        res.append(c_i_2d)
    return res

def find_two_d_obj(obj: ObjectiveFunction3D, curr: Constraints3D) -> ObjectiveFunction:
    l1, l2, l3 = obj.a, obj.b, obj.c
    a, b, c = curr.a, curr.b, curr.c

    d2_a = l1-(l3*a)/c
    d2_b = l2-(l3*b)/c
    return ObjectiveFunction(d2_a, d2_b, obj.maxOrMin)

def find_two_d_obj_x_z(obj: ObjectiveFunction3D, curr: Constraints3D) -> ObjectiveFunction:
    l1, l2, l3 = obj.a, obj.b, obj.c
    a, b, c = curr.a, curr.b, curr.c
    
    d_2a = l1-(l2*a)/b
    d_2c = l3-(l2*c)/b
    
    return ObjectiveFunction(d_2a, d_2c, obj.maxOrMin)

class Convex3DSolver(Solver):

    def solve(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> List[Point3D]:
        res = self.check_bounded(obj, cons)
        if not res.is_bounded:
            #Unbounded Index To Be Determined
            raise UnboundedException3D(stage="Solve", unbounded_index=None)

        h1_idx, h2_idx, h3_idx = res.certificates[0], res.certificates[1], res.certificates[2]
        h1,h2,h3 = self.switch_index(h1_idx, h2_idx, h3_idx, cons)
        v = self.find_intersection_point(h1, h2, h3)
        for idx, c in enumerate(cons):
            if c.contains(v):
                continue
            
            #vertical plane case
            if c.is_vertical():
                convert_func,obj_func,evaluate_func = convert_to_2d_x_z,find_two_d_obj_x_z,c.find_point_with_x_z
            else :
                convert_func,obj_func,evaluate_func = convert_to_2d,find_two_d_obj,c.find_point_with_x_y
                
            two_d_cons = convert_func(c, cons[:idx])
            two_d_obj = obj_func(obj, c)

            try:
                res = ConvexSolver().solve(two_d_obj, two_d_cons)
            except NoSolutionException2D as err:
                raise NoSolutionException3D(stage="2D Infeasible") from err
            except UnboundedException2D as err:
                # we should never get here
                raise err

            v = evaluate_func(res.x, res.y)
        return v

    def rotate_program(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> Program3d:
        """
        returns the rotated program so that the objective function is facing up the z-axis
        """
        theta, phi = obj.get_angle_needed_for_rotation()
        x_rotated_cons = [c.get_rotate_z(theta) for c in cons]
        y_rotated_cons = [c.get_rotate_x(phi) for c in x_rotated_cons]
        return ObjectiveFunction3D(a=0, b=0, c=1), y_rotated_cons

    def check_bounded(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> CheckBoundResult3D:
        """
        returns true if the problem is bounded, false otherwise
        """

        theta, phi = obj.get_angle_needed_for_rotation()
        z_rotated_cons = [c.get_rotate_z(theta) for c in cons]
        x_rotated_cons = [c.get_rotate_x(phi) for c in z_rotated_cons]
        facing_direction_vecs = [c.facing_direction_vector() for c in x_rotated_cons]
        two_d_cons = [Constraints(v[0], v[1], lessOrGreater=GreaterOrLess.GREATER, c=-v[2]) for v in facing_direction_vecs]
        try:
            obj = ObjectiveFunction(1,1)
            res = ConvexSolver().solve_with_3d_certificate(obj, two_d_cons)
        except NoSolutionException2D as err:
            if err.three_d_bound_certificate is not None:
                return CheckBoundResult3D(is_bounded=True, ray=None, certificates=err.three_d_bound_certificate)
            raise AbnormalException("This may have a solution, but we can't find it") from err
        except UnboundedException2D as err:
            return CheckBoundResult3D(is_bounded=False, ray=f"TODO:find ray {err}", certificates=None)
        return CheckBoundResult3D(is_bounded=False, ray=f"TODO:find ray {res}", certificates=None)

    @staticmethod
    def switch_index(h1_idx, h2_idx,h3_idx, cons) -> Tuple[Constraints3D, Constraints3D, Constraints3D]:
        c1, c2, c3 = cons[h1_idx], cons[h2_idx], cons[h3_idx]
        cons[0], cons[h1_idx] = cons[h1_idx], cons[0]
        h2_idx = cons.index(c2)
        cons[1], cons[h2_idx] = cons[h2_idx], cons[1]
        h3_idx = cons.index(c3)
        cons[2], cons[h3_idx] = cons[h3_idx], cons[2]
        
        return c1, c2, c3

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
            raise NoSolutionException3D(stage="3D No Intersection") from err

        x = A_inv @ np.array([c1.d, c2.d, c3.d])
        return Point3D(x[0], x[1], x[2])

    @staticmethod
    def con_solve(obj, cons):
        try:
            return Convex3DSolver().solve(obj, cons)
        except NoSolutionException3D:
            return "INFEASIBLE" 
        except UnboundedException2D:
            return "UNBOUNDED"
