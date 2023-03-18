
from linear_programming.classes import constraints
from linear_programming.classes.convexSolver import ConvexSolver
from linear_programming.classes.osToolSolver import OsToolSolver
from linear_programming.utils.exceptions import NoSolutionException


def con_solve(obj,cons):
    try:
        p_cons = ConvexSolver().solve(obj, cons)
    except NoSolutionException:
        return None
    return p_cons

def os_solve(obj,cons):
    p_os = OsToolSolver().solve(obj, cons)
    return p_os


def re_arrange_cons(obj,cons) -> constraints.Constraints:
    """
    this method grabs the first bad constraint and moves it to the top of the list
    """
    assert len(cons) > 4
    for i in range(4,len(cons)+1):
        p_os = os_solve(obj, cons[:i])
        p_cons = con_solve(obj, cons[:i])
        if(p_cons != p_os):
            poped = cons.pop(i-1)
            cons.insert(0,poped)
            return poped
    return None
    
    
