import unittest
from linear_programming.classes.constraints import Constraints
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.utils.problem_reader import read_bounded_problem

class TestCheckBound(unittest.TestCase):
    def test_check_bound(self):
        c1 = Constraints(1, 3, c=1)
        c2 = Constraints(2, -5, c=2)
        c3 = Constraints(-1, -0.2, c=3)
        obj = ObjectiveFunction(1, 1)

        solver = ConvexSolver()
        
        result = solver.check_unbounded(obj, [c1, c2, c3])
        
        self.assertTrue(result.bounded)
        self.assertTrue(1 in result.bound_certificate)
        self.assertTrue(0 in result.bound_certificate)
        
    def test_boundedness_for_1_to_10(self):
        solver = ConvexSolver()
        for i in range(1,11):
            program = read_bounded_problem(i)
            result = solver.check_unbounded(program[0], program[1])
            self.assertTrue(result.bounded)
            
            
            