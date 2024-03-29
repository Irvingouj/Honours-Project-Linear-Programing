import random
from typing import List, Tuple

from linear_programming.classes.two_d import Constraints, GreaterOrLess, ObjectiveFunction, Point
from linear_programming.classes.one_d.one_d_constraint import OneDConstraint
from linear_programming.classes.vector import Vector
from linear_programming.utils.types import Program, Program3d
from linear_programming.utils.problem_reader import PROJECT_ROOT
from linear_programming.classes.three_d import Constraints3D, ObjectiveFunction3D, Point3D

LINEAR_PROGRAMS_DIR = PROJECT_ROOT.joinpath("linear_program_data")

def rand_float_in_range(min: int, max: int) -> int:
    res =  random.uniform(min, max)
    while res == 0:
        res =  random.randint(min, max)
    # expecting for higher precision, blocked by floating point error on the solver
    res = round(res, 2)
    return res
def random_constraint(max_value: int = 100) -> Constraints:
    a = rand_float_in_range(-max_value, max_value)
    while(a == 0):
        a = rand_float_in_range(-max_value, max_value)
    b = rand_float_in_range(-max_value, max_value)
    while(b == 0):
        b = rand_float_in_range(-max_value, max_value)
        
    c = rand_float_in_range(10*max_value, 10*max_value*max_value)
    
    return Constraints(a=a, b=b, lessOrGreater=GreaterOrLess.LESS, c=c)

def random_obj() -> ObjectiveFunction:
    a = rand_float_in_range(-10, 10)
    b = rand_float_in_range(-10, 10)
    while a == 0 and b == 0:
        a = rand_float_in_range(-10, 10)
        b = rand_float_in_range(-10, 10)
    return ObjectiveFunction(a=a, b=b)

def random_point(start: int = -100,end:int = -100) -> Point:
    x = rand_float_in_range(start, end)
    y = rand_float_in_range(start, end)
    return Point(x, y)

def gen_random_2d_feasible(num_constrains: int,  max_value: int = 10) -> Program:
    p_1 = random_point(-max_value, max_value)
    p_2 = random_point(-max_value, max_value)
    p_3 = random_point(-max_value, max_value)
    # 3 points generate a plane
    cons = []

    def if_feasible_constraint(c: Constraints) -> bool:
        return c.contains(p_1) and c.contains(p_2) and c.contains(p_3)

    while len(cons) < num_constrains:
        c = random_constraint(max_value)

        if if_feasible_constraint(c):
            cons.append(c)
        elif if_feasible_constraint(c.flip_sign()):
            cons.append(c.flip_sign())
        
    
    
    return (random_obj(), cons)

OneDProgram = Tuple[bool, List[OneDConstraint]]



def gen_random_1d_feasible(num_constrains: int,  max_value: int = 100) -> OneDProgram:
    p_1 = rand_float_in_range(-max_value, max_value)
    
    cons = []
    while len(cons) < num_constrains:
        a = random.randint(-max_value, max_value) 
        if a == 0:
            continue
        con = OneDConstraint(a, random.randint(10*max_value, 10*max_value*max_value))
        if not con.contains(p_1):
            continue
        cons.append(con)
        
    return (True, cons)
        
def gen_random_2d_infeasible(num_constrains: int,  max_value: int = 10) -> Program:
    p_1 = Point(rand_float_in_range(-max_value,max_value), rand_float_in_range(-max_value,max_value))
    cons = []

    def if_infeasible_constraint(c: Constraints) -> bool:
        return not c.contains(p_1)

    while len(cons) < num_constrains:
        
        c = random_constraint(max_value)
        if if_infeasible_constraint(c):
            cons.append(c)
        elif if_infeasible_constraint(c.flip_sign()):
            cons.append(c.flip_sign())

    return (random_obj(), cons)

def gen_random_2d_unbounded(num_constrains:int, max_value:int = 10) -> Program:
    # start_point = Point(random.randint(-max_value, max_value), random.randint(-max_value, max_value))
    direction_vector = Vector([random.uniform(-max_value, max_value), random.uniform(-max_value, max_value)])
    #if a constrain intersects with a ray, and it is facing the direction of the ray, then thats fine
    #if a constrain intersects with a ray, and it is facing the opposite direction of the ray, then we need to flip the sign of the constraint
    res = []
    while len(res) < num_constrains:
        c = random_constraint(max_value)
        if c.facing_direction_vector()*direction_vector > 0:
            res.append(c)
        elif c.facing_direction_vector()*direction_vector < 0:
            res.append(c.get_flip_sign())


    obj = random_obj()
    while obj.to_vector()*direction_vector < 0:
        obj = random_obj()
        

    return (obj, res)

def random_constraint_3d(max_value: int = 100) -> Constraints3D:
    a = rand_float_in_range(-max_value, max_value)
    
    b = rand_float_in_range(-max_value, max_value)
    
    c = rand_float_in_range(-max_value, max_value)
    
    d = rand_float_in_range(10*max_value, 10*max_value*max_value)
    
    return Constraints3D(a=a, b=b, c=c, lessOrGreater=GreaterOrLess.LESS, d=d)
    
def random_obj_3d() -> ObjectiveFunction3D:
    a = rand_float_in_range(-10, 10)
    b = rand_float_in_range(-10, 10)
    c = rand_float_in_range(-10, 10)
    while a == 0 or b == 0 or c == 0:
        a = rand_float_in_range(-10, 10)
        b = rand_float_in_range(-10, 10)
        c = rand_float_in_range(-10, 10)
    return ObjectiveFunction3D(a=a, b=b, c=c)

def gen_random_3d_unbounded(num_constrains:int, max_value:int = 10) -> Program3d:
    direction_vector = Vector([random.uniform(-max_value, max_value), random.uniform(-max_value, max_value), random.uniform(-max_value, max_value)])
    res = []
    while len(res) < num_constrains:
        c = random_constraint_3d(max_value)
        if c.facing_direction_vector()*direction_vector > 0:
            res.append(c)
        elif c.facing_direction_vector()*direction_vector < 0:
            res.append(c.get_flip_sign())

    obj = random_obj_3d()
    while obj.to_vector()*direction_vector < 0:
        obj = random_obj_3d()
        

    return (obj, res)

def gen_random_3d_feasible(num_constrains:int, max_value:int = 10) -> Program3d:
    """
    generate a 3d program with bounded solution with high probability
    """
    p_1 = Point3D(rand_float_in_range(-max_value, max_value), rand_float_in_range(-max_value, max_value), rand_float_in_range(-max_value, max_value))
    p_2 = Point3D(rand_float_in_range(-max_value, max_value), rand_float_in_range(-max_value, max_value), rand_float_in_range(-max_value, max_value))
    p_3 = Point3D(rand_float_in_range(-max_value, max_value), rand_float_in_range(-max_value, max_value), rand_float_in_range(-max_value, max_value))
    p_4 = Point3D(rand_float_in_range(-max_value, max_value), rand_float_in_range(-max_value, max_value), rand_float_in_range(-max_value, max_value))
    cons = []

    def if_feasible_constraint(c: Constraints3D) -> bool:
        return c.contains(p_1) and c.contains(p_2) and c.contains(p_3) and c.contains(p_4)

    while len(cons) < num_constrains:
        c = random_constraint_3d(max_value)

        if if_feasible_constraint(c):
            cons.append(c)
        elif if_feasible_constraint(c.flip_sign()):
            cons.append(c.flip_sign())

    return (random_obj_3d(), cons)

def gen_random_3d_infeasible(num_constrains: int,  max_value: int = 10) -> Program3d:
    p_1 = Point3D(rand_float_in_range(-max_value,max_value), rand_float_in_range(-max_value,max_value), rand_float_in_range(-max_value,max_value))
    cons = []

    def if_infeasible_constraint(c: Constraints3D) -> bool:
        return not c.contains(p_1)

    while len(cons) < num_constrains:
        
        c = random_constraint_3d(max_value)
        if if_infeasible_constraint(c):
            cons.append(c)
        elif if_infeasible_constraint(c.flip_sign()):
            cons.append(c.flip_sign())

    return (random_obj_3d(), cons)


def gen_random_2d(n):
    res = []
    while len(res) < n:
        res.append(random_constraint())
    return (random_obj(), res)

def gen_random_3d(n):
    res = []
    while len(res) < n:
        res.append(random_constraint_3d())
    return (random_obj_3d(), res)