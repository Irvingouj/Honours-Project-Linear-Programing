
from typing import List
from linear_programming.classes.solver import Solver
from linear_programming.classes.three_d.point3d import Point3D
from .objective_function_3d import ObjectiveFunction3D
from .constraint_3d import Constraints3D


class Convex3DSolver(Solver):
    def solve(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> List[Point3D]:
        pass
    
    def check_unbounded(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> bool:

        # rotate everything so that the objective function is facing up the z-axis
        theta, phi = obj.get_angle_needed_for_rotation()
        x_rotated_cons = [c.rotate_x(theta) for c in cons]
        y_rotated_cons = [c.rotate_y(phi) for c in x_rotated_cons]
        facing_direction_vecs = [c.get_facing_direction_vector() for c in y_rotated_cons]

        
        