from linear_programming.classes.osToolSolver import OsToolSolver
import unittest
class TestOsToolSolver(unittest.TestCase):
    def test_import(self):
        self.assertTrue(OsToolSolver)
        solver = OsToolSolver()

if __name__ == '__main__':
    unittest.main()

