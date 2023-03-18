
import random
from linear_programming.classes.constraints import Constraints
from linear_programming.classes.convexSolver import ConvexSolver, get_one_d_optimize_direction, to_1d_constraint
from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.classes.oneDLinearProgram import solve_1d_linear_program
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.classes.point import Point
from linear_programming.utils.compare_time import write_bad_program
from linear_programming.utils.exceptions import NoSolutionException
from linear_programming.utils.problem_reader import Program, read_bounded_problem,read_unexpected_problem
from linear_programming.utils.analysis import con_solve, os_solve, re_arrange_cons

long = "(35.87805,38.05864)!=None__0.1503365282262642.txt"
short = "(35.87805,38.05864)!=None__0.19204466561538835.txt"

def analysis_bad_program(filename):
    program = read_unexpected_problem(filename=filename)
    cons = program[1]
    idx_differ = []
    for i in range(4,len(cons)+1):
        p_os = OsToolSolver().solve(program[0],  cons[:i])
        p_con = ConvexSolver().solve(program[0], cons[:i])
        print("--------------------------------------" + str(i))
        print(p_con)
        print(p_os)
        print()
        if(p_con != p_os):
            write_bad_program((program[0],cons[:i+1]), p_con, p_os, "result not equal at index" + str(i))
            idx_differ.append(i)
            break
    print("done")
    print(idx_differ)
    
def analysis_bad_program_no_export(filename):
    obj,cons = read_unexpected_problem(filename=filename)
    poped = cons[:5]
    while True:
        pop = re_arrange_cons(obj,cons)
        print(pop)
        if pop in poped:
            break
        poped.append(pop)
        
    p_os = os_solve(obj, poped)
    p_cos = con_solve(obj, poped) 
    print(p_os)
    print(p_cos)
    print(obj)
    write_bad_program((obj,poped), p_cos, p_os, "truncated program")
    

# def randomly_remove_constraints_with_same_result(program:Program):
#     obj = program[0]
#     cons = program[1]
#     cons_removed = []
#     while True:
#         idx = random.randint(0,len(cons)-1)
#         con_removed=cons.pop(idx)
#         p_os = OsToolSolver().solve(program[0],  cons)
#         try:
#             p_con = ConvexSolver().solve(program[0], cons)
#         except NoSolutionException:
#             p_con = None
            
#         if(p_con != p_os):
#             cons.append(con_removed)
#         cons_removed.append(con_removed)
            

analysis_bad_program_no_export(short)
