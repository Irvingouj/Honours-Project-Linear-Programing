import unittest
from linear_programming.classes.convexSolver import solve_with_convex
from linear_programming.classes.osToolSolver import solve_with_os_tool
from linear_programming.utils.exceptions import NoSolutionException
from linear_programming.utils.problem_reader import read_problem,ProblemType
from linear_programming.utils.types import Program



class TestInfeasibleProblems(unittest.TestCase):
    def __test__program(self, program: Program):
        google_os_sol = solve_with_os_tool(program)
        try:
            solve_with_convex(program)
        except NoSolutionException:
            self.assertTrue(google_os_sol is None)
            return
        
        if google_os_sol is not None:
            self.fail('Google os tool should not find solution')
         
        self.fail('Convex solver should not find solution')

    def test_problem_1(self):
        program: Program = read_problem(ProblemType.INFEASIBLE,1)
        self.__test__program(program)

    def test_problem_2(self):
        program: Program = read_problem(ProblemType.INFEASIBLE,2)
        self.__test__program(program)

    def test_problem_3(self):
        program: Program = read_problem(ProblemType.INFEASIBLE,3)
        self.__test__program(program)

    def test_problem_4(self):
        program: Program = read_problem(ProblemType.INFEASIBLE,4)
        self.__test__program(program)

    def test_problem_5(self):
        program: Program = read_problem(ProblemType.INFEASIBLE,5)
        self.__test__program(program)

    def test_problem_6(self):
        program: Program = read_problem(ProblemType.INFEASIBLE,6)
        self.__test__program(program)

    def test_problem_7(self):
        program: Program = read_problem(ProblemType.INFEASIBLE,7)
        self.__test__program(program)
        
    def test_problem_8(self):
        program: Program = read_problem(ProblemType.INFEASIBLE,8)
        self.__test__program(program)
