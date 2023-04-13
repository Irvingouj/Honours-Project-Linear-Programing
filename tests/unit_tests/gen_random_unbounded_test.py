import unittest
import linear_programming.utils.linear_program_generator as gen
from linear_programming.solvers.or_tool_solver import OrToolSolver
import linear_programming.utils.compare_time as compare


class TestRandomGen(unittest.TestCase):

    def test_random_gen_unbound(self):
        for i in range(100):
            obj, cons = gen.gen_random_2d_unbounded(i)
            solver = OrToolSolver()
            res = solver.solve(obj, cons)
            if res is not 'UNBOUNDED':
                compare.write_bad_program((obj, cons), None, res, "suppose to be unbounded")
            self.assertTrue(res == 'UNBOUNDED')

    def test_random_gen_unbounded_3d(self):
        for i in range(100):
            obj, cons = gen.gen_random_3d_unbounded(i*10)
            solver = OrToolSolver()
            res = solver.solve_three_d(obj, cons)
            if res is not 'UNBOUNDED':
                compare.write_bad_program((obj, cons), None, res, "suppose to be unbounded")
            self.assertTrue(res == 'UNBOUNDED')
            
    def test_random_gen_infeasible(self):
        for i in range(100):
            obj, cons = gen.gen_random_2d_infeasible(i+10)
            solver = OrToolSolver()
            res = solver.solve(obj, cons)
            if res is not 'INFEASIBLE':
                compare.write_bad_program((obj, cons), None, res, "suppose to be infeasible")
            self.assertTrue(res == 'INFEASIBLE')