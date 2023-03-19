import time
import unittest
from linear_programming.utils.exceptions import NoSolutionException
from linear_programming.classes.convexSolver import solve_with_convex
from linear_programming.classes.osToolSolver import solve_with_os_tool
from linear_programming.utils.problem_reader import read_problem,ProblemType,read_unexpected_problem
from linear_programming.utils.types import Program


class TestBoundedProblems(unittest.TestCase):
    def __test__program(self, program: Program):
        con_time = time.time()
        try:
            convex_sol = solve_with_convex(program)
        except NoSolutionException as err:
            print(err)
            convex_sol = None
        con_end = time.time()
        
        os_time = time.time()
        google_os_sol = solve_with_os_tool(program)
        os_end = time.time()
        
        with open('time_comparison_bounded.txt', 'a+',encoding='utf-8') as f:
            n = len(program[1])
            res = f'convex time: {str(con_end - con_time)} os time: {str(os_end - os_time)} for n={n} \n'
            f.seek(0)
            lines = f.readlines()
            n_in_lines = [line.split("n=")[1].removesuffix(' \n') for line in lines]
            if str(n) not in n_in_lines:
                f.write(res)
            
        self.assertTrue(convex_sol == google_os_sol)
        
    def test_problem_unexpected(self):
        program: Program = read_unexpected_problem('bounded_problems1')
        convex_sol = solve_with_convex(program)
        google_os_sol = solve_with_os_tool(program)
        self.assertTrue(convex_sol == google_os_sol)
        

    def test_problem_1(self):
        program: Program = read_problem(ProblemType.BOUNDED, 1)
        self.__test__program(program)

    def test_problem_2(self):
        program: Program = read_problem(ProblemType.BOUNDED,2)
        self.__test__program(program)

    def test_problem_3(self):
        program: Program = read_problem(ProblemType.BOUNDED,3)
        self.__test__program(program)

    def test_problem_4(self):
        program: Program = read_problem(ProblemType.BOUNDED,4)
        self.__test__program(program)

    def test_problem_5(self):
        program: Program = read_problem(ProblemType.BOUNDED,5)
        self.__test__program(program)

    def test_problem_6(self):
        program: Program = read_problem(ProblemType.BOUNDED,6)
        self.__test__program(program)

    def test_problem_7(self):
        program: Program = read_problem(ProblemType.BOUNDED,7)
        self.__test__program(program)

    def test_problem_8(self):
        program: Program = read_problem(ProblemType.BOUNDED,8)
        self.__test__program(program)

    def test_problem_9(self):
        program: Program = read_problem(ProblemType.BOUNDED,9)
        self.__test__program(program)
        
    def test_problem_10(self):
        program: Program = read_problem(ProblemType.BOUNDED,10)
        self.__test__program(program)
        
    def test_problem_11(self):
        program: Program = read_problem(ProblemType.BOUNDED,11)
        self.__test__program(program)
        
    def test_problem_12(self):
        program: Program = read_problem(ProblemType.BOUNDED,12)
        self.__test__program(program)
        
    def test_problem_13(self):
        program: Program = read_problem(ProblemType.BOUNDED,13)
        self.__test__program(program)
        
    def test_problem_14(self):
        program: Program = read_problem(ProblemType.BOUNDED,14)
        self.__test__program(program)
        
    def test_problem_15(self):
        program: Program = read_problem(ProblemType.BOUNDED,15)
        self.__test__program(program)

    def test_problem_16(self):
        program: Program = read_problem(ProblemType.BOUNDED,16)
        self.__test__program(program)
