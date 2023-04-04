import unittest
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.classes.three_d import Convex3DSolver
from linear_programming.utils.linear_program_generator import gen_random_3d_unbounded
from linear_programming.utils.problem_writer import write_bad_program_no_analysis

from linear_programming.utils.types import Program3d


class UnboundedTest(unittest.TestCase):
    def __test_problem(self, program: Program3d):
        obj, cons = program
        os_solver = OsToolSolver()
        os_res = os_solver.solve_three_d(obj, cons)

        con_solver = Convex3DSolver()
        
        bounded = con_solver.check_bounded(obj, cons)
        if bounded and os_res == "UNBOUNDED":
            return
         
        write_bad_program_no_analysis(program, None, os_res, "suppose to be unbounded")
        self.fail("Unbounded problem was not detected")
        
    def test_unbounded_1(self):
        for i in range(100):
            program = gen_random_3d_unbounded(i+3)
            self.__test_problem(program)
        
    # def test_unbounded_2(self):
    #     program = gen_random_3d_unbounded(10)
    #     self.__test_problem(program)
        
    # def test_unbounded_3(self):
    #     program = gen_random_3d_unbounded(50)
    #     self.__test_problem(program)
        
    # def test_unbounded_4(self):
    #     program = gen_random_3d_unbounded(500)
    #     self.__test_problem(program)
        
    # def test_unbounded_5(self):
    #     program = gen_random_3d_unbounded(1000)
    #     self.__test_problem(program)