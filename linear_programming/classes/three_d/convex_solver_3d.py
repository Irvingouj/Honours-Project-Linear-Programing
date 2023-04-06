
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
        import linear_programming.utils.debug as debug
        debug.start()
        debug.message("before rotation")
        debug.os_solve_3d(obj, cons)
        # debug.message("original",cons)
        debug.message("angles between consecutive constraint", [cons[i].angle_between(cons[i+1]) for i in range(len(cons)-1)])
        
        debug.message("\n","angel between obj and each constraint",
                    [obj.to_vector().angle_between(c.facing_direction_vector()) for c in cons])

        debug.message("-" * 20)

        # rotate everything so that the objective function is facing up the z-axis
        theta, phi = obj.get_angle_needed_for_rotation()
        z_rotated_cons = [c.get_rotate_z(theta) for c in cons]
        z_rotated_obj = obj.get_rotate_z(theta)

        # debug.message("z rotated",z_rotated_cons)
        # debug.message("rotated_obj",z_rotated_obj,'\n')
        debug.message("angles between consecutive constraint", [z_rotated_cons[i].angle_between(z_rotated_cons[i+1]) for i in range(len(cons)-1)])
        debug.message("\n","angel between obj and each constraint",
                      [z_rotated_obj.to_vector().angle_between(c.facing_direction_vector()) for c in z_rotated_cons])

        debug.os_solve_3d(z_rotated_obj, z_rotated_cons)
        debug.message("-" * 20)
        x_rotated_cons = [c.get_rotate_x(phi) for c in z_rotated_cons]
        x_rotated_obj = z_rotated_obj.get_rotate_x(phi)
        
        # debug.message("x rotated",x_rotated_cons)
        # debug.message("rotated_obj",x_rotated_obj)
        debug.message("angles between consecutive constraint", [x_rotated_cons[i].angle_between(x_rotated_cons[i+1]) for i in range(len(cons)-1)])
        debug.message("\n","angel between obj and each constraint",
                      [x_rotated_obj.to_vector().angle_between(c.facing_direction_vector()) for c in x_rotated_cons])

        debug.message("end rotation")
        debug.os_solve_3d(ObjectiveFunction(0,0,1), cons)
        debug.end()
        
        facing_direction_vecs = [c.facing_direction_vector() for c in x_rotated_cons]
        two_d_cons = [Constraints(v[0], v[1], lessOrGreater=GreaterOrLess.GREATER, c=v[2]) for v in facing_direction_vecs]

        try:
            res = ConvexSolver().solve(ObjectiveFunction(0, 0), two_d_cons)
        except NoSolutionException:
            # unbounded
            return 'BOUNDED'
        except UnboundedException as err:
            unbounded_certificate = err.unbounded_certificate
            unbounded_index = err.unbounded_index
            return 'UNBOUNDED, by unbounded'
        
        return 'UNBOUNDED, by solution'
        

        
        