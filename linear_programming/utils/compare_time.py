from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.utils.exceptions import NoSolutionException, ResultNotEqualException
from linear_programming.utils.linear_program_generator import gen_random_2d_feasible
from typing import Tuple
from linear_programming.utils.problem_reader import Program
from linear_programming.classes.point import Point
import time
        

def test_data_feasible(range:range):
    convex_solve = ConvexSolver()
    os_tool_solve = OsToolSolver()
    file = open('feasible_data_comparison.txt', 'w',encoding='utf-8')
    for i in range:
        print(f"n={i}")
        program = gen_random_2d_feasible(i)
        os_res,os_time = solve_with_time(os_tool_solve, program)
        try:
            con_res,con_time = solve_with_time(convex_solve, program)
        except NoSolutionException as err:
            if not os_res == None:
                write_bad_program(program, None, os_res,err)
                raise NoSolutionException(f"convex solver has no solution and os tool has solution: {os_res} \n")
            
            
        
        if con_res != os_res:
            write_bad_program(program, con_res, os_res,"result not equal")
            file.close()
            raise ResultNotEqualException(program)

            
        file.write(f"convex time: {con_time} os time: {os_time} for n={i} \n")
        
    file.close()
        
            
        
        
def solve_with_time(solver, program) -> Tuple[Point, float]:
    start = time.time()
    res = solver.solve(program[0], program[1])
    end = time.time()
    return res, end-start

def write_bad_program(program:Program, con_res:Point, os_res:Point,err):
    with open('bad_program.txt', 'a+',encoding='utf-8') as f:
        f.write(str(err)+"\n")
        f.write(f"convex result: {con_res} os tool result: {os_res}\n")
        f.write(str(program[0])+"\n")
        for line in program[1]:
            f.write(str(line)+"\n")
        f.write("-----------------program end-----------------")