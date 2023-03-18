import math
import random
import unittest
from linear_programming.classes.vector import Vector

class TestVector(unittest.TestCase):

    def test_get_rotate(self):
        v1 = Vector([1, 0])
        self.assertEqual(v1.get_rotate(math.pi/2), Vector([0, 1]))
        self.assertEqual(v1.get_rotate(math.pi), Vector([-1, 0]))
        self.assertEqual(v1.get_rotate(3*math.pi/2), Vector([0, -1]))

        v2 = Vector([2, 3])
        self.assertEqual(v2.get_rotate(math.pi/2), Vector([-3, 2]))
        self.assertEqual(v2.get_rotate(math.pi), Vector([-2, -3]))
        self.assertEqual(v2.get_rotate(3*math.pi/2), Vector([3, -2]))

    def test_degree_needed_to_rotate_to(self):
        v1 = Vector([1, 0])
        v2 = Vector([0, 1])
        self.assertAlmostEqual(v1.degree_needed_to_rotate_to(v2), math.pi/2)

        v3 = Vector([1, 1])
        v4 = Vector([1, -1])
        self.assertAlmostEqual(v3.degree_needed_to_rotate_to(v4), -math.pi/2)

        v5 = Vector([1, 0])
        v6 = Vector([-1, 0])
        self.assertAlmostEqual(v5.degree_needed_to_rotate_to(v6), math.pi)
        
    def test_degree_against_it_self(self):
        v1= Vector([1,1])
        # degree = random.uniform(0, 2*math.pi)  
        pi = math.pi
        
        for i in range(1000):
            degree =random.uniform(-pi, pi)
            rotated = v1.get_rotate(degree=degree)
            degree_get = v1.degree_needed_to_rotate_to(rotated)
            self.assertAlmostEqual(degree, degree_get)
        
