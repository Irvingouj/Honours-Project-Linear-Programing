from linear_programming.classes import constraints
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.utils.exceptions import NoSolutionException, UnboundedException


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

def re_arrange_cons(obj,cons) -> constraints.Constraints:
    """
    this method grabs the first bad constraint and moves it to the top of the list
    """
    bad_index = find_first_line_diff(obj,cons)
    if(bad_index == None):
        return cons
    else:
        bad_cons = cons[bad_index-1]
        cons.remove(bad_cons)
        cons.insert(0,bad_cons)
        return cons
    
    
