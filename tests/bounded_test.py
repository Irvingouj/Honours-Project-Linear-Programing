from linear_programming.utils.problem_reader import read_bounded_problem,Program
from linear_programming.classes.convexSolver import solve_with_convex
from linear_programming.classes.osToolSolver import solve_with_os_tool
import unittest

class TestBoundedProblem(unittest.TestCase):
    def test_problem_1(self):
        program:Program = read_bounded_problem(1)
        convex_sol = solve_with_convex(program)
        google_os_sol = solve_with_os_tool(program)
        
        self.assertEqual(convex_sol, google_os_sol)