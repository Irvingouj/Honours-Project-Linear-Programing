 
from linear_programming.solvers import convex_solver_3d
from linear_programming.solvers.convexSolver import ConvexSolver
from linear_programming.solvers.convex_solver_3d import Convex3DSolver
from linear_programming.utils.linear_program_generator import gen_random_3d_unbounded
from linear_programming.solvers.osToolSolver import OsToolSolver
from linear_programming.utils.problem_reader import read
import linear_programming.utils.debug as dbg
import random
from linear_programming.solvers import Convex3DSolver
from linear_programming.utils import *

obj,cons = read(r'linear_program_data\problems_unexpected\2d__in_3',2)
print(obj)
for c in cons:
    print(c)
consolver = ConvexSolver()
osolver = OsToolSolver()

os_res = OsToolSolver().solve(obj,cons)
print(os_res)
c_res = ConvexSolver().solve(obj,cons)

print(f"convex: {c_res}, os: {os_res}")