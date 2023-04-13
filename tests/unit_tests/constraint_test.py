import math
import unittest
from linear_programming.classes.two_d import Constraints
from linear_programming.solvers.or_tool_solver import OrToolSolver
from linear_programming.solvers.convex_solver_3d import Convex3DSolver
from linear_programming.utils.linear_program_generator import gen_random_3d_unbounded


class TestConstraints(unittest.TestCase):
    def test_rotation(self):
        con = Constraints(a=1, b=1, c=1) # x + y <= 1
        rotated = con.get_rotate_around_origin(math.pi/2)
        
        print(rotated)
        self.assertAlmostEqual(rotated.a, -1)
        self.assertAlmostEqual(rotated.b, 1)
        self.assertAlmostEqual(rotated.c, 1)
        
        rotated = con.get_rotate_around_origin(math.pi)
        print(rotated)
        self.assertAlmostEqual(rotated.a, -1)
        self.assertAlmostEqual(rotated.b, -1)
        self.assertAlmostEqual(rotated.c, 1)
        self.assertAlmostEqual(rotated.a, -1)
        
        rotated = con.get_rotate_around_origin(3*math.pi/2)
        print(rotated)
        self.assertAlmostEqual(rotated.a, 1)
        self.assertAlmostEqual(rotated.b, -1)
        self.assertAlmostEqual(rotated.c, 1)
        
        rotated = con.get_rotate_around_origin(-math.pi/2)
        print(rotated)
        self.assertAlmostEqual(rotated.a, 1)
        self.assertAlmostEqual(rotated.b, -1)
        self.assertAlmostEqual(rotated.c, 1)
        
    def test_iteratively(self):
        for i in range(100):
            prev_obj,prev_cons = gen_random_3d_unbounded(5)
            prev = OrToolSolver().solve_three_d(prev_obj,prev_cons)
            obj,cons = Convex3DSolver().rotate_program(prev_obj,prev_cons)
            after = OrToolSolver().solve_three_d(obj,cons)
            
            
            if type(prev) != type(after):
               self.fail("Different types")
               
            self.assertAlmostEqual(prev,after)   
        
        
        
        
        

        