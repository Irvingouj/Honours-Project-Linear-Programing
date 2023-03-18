import time
import unittest
from linear_programming.utils.exceptions import NoSolutionException
from linear_programming.utils.problem_reader import read_bounded_problem, Program, read_unexpected_problem
from linear_programming.classes.convexSolver import solve_with_convex
from linear_programming.classes.osToolSolver import solve_with_os_tool


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
            res = f'convex time: {str(con_end - con_time)} os time: {str(os_end - os_time)} for n = {str(len(program[1]))} \n'
            lines = f.readlines()
            if res not in lines:
                f.write(res)
            
        self.assertTrue(convex_sol == google_os_sol)
        
    def test_problem_unexpected(self):
        program: Program = read_unexpected_problem('bounded_problems1')
        convex_sol = solve_with_convex(program)
        google_os_sol = solve_with_os_tool(program)
        self.assertTrue(convex_sol == google_os_sol)
        

    def test_problem_1(self):
        program: Program = read_bounded_problem(1)
        self.__test__program(program)

    def test_problem_2(self):
        program: Program = read_bounded_problem(2)
        self.__test__program(program)

    def test_problem_3(self):
        program: Program = read_bounded_problem(3)
        self.__test__program(program)

    def test_problem_4(self):
        program: Program = read_bounded_problem(4)
        self.__test__program(program)

    def test_problem_5(self):
        program: Program = read_bounded_problem(5)
        self.__test__program(program)

    def test_problem_6(self):
        program: Program = read_bounded_problem(6)
        self.__test__program(program)

    def test_problem_7(self):
        program: Program = read_bounded_problem(7)
        self.__test__program(program)

    def test_problem_8(self):
        program: Program = read_bounded_problem(8)
        self.__test__program(program)

    def test_problem_9(self):
        program: Program = read_bounded_problem(9)
        self.__test__program(program)
        
    def test_problem_10(self):
        program: Program = read_bounded_problem(10)
        self.__test__program(program)
        
    def test_problem_11(self):
        program: Program = read_bounded_problem(11)
        self.__test__program(program)
        
    def test_problem_12(self):
        program: Program = read_bounded_problem(12)
        self.__test__program(program)
        
    def test_problem_13(self):
        program: Program = read_bounded_problem(13)
        self.__test__program(program)
        
    def test_problem_14(self):
        program: Program = read_bounded_problem(14)
        self.__test__program(program)
        
    def test_problem_15(self):
        program: Program = read_bounded_problem(15)
        self.__test__program(program)
