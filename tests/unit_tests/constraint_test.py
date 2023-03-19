import math
import unittest
from linear_programming.classes.constraints import Constraints


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
        
        
        
        

        