import multiprocessing
from linear_programming.utils.compare_time import test_with_time_3d
from linear_programming.utils.problem_reader import ProblemType



rang = range(100, 10001,300)
def gen_bounds():
    test_with_time_3d(problem_type=ProblemType.BOUNDED, rang=rang)
def gen_unbounded():
    test_with_time_3d(problem_type=ProblemType.UNBOUNDED, rang=rang)
def gen_infeasible():
    test_with_time_3d(problem_type=ProblemType.INFEASIBLE, rang=rang)

    
if __name__ == "__main__":
    with multiprocessing.Pool(10) as p:
        p.map(gen_bounds, [None]*10)
        p.map(gen_unbounded, [None]*10)
        p.map(gen_infeasible, [None]*10)
    print("done")