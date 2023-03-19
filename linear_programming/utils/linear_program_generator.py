import random
from typing import List, Tuple
import os

from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.classes.constraints import Constraints, GreaterOrLess
from linear_programming.classes.point import Point
from linear_programming.classes.oneDConstraint import OneDConstraint
from linear_programming.classes.vector import Vector
from .problem_reader import project_root, Program,bounded_prefix,infeasible_prefix


LINEAR_PROGRAMS_DIR = project_root.joinpath("linear_program_data")

def rand_float_in_range(min: int, max: int) -> int:
    res =  random.uniform(min, max)
    while res == 0:
        res =  random.randint(min, max)
    res = round(res, 4)
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

def gen_random_2d_feasible(num_constrains: int,  max_value: int = 10) -> Program:
    p_1 = Point(random.randint(0, max_value), random.randint(0, max_value))
    p_2 = Point(random.randint(0, max_value), random.randint(0, max_value))
    p_3 = Point(random.randint(0, max_value), random.randint(0, max_value))
    # 3 points generate a plane
    cons = []

    def if_feasible_constraint(c: Constraints) -> bool:
        return c.contains(p_1) or c.contains(p_2) or c.contains(p_3)

    while len(cons) < num_constrains:
        a = rand_float_in_range(-max_value, max_value)
        b = rand_float_in_range(-max_value, max_value)
        
        c = Constraints(a=a, b=b,
                        lessOrGreater=GreaterOrLess.LESS, c=random.randint(10*max_value, 10*max_value*max_value))

        if if_feasible_constraint(c):
            cons.append(c)
        elif if_feasible_constraint(c.flip_sign()):
            cons.append(c.flip_sign())

    return (ObjectiveFunction(a=random.randint(1, max_value), b=random.randint(1, max_value)), cons)

OneDProgram = Tuple[bool, List[OneDConstraint]]



def gen_random_1d_feasible(num_constrains: int,  max_value: int = 100) -> OneDProgram:
    p_1 = random.randint(-max_value, max_value)
    
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
    p_1 = Point(random.randint(0, max_value), random.randint(0, max_value))
    # 3 points generate a plane
    cons = []

    def if_infeasible_constraint(c: Constraints) -> bool:
        return not c.contains(p_1)

    while len(cons) < num_constrains:
        a = rand_float_in_range(-max_value, max_value)
        b = rand_float_in_range(-max_value, max_value)
        
        c = Constraints(a=a, b=b,
                        lessOrGreater=GreaterOrLess.LESS, c=random.randint(10*max_value, 10*max_value*max_value))

        if if_infeasible_constraint(c):
            cons.append(c)
        elif if_infeasible_constraint(c.flip_sign()):
            cons.append(c.flip_sign())

    return (ObjectiveFunction(a=random.randint(1, max_value), b=random.randint(1, max_value)), cons)

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
    
def save_to_file(file_type:str,obj:ObjectiveFunction,constraints:List[Constraints])->str:
    assert file_type in ["bounded", "unbounded", "infeasible"]
    file_prefix = f"{file_type}_problem"
    
    files = [f for f in os.listdir(
        LINEAR_PROGRAMS_DIR) if f.startswith(file_prefix)]
    
    file_name = f"{file_prefix}{len(files)+1}"
    file_path = os.path.join(LINEAR_PROGRAMS_DIR, file_name)
    file = open(file_path, 'w', encoding='utf-8')
    file.write(f"# type = {file_type} problem generated randomly,n = {len(constraints)}\n")
    file.write(str(obj))
    for con in constraints:
        file.write("\n")
        file.write(str(con))
    file.close()
    return file_path   
    
    

def generate_to_file_bounded(num_of_constraints: int,  max_value: int = 100) -> str:
    obj, cons = gen_random_2d_feasible(
        num_of_constraints, max_value)
    files = [f for f in os.listdir(
        LINEAR_PROGRAMS_DIR) if f.startswith(bounded_prefix)]
    
    print(files)
    file_name = f"{bounded_prefix}{len(files)+1}"
            
    file_path = os.path.join(LINEAR_PROGRAMS_DIR, file_name)
    file = open(file_path, 'w', encoding='utf-8')
    file.write(f"# problem generated randomly,n = {num_of_constraints}\n")
    file.write(str(obj))
    for con in cons:
        file.write("\n")
        file.write(str(con))
    file.close()
    return file_path

def generate_to_file_infeasible(num_of_constraints: int,  max_value: int = 100) -> str:
    obj, cons = gen_random_2d_infeasible(
        num_of_constraints, max_value)
    files = [f for f in os.listdir(
        LINEAR_PROGRAMS_DIR) if f.startswith(infeasible_prefix)]
    
    print(files)
    file_name = f"{infeasible_prefix}{len(files)+1}"
            
    file_path = os.path.join(LINEAR_PROGRAMS_DIR, file_name)
    file = open(file_path, 'w', encoding='utf-8')
    file.write(f"# problem generated randomly,n = {num_of_constraints}\n")
    file.write(str(obj))
    for con in cons:
        file.write("\n")
        file.write(str(con))
    file.close()
    return file_path
