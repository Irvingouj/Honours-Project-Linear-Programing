import multiprocessing
from linear_programming.utils.compare_time import test_with_time_3d
from linear_programming.utils.problem_reader import ProblemType



rang = range(100, 15001,400)
def gen_bounds(_):
    test_with_time_3d(problem_type=ProblemType.BOUNDED, rang=rang)
def gen_unbounded(_):
    test_with_time_3d(problem_type=ProblemType.UNBOUNDED, rang=rang)
def gen_infeasible(_):
    test_with_time_3d(problem_type=ProblemType.INFEASIBLE, rang=rang)

    
if __name__ == "__main__":
    with multiprocessing.Pool(10) as p:
        p.map(gen_bounds, [None]*20)
        p.map(gen_unbounded, [None]*20)
        p.map(gen_infeasible, [None]*20)
    print("done")