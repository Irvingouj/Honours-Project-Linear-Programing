import unittest

from linear_programming.utils.linear_program_generator import OneDProgram, gen_random_1d_feasible
from linear_programming.classes.one_d.one_d_LinearProgram import solve_1d_linear_program
from linear_programming.solvers.or_tool_solver import OrToolSolver

class TestOneDSolver(unittest.TestCase):
    
    def compare_to_os_tool(self, program: OneDProgram,sol):
        solver = OrToolSolver()
        res = solver.solve_one_dimension(objective=program[0], one_d_constraints=program[1])
        self.assertTrue(sol == res)
    
    def test_basic_no_constraint(self):
        program: OneDProgram = gen_random_1d_feasible(0)
        value = solve_1d_linear_program(objective=program[0], one_d_constraints=program[1])
        
        self.assertTrue(value != None)
        
    def test_5_constraints(self):
        program: OneDProgram = gen_random_1d_feasible(5)
        value = solve_1d_linear_program(objective=program[0], one_d_constraints=program[1])
        
        self.compare_to_os_tool(program, value)
        
    def test_100_constraints(self):
        program: OneDProgram = gen_random_1d_feasible(100)
        value = solve_1d_linear_program(objective=program[0], one_d_constraints=program[1])
                
        self.compare_to_os_tool(program, value)
        
    def test_1000_constraints(self):
        program: OneDProgram = gen_random_1d_feasible(1000)
        value = solve_1d_linear_program(objective=program[0], one_d_constraints=program[1])
                
        self.compare_to_os_tool(program, value)
        
    def test_10000_constraints(self):
        program: OneDProgram = gen_random_1d_feasible(10000)
        value = solve_1d_linear_program(objective=program[0], one_d_constraints=program[1])
                
        self.compare_to_os_tool(program, value)
        
    def test_100000_constraints(self):
        program: OneDProgram = gen_random_1d_feasible(100000)
        value = solve_1d_linear_program(objective=program[0], one_d_constraints=program[1])
                
        self.compare_to_os_tool(program, value)
