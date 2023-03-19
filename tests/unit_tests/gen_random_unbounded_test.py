import unittest
import linear_programming.utils.linear_program_generator as gen
from linear_programming.classes.osToolSolver import OsToolSolver
import linear_programming.utils.compare_time as compare


class TestRandomGenUnbound(unittest.TestCase):

    def test_random_gen_unbound(self):
        for i in range(100):
            obj, cons = gen.gen_random_2d_unbounded(i)
            solver = OsToolSolver()
            res = solver.solve(obj, cons)
            if res is not None:
                compare.write_bad_program((obj, cons), None, res, "suppose to be unbounded")
            self.assertTrue(res == None)