from concurrent.futures import ThreadPoolExecutor
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.utils.graph import show_feasible_region,show_vectors
from linear_programming.utils.problem_reader import read_bounded_problem
from linear_programming.utils.linear_program_generator import gen_random_2d_feasible

obj,cons = gen_random_2d_feasible(10)

vectors = [c.facing_normal_vector() for c in cons]
names = [str(c) for c in cons]

obj = ObjectiveFunction(1,1).to_vector()
name = 'obj'

vectors.append(obj)
names.append(name)

show_vectors(vectors,names)
show_feasible_region(cons)
