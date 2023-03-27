import unittest
from linear_programming.classes.three_d import Constraints3D
from linear_programming.classes.three_d import Point3D
from random import randint

class TestConstraints3D(unittest.TestCase):
    
    def __random_constraint3d(self):
        a, b, c = randint(-10, 10), randint(-10, 10), randint(-10, 10)
        while a == 0 or b == 0 or c == 0:
            a, b, c = randint(-10, 10), randint(-10, 10), randint(-10, 10)
        return Constraints3D(a, b, c,d=randint(-10, 10))

    def test_from_string(self):
        c1 = Constraints3D.from_string('2x + 3y + -4z <= 5')
        self.assertAlmostEqual(c1.a, 2)
        self.assertAlmostEqual(c1.b, 3)
        self.assertAlmostEqual(c1.c, -4)
        self.assertAlmostEqual(c1.d, 5)
        c2 = Constraints3D.from_string('-1x + 0.5y + 1z >= -1.5')
        self.assertAlmostEqual(c2.a, 1)
        self.assertAlmostEqual(c2.b, -0.5)
        self.assertAlmostEqual(c2.c, -1)
        self.assertAlmostEqual(c2.d, 1.5)

    def test_contains(self):
        c1 = Constraints3D(2, 3, -4, d=5)
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(0, 0, -2)
        self.assertTrue(c1.contains(p1))
        self.assertFalse(c1.contains(p2))

    # def test_find_intersection(self):
    #     c1 = Constraints3D(2, 3, -4, d=5)
    #     c2 = Constraints3D(-1, 0.5, 1, GreaterOrLess.GREATER, d=-1.5)
    #     p1 = c1.find_intersection(c2)
    #     self.assertAlmostEqual(p1.x, -0.2941176470588235)
    #     self.assertAlmostEqual(p1.y, -0.5882352941176471)
    #     self.assertAlmostEqual(p1.z, -1.1764705882352942)

    def test_get_vector_space(self):
        c1 = self.__random_constraint3d()
        v1, v2 = c1.get_vector_space()
        p = c1.find_random_point_on_plane()
        
        p1 = Point3D(p.x + v1[0], p.y + v1[1], p.z + v1[2])
        p2 = Point3D(p.x + v2[0], p.y + v2[1], p.z + v2[2])
        
        self.assertAlmostEqual(p1.x * c1.a + p1.y * c1.b + p1.z * c1.c,c1.d)
        self.assertAlmostEqual(p2.x * c1.a + p2.y * c1.b + p2.z * c1.c,c1.d)
    
    def test_random_point(self):
        c1 = Constraints3D(2, 3, -4, d=5)
        p = c1.find_random_point_on_plane()
        p_on_plane = p.x * c1.a + p.y * c1.b + p.z * c1.c == c1.d
        self.assertTrue(p_on_plane)
        
    def test_perpendicular(self):
        c1 = Constraints3D(2, 3, -4, d=5)
        perpendicular_vec = c1.get_perpendicular_vector()
        vec_space = c1.get_vector_space()
        
        self.assertTrue(perpendicular_vec*vec_space[0] == 0)
        self.assertTrue(perpendicular_vec*vec_space[1] == 0)
        
    def test_facing_direction(self):
        c1 = Constraints3D(2, 3, -4, d=5)
        facing_direction_vec = c1.facing_direction_vector()
        p = c1.find_random_point_on_plane()
        
        vec_space = c1.get_vector_space()
        
        p1 = Point3D(p.x + facing_direction_vec[0], p.y + facing_direction_vec[1], p.z + facing_direction_vec[2])
        
        self.assertTrue(facing_direction_vec*vec_space[0] == 0)
        self.assertTrue(facing_direction_vec*vec_space[1] == 0)
        self.assertTrue(c1.contains(p1))
        

if __name__ == '__main__':
    unittest.main()
