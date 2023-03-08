import unittest
from LinearProgramming.Utils.twodLinearProgramGenerator import generate_random_2d_feasible_linear_program, generate_to_file
from LinearProgramming.Classes.OsToolSolver import OsToolSolver
import os
class TestGenerateRandomLP(unittest.TestCase):
    def test_generates_correct_number_of_constraints(self):
        num_of_constraints = 5

        _obj,cons = generate_random_2d_feasible_linear_program(num_of_constraints)
        self.assertEqual(len(cons), num_of_constraints)

    def test_generates_correct_number_of_constraints2(self):
        num_of_constraints = 100

        _obj,cons = generate_random_2d_feasible_linear_program(num_of_constraints)
        self.assertEqual(len(cons), num_of_constraints)

    def test_generates_feasible_lp(self):
        num_of_constraints = 100
        #
        obj,cons = generate_random_2d_feasible_linear_program(num_of_constraints)
        solver = OsToolSolver();
        res = solver.solve(cons=cons, obj=obj)
        self.assertIsNotNone(res)

    def test_file_created(self):
        # Generate a new LP file and check if it exists
        file_name = "test_lp.txt"
        file_path = generate_to_file(2, 100, file_name)
        self.assertTrue(os.path.isfile(file_path))

        # Clean up the test file
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
