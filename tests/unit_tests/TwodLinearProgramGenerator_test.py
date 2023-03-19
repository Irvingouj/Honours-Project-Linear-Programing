import unittest
from  linear_programming.utils.linear_program_generator import gen_random_2d_feasible
from linear_programming.classes.osToolSolver import OsToolSolver
import os


class TestGenerateRandomLP(unittest.TestCase):
    def test_generates_correct_number_of_constraints(self):
        num_of_constraints = 5

        _obj, cons = gen_random_2d_feasible(
            num_of_constraints)
        self.assertEqual(len(cons), num_of_constraints)

    def test_generates_correct_number_of_constraints2(self):
        num_of_constraints = 100

        _obj, cons = gen_random_2d_feasible(
            num_of_constraints)
        self.assertEqual(len(cons), num_of_constraints)

    def test_generates_feasible_lp(self):
        num_of_constraints = 100
        #
        obj, cons = gen_random_2d_feasible(
            num_of_constraints)
        solver = OsToolSolver()
        res = solver.solve(cons=cons, obj=obj)
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
