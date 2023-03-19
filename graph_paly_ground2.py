from linear_programming.utils.graph import show_feasible_region,show_vectors
from linear_programming.utils.problem_reader import read_bounded_problem

obj,cons = read_bounded_problem(3)

vectors = [c.facing_normal_vector() for c in cons]
names = [str(c) for c in cons]

show_vectors(vectors,names)
# show_feasible_region(cons)
