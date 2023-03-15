import unittest
from linear_programming.utils.linear_program_generator import gen_random_2d_feasible
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.utils.problem_reader import Program


class TestConvexSolver(unittest.TestCase):
    def test_basic_no_constraint(self):
        program: Program = gen_random_2d_feasible(0)
        solver = ConvexSolver()
        solver.solve(program[0], program[1])

