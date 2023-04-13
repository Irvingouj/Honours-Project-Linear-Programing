debug_mode_global = True
debug_mode = True   
def if_debug(func):
    def wrapper(*args, **kwargs):
        global debug_mode_global
        if debug_mode_global:
            return func(*args, **kwargs)
        return None
    return wrapper

# def toggle(on:bool):
#     print("toggle")
#     def wrapper(func):
#         print("wrapper")
#         def inner(*args, **kwargs):
#             print("inner,befor execute")
#             global debug_mode
#             temp = debug_mode
#             debug_mode = on
#             result = func(*args, **kwargs)
#             debug_mode = temp
#             print("inner,after execute")
#             return result
#         return inner
#     return wrapper

# def start():
#     global debug_mode
#     debug_mode = True

# def end():
#     global debug_mode
#     debug_mode = False
    
@if_debug
def print_vecs(vecs,title=""):
    if title != "":
        print(title)
    for v in vecs:
        print(v)
    
@if_debug
def print_cons_float(cons,title=""):
    if title != "":
        print(title)
    for c in cons:
        print(c.str_float())

@if_debug
def print_cons(cons,title=""):
    if title != "":
        print(title)
    for c in cons:
        print(c)
        
@if_debug
def print_deg(any):
    print(any)

@if_debug
def message(*args):
    #if is array, print each element
    for arg in args:
        res = ""
        if isinstance(arg, list):
            res = " ".join([str(x)+"\n" for x in arg])
        else:
            res = str(arg)
        print(res)

@if_debug
def print_for_geo_gebra(cons):
    for c in cons:
        print(str(c).replace("<","").replace(">",""))

@if_debug
def os_solve_3d(obj,cons):
    from linear_programming.solvers.or_tool_solver import OsToolSolver
    return OsToolSolver().solve_three_d(obj, cons)
    
    
import numpy as np
from pyparsing import List
from linear_programming.classes.three_d import Constraints3D
@if_debug
def assert_pairwise_angle_the_same(old_cons:List[Constraints3D],new_cons:List[Constraints3D]):
    for i in range(len(old_cons)):
        for j in range(len(old_cons)):
            old_i = old_cons[i]
            old_j = old_cons[j]
            new_i = new_cons[i]
            new_j = new_cons[j]
            assert np.isclose(old_i.angle_to(old_j),new_i.angle_to(new_j)) 

            
            
@if_debug
def assertTrue(boolean, message=""):
    assert boolean , message
    
@if_debug
def assertEqualORTool(obj,cons,v,message=""):
    res = os_solve_3d(obj, cons)
    if res != v:
        print("con result")
        print(v)
        print("expected result")
        print(res)
        print("--------------------")
        print(obj)
        for c in cons:
            print(c)
    assert res == v, message
    return True