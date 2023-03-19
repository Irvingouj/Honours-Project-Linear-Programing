import unittest
from linear_programming.classes.convexSolver import ConvexSolver

from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.utils.exceptions import UnboundedException
from linear_programming.utils.problem_reader import Program,read_unbounded_problem

class UnboundedTest(unittest.TestCase):
    def __test_problem(self, program: Program):
        os_solver = OsToolSolver()
        os__res = os_solver.solve(program[0], program[1])

        con_solver = ConvexSolver()
        try:
            con_solver.solve(program[0], program[1])
        except UnboundedException:
            assert os__res is None
            #only this is accepted
            return
        
        raise Exception("should be unbounded")
    
    def test_problem_1(self):
        program: Program = read_unbounded_problem(1)
        self.__test_problem(program)
        
    def test_problem_2(self):
        program: Program = read_unbounded_problem(2)
        self.__test_problem(program)
        
    def test_problem_3(self):
        program: Program = read_unbounded_problem(3)
        self.__test_problem(program)

    def test_problem_4(self):
        program: Program = read_unbounded_problem(4)
        self.__test_problem(program)

    def test_problem_5(self):
        program: Program = read_unbounded_problem(5)
        self.__test_problem(program)

    def test_problem_6(self):
        program: Program = read_unbounded_problem(6)
        self.__test_problem(program)

    def test_problem_7(self):
        program: Program = read_unbounded_problem(7)
        self.__test_problem(program)

    def test_problem_8(self):
        program: Program = read_unbounded_problem(8)
        self.__test_problem(program)
    