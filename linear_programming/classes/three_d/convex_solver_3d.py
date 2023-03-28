
from typing import List
from linear_programming.classes.constraints import Constraints, GreaterOrLess
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.classes.solver import Solver
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.three_d.point3d import Point3D
from linear_programming.utils.exceptions import NoSolutionException
from .objective_function_3d import ObjectiveFunction3D
from .constraint_3d import Constraints3D


class Convex3DSolver(Solver):
    def solve(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> List[Point3D]:
        pass
    
    def check_unbounded(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> bool:

        # rotate everything so that the objective function is facing up the z-axis
        theta, phi = obj.get_angle_needed_for_rotation()
        x_rotated_cons = [c.get_rotate_x(theta) for c in cons]
        y_rotated_cons = [c.get_rotate_y(phi) for c in x_rotated_cons]
        facing_direction_vecs = [c.facing_direction_vector() for c in y_rotated_cons]
        two_d_cons = [Constraints(v[0], v[1], lessOrGreater=GreaterOrLess.GREATER, c=v[2]) for v in facing_direction_vecs]

        try:
            ConvexSolver().solve(ObjectiveFunction(0, 0), two_d_cons)
        except NoSolutionException:
            # bounded
            return True
        
        # unbounded
        return False
        

        
        