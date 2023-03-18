
from linear_programming.classes.constraints import Constraints
from linear_programming.classes.convexSolver import ConvexSolver, get_one_d_optimize_direction, to_1d_constraint
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.classes.oneDLinearProgram import solve_1d_linear_program
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.utils.problem_reader import read_bounded_problem

con_solver = ConvexSolver()
os_solver = OsToolSolver()

program = read_bounded_problem(1)

con_sol = con_solver.solve(program[0], program[1])
os_sol = os_solver.solve(program[0], program[1])

print(con_sol)
print(os_sol)




