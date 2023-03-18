from linear_programming.utils.problem_reader import read_bounded_problem, read_infeasible_problem, Program
from linear_programming.classes.convexSolver import solve_with_convex
from linear_programming.classes.osToolSolver import solve_with_os_tool
from linear_programming.utils.exceptions import NoSolutionException

import unittest


class TestInfeasibleProblems(unittest.TestCase):
    def __test__program(self, program: Program):
        google_os_sol = solve_with_os_tool(program)
        try:
            convex_sol = solve_with_convex(program)
        except NoSolutionException:
            self.assertTrue(google_os_sol == None)
            return
        
        if google_os_sol is not None:
            raise Exception('THis problem should be infeasible')
         
        raise Exception('Convex solver should raise NoSolutionException')

    def test_problem_1(self):
        program: Program = read_infeasible_problem(1)
        self.__test__program(program)

    def test_problem_2(self):
        program: Program = read_infeasible_problem(2)
        self.__test__program(program)

    def test_problem_3(self):
        program: Program = read_infeasible_problem(3)
        self.__test__program(program)

    def test_problem_4(self):
        program: Program = read_infeasible_problem(4)
        self.__test__program(program)

    def test_problem_5(self):
        program: Program = read_infeasible_problem(5)
        self.__test__program(program)

    def test_problem_6(self):
        program: Program = read_infeasible_problem(6)
        self.__test__program(program)

    def test_problem_7(self):
        program: Program = read_infeasible_problem(7)
        self.__test__program(program)
        
    def test_problem_8(self):
        program: Program = read_infeasible_problem(8)
        self.__test__program(program)
