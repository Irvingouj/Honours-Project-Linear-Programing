from linear_programming.classes import constraints
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.utils.exceptions import NoSolutionException, UnboundedException


def con_solve(obj,cons):
    try:
        p_cons = ConvexSolver().solve(obj, cons)
    except NoSolutionException:
        return None
    except UnboundedException:
        return None
    return p_cons

def os_solve(obj,cons):
    p_os = OsToolSolver().solve(obj, cons)
    return p_os


def find_first_line_diff(obj,cons):
    for i in range(len(cons)+1):
        p_os = os_solve(obj, cons[:i])
        p_cons = con_solve(obj, cons[:i])
        if(p_cons != p_os):
            return i,p_os,p_cons

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
    
    
