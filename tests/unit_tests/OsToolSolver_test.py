from linear_programming.solvers.or_tool_solver import OrToolSolver
import unittest


class TestOsToolSolver(unittest.TestCase):
    def test_import(self):
        self.assertTrue(OrToolSolver)
        solver = OrToolSolver()


if __name__ == '__main__':
    unittest.main()
