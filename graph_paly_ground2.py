from concurrent.futures import ThreadPoolExecutor
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.utils.graph import show_feasible_region,show_vectors
from linear_programming.utils.problem_reader import read_bounded_problem, read_unbounded_problem
from linear_programming.utils.linear_program_generator import gen_random_2d_feasible,gen_random_2d_unbounded

obj,cons = gen_random_2d_unbounded(num_constrains=10)

vectors = [c.facing_normal_vector() for c in cons]
names = [str(c) for c in cons]

obj_vec = ObjectiveFunction(1,1).to_vector()
name = 'obj'

vectors.append(obj_vec)
names.append(name)

print(obj)

show_vectors(vectors,names)
show_feasible_region(obj,cons,x_left=-500,x_right=500,y_bottom=-500,y_top=500)
