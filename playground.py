
from linear_programming.classes.constraints import Constraints
from linear_programming.classes.convexSolver import ConvexSolver, get_one_d_optimize_direction, to_1d_constraint
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.classes.oneDLinearProgram import solve_1d_linear_program
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.classes.point import Point
from linear_programming.utils.problem_reader import read_bounded_problem,read_unexpected_problem

program = read_unexpected_problem("bounded_problem2")
cons = program[1]
p_con = ConvexSolver().solve(program[0], cons)
p = Point(22.43897,34.05724)
assert p_con == p
for c in cons:
    if not c.contains(p):
        print("this point is not in the constraint")
        print(c)




