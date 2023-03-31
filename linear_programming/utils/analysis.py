import random
from linear_programming.classes import constraints
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.utils.exceptions import NoSolutionException, UnboundedException
from linear_programming.utils.types import Program
import linear_programming.utils.problem_reader as reader


def con_solve(obj,cons):
    try:
        p_cons = ConvexSolver().solve(obj, cons)
    except NoSolutionException:
        return "INFEASIBLE"
    except UnboundedException:
        return "UNBOUNDED"
    return p_cons

def os_solve(obj,cons):
    p_os = OsToolSolver().solve(obj, cons)
    return p_os


def find_first_line_diff(obj,cons):
    for i in range(len(cons)+1):
        os_res = os_solve(obj, cons[:i])
        con_res = con_solve(obj, cons[:i])
        if(os_res != con_res):
            return i,os_res,con_res
    return None,None,None

def find_first_line_diff_3d(obj,cons):
    pass

def trim_off_and_try_again(num,obj,cons):
    """
    return true means that the results are the same 
    """
    cons = cons[num:]
    diff,os_res,cons_res = find_first_line_diff(obj,cons)
    # it is the same
    if(diff == None):
        return True
    return False

def result_is_not_same(obj,cons):
    diff,os_res,cons_res = find_first_line_diff(obj,cons)
    if(diff == None):
        return False
    return True

def re_arrange_cons(obj,cons) -> Program:
    """
    this method grabs the first bad constraint and moves it to the top of the list
    """
    bad_index,_,_ = find_first_line_diff(obj,cons)
    if(bad_index == None):
        return cons
    else:
        bad_cons = cons[bad_index-1]
        cons.remove(bad_cons)
        cons.insert(0,bad_cons)
        return obj,cons
    
def test_all_file_unexpected():
    programs_with_name = reader.read_all_problem_in_dir("problems_unexpected")
    for (name,program) in programs_with_name:
        obj,cons = program
        print(name)
        con_res = con_solve(obj,cons)
        os_res = os_solve(obj,cons)
        print(f"con_res: {con_res}, os_res: {os_res}, same: {con_res == os_res}\n")
        print("---------------------------------")
    
def trim_cons(obj,cons):
    """
    this method will trim off the first constraint that is causing the problem
    """
    bad_index,_,_ = find_first_line_diff(obj,cons)
    if(bad_index == None):
        return cons
    else:
        bad_cons = cons[bad_index-1]
        cons.remove(bad_cons)
        return obj,cons

def full_analysis(obj,cons):
    """
    this method will try to find the first constraint that is causing the problem
    """
    bad_index,_,_ = find_first_line_diff(obj,cons)
    cons = cons[:bad_index]
    prev = None
    while bad_index!=prev:
        re_arrange_cons(obj,cons)
        bad_index,_,_ = find_first_line_diff(obj,cons)
        cons = cons[:bad_index]
        prev = bad_index
    
    try_counter = 0
    while try_counter < 50:
        random_int = random.randint(0,len(cons)-1)
        con_copy = [c for i,c in enumerate(cons) if i != random_int]
        bad_index,_,_ = find_first_line_diff(obj,cons)
        if bad_index != None:
            cons = con_copy
        else:
            try_counter += 1
    
    return obj,cons
    