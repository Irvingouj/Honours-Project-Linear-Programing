import time
import csv
from typing import Tuple
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.utils.exceptions import NoSolutionException, ResultNotEqualException, UnboundedException
from linear_programming.utils.linear_program_generator import gen_random_2d_feasible, gen_random_2d_infeasible, gen_random_2d_unbounded
from linear_programming.utils.problem_reader import PROJECT_ROOT, ProblemType
from linear_programming.utils.problem_writer import write_bad_program

TIME_DATA_DIR = PROJECT_ROOT.joinpath("time_data")

def solve_calculate_time(program) -> Tuple[float, float]:
    """
    Calculates the time taken by the convex solver and the os tool solver to solve a given program, 
    and returns the elapsed time for each solver.

    Args:
    program (Tuple): A tuple containing the problem to be solved as two elements: the coefficients of the linear
    equations and the right-hand side of the inequalities.

    Returns:
    Tuple[float, float]: A tuple containing the elapsed time for the convex solver and the os tool solver, respectively.

    Raises:
    NoSolutionException: If the convex solver has no solution and the os tool solver has a solution.
    UnboundedException: If the convex solver is unbounded and the os tool solver has a solution.
    ResultNotEqualException: If the result of the convex solver and the os tool solver is not equal.

    """
    convex_solver = ConvexSolver()
    os_tool_solver = OsToolSolver()
    
    os_time_start = time.time()
    os_res = os_tool_solver.solve(program[0], program[1])
    os_time_end = time.time()
    
    cons_time_start = time.time()
    con_res = None
    try:
        con_res = convex_solver.solve(program[0], program[1])
    except NoSolutionException as exc:
        if os_res is not None:
            write_bad_program(program, None, os_res,"convex solver has no solution but os tool has")
            raise ResultNotEqualException("convex solver has no solution but os tool has solution") from exc
    except UnboundedException as exc:
        if os_res is not None:
            write_bad_program(program, None, os_res,"convex solver has no solution but os tool has")
            raise ResultNotEqualException("convex solver is unbounded  but os tool has solution") from exc
        
    if os_res != con_res:
        write_bad_program(program, con_res, os_res,"result not equal")
        raise ResultNotEqualException("result not equal")
    
    cons_time_end = time.time()
    
    return cons_time_end - cons_time_start, os_time_end - os_time_start

    

def test_with_time(problem_type:ProblemType,range:range,result_name:str = "result.txt")->str:

    gen_func = None;
    if problem_type == ProblemType.UNBOUNDED:
        gen_func = gen_random_2d_unbounded
        result_name = "unbounded_"+result_name
    elif problem_type == ProblemType.INFEASIBLE:
        gen_func = gen_random_2d_infeasible
        result_name = "infeasible_"+result_name
    elif problem_type == ProblemType.BOUNDED:
        gen_func = gen_random_2d_feasible
        result_name = "bounded_"+result_name
    else:
        raise ValueError("problem type not supported")
    
    
    f = open(TIME_DATA_DIR.joinpath(result_name), 'w', encoding='utf-8')
    for n in range:
        print(f"testing for n = {n} \n")
        program = gen_func(num_constrains=n)
        cons_time, os_time = solve_calculate_time(program)
        csv.writer(f).writerow([n,cons_time,os_time])
    f.close()
    
    return TIME_DATA_DIR.joinpath(result_name)