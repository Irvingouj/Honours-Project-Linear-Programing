
from typing import List
from linear_programming.classes.constraints import Constraints, GreaterOrLess
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.classes.solver import Solver
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.three_d.point3d import Point3D
from linear_programming.utils.exceptions import NoSolutionException, UnboundedException
from linear_programming.utils.types import Program3d
from .objective_function_3d import ObjectiveFunction3D
from .constraint_3d import Constraints3D


class Convex3DSolver(Solver):
    def solve(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> List[Point3D]:
        raise NotImplementedError("Not implemented yet")
        # if not self.check_bounded(obj, cons):V
        #     raise UnboundedException("Unbounded problem",ray=)
    
    def rotate_program(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> Program3d:
        """
        returns the rotated program so that the objective function is facing up the z-axis
        """
        theta, phi = obj.get_angle_needed_for_rotation()
        x_rotated_cons = [c.get_rotate_z(theta) for c in cons]
        y_rotated_cons = [c.get_rotate_x(phi) for c in x_rotated_cons]
        return ObjectiveFunction3D(a=0,b=0,c=1), y_rotated_cons
    
    def check_bounded(self, obj: ObjectiveFunction3D, cons: List[Constraints3D]) -> bool:
        """
        returns true if the problem is bounded, false otherwise
        """

        # rotate everything so that the objective function is facing up the z-axis
        theta, phi = obj.get_angle_needed_for_rotation()
        x_rotated_cons = [c.get_rotate_x(theta) for c in cons]
        y_rotated_cons = [c.get_rotate_y(phi) for c in x_rotated_cons]
        facing_direction_vecs = [c.facing_direction_vector() for c in y_rotated_cons]
        two_d_cons = [Constraints(v[0], v[1], lessOrGreater=GreaterOrLess.GREATER, c=v[2]) for v in facing_direction_vecs]

        try:
            res = ConvexSolver().solve(ObjectiveFunction(0, 0), two_d_cons)
        except NoSolutionException:
            # unbounded
            return 'BOUNDED'
        except UnboundedException:
            # unbounded for 2d problem means that there exist infinitely many solutions for the 3d problem
            return 'UNBOUNDED'
        
        return 'UNBOUNDED'
        

        
        