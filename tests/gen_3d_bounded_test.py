import unittest
from linear_programming.solvers.osToolSolver import OsToolSolver, Point3D
from linear_programming.utils.linear_program_generator import gen_random_3d_bounded

class TestRandom3DBounded(unittest.TestCase):
    def test_gen_random_3d_bounded(self):
        solver = OsToolSolver()
        for num_constraints in range(100, 10001, 100):
            program = gen_random_3d_bounded(num_constraints)
            obj = program[0]
            constraints = program[1]

            result = solver.solve_three_d(obj, constraints)

            self.assertFalse(isinstance(result, str), f"Generated program with {num_constraints} constraints returned a string result: {result}")
            self.assertIsInstance(result, Point3D, f"Generated program with {num_constraints} constraints does not return a Point3D")

if __name__ == '__main__':
    unittest.main()
