import time
import csv
import threading
from typing import Tuple
import uuid

import numpy as np
from linear_programming.classes.two_d import ObjectiveFunction
from linear_programming.utils.exceptions import NoSolutionException, ResultNotEqualException, UnboundedException, PerceptionException
from linear_programming.utils.linear_program_generator import gen_random_2d_feasible, gen_random_2d_infeasible, gen_random_2d_unbounded, gen_random_3d_bounded, gen_random_3d_infeasible, gen_random_3d_unbounded
from linear_programming.utils.problem_reader import PROJECT_ROOT, ProblemType
from linear_programming.utils.problem_writer import write_bad_3d_program, write_bad_program, write_bad_program_no_analysis
from linear_programming.solvers import Convex3DSolver, OsToolSolver,ConvexSolver

TIME_DATA_DIR_2d = PROJECT_ROOT.joinpath("time_data").joinpath("2d")
TIME_DATA_DIR_3d = PROJECT_ROOT.joinpath("time_data").joinpath("3d")


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
        obj:ObjectiveFunction = program[0]
        if np.isclose(obj.value(os_res) ,obj.value(con_res)):
            write_bad_program(program, con_res, os_res, "result not equal")
            raise ResultNotEqualException("result not equal")
    except NoSolutionException:
        if os_res != "INFEASIBLE":
            thread = threading.Thread(target=write_bad_program_no_analysis, args=(
                program, "INFEASIBLE", os_res, f"convex solver has no solution but os tool has {os_res} \n"))
            thread.start()
    except UnboundedException:
        if os_res != "UNBOUNDED":
            thread = threading.Thread(target=write_bad_program_no_analysis, args=(
                program, "UNBOUNDED", os_res,
                              f"convex solver is unbounded  but os tool has solution {os_res} \n"))
            thread.start()

    cons_time_end = time.time()
    return cons_time_end - cons_time_start, os_time_end - os_time_start


def retry(size, gen_func):
    try:
        return solve_calculate_time(gen_func(num_constrains=size))
    except PerceptionException:
        retry(size, gen_func)


def test_with_time(problem_type: ProblemType, range: range, result_name: str = "result.txt") -> str:

    gen_func = None
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

    f = open(TIME_DATA_DIR_2d.joinpath(result_name), 'w', encoding='utf-8')
    f.write("n,convex_time,os_time\n")
    for n in range:
        print(f"testing for n = {n} \n")
        program = gen_func(num_constrains=n)
        try:
            cons_time, os_time = solve_calculate_time(program)
        except PerceptionException:
            print("retrying, something went wrong,perception error")
            cons_time, os_time = retry(n, gen_func)
        csv.writer(f).writerow([n, cons_time, os_time])
    f.close()

    return TIME_DATA_DIR_2d.joinpath(result_name)



def solve_with_time_3d(obj,cons) -> Tuple[float,float]:
    c_start_time = time.time()
    c_res = Convex3DSolver.con_solve(obj,cons)
    c_total_time = time.time() - c_start_time
    
    o_start_time = time.time()
    o_res = o_res = OsToolSolver.solve3d(obj,cons)
    o_total_time = time.time() - o_start_time
    
    if o_res != c_res:
        write_bad_3d_program((obj,cons))
        return None,None
    return c_total_time,o_total_time


def test_with_time_3d(problem_type: ProblemType, rang:range):
    match problem_type:
        case ProblemType.UNBOUNDED:
            gen_func = gen_random_3d_unbounded
        case ProblemType.INFEASIBLE:
            gen_func = gen_random_3d_infeasible
        case ProblemType.BOUNDED:
            gen_func = gen_random_3d_bounded
        case _:
            raise ValueError("problem type not supported")
    
    data_file = open(TIME_DATA_DIR_3d.joinpath(f"{problem_type}_{str(uuid.uuid4())}"), 'w', encoding='utf-8')
    n = 0
    counter = 0
    while True:
        n = rang[counter]
        try:
            program = gen_func(num_constrains=n)
            c_time,o_time = solve_with_time_3d(*program)
            if c_time is None or o_time is None:
                continue
            print(f"n = {n}")
            counter += 1
            data_file.write(f"{n},{c_time},{o_time}\n")
        except Exception as e:
            print("retrying, something went wrong,error: ",type(e).__name__,e)
            write_bad_3d_program(program)
            continue
        if counter >= len(rang):
            break
    data_file.close()