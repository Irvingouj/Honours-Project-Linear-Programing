import math
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.vector import Vector
from linear_programming.classes.constraints import Constraints
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.utils.problem_reader import read_bounded_problem, read_unbounded_problem

obj,cons = read_bounded_problem(3)
solver = ConvexSolver();
res = solver.check_unbounded(obj,cons)

print(res)
# c1 = Constraints(1,1,c=1)
# c2 = Constraints(1,-1,c=1)
# obj = ObjectiveFunction(1,12)

# degree = obj.to_vector().degree_needed_to_rotate_to(Vector([0,1]))
# c1_rotate = c1.get_rotate_around_origin(degree)
# c2_rotate = c2.get_rotate_around_origin(degree)

# print(degree == math.pi/4)
# print(c1_rotate)
# print(c2_rotate)
# print(c1.facing_normal_vector())
# print(c2.facing_normal_vector())