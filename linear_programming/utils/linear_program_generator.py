import random
from typing import List, Tuple
import os

from linear_programming.classes.objectiveFunction import ObjectiveFunction
from linear_programming.classes.constraints import Constraints, GreaterOrLess
from linear_programming.classes.point import Point
from linear_programming.classes.oneDConstraint import OneDConstraint
from .problem_reader import project_root, Program,bounded_prefix


LINEAR_PROGRAMS_DIR = project_root.joinpath("linear_program_data")


def gen_random_2d_feasible(num_constrains: int,  max_value: int = 100) -> Program:
    p_1 = Point(random.randint(0, max_value), random.randint(0, max_value))
    p_2 = Point(random.randint(0, max_value), random.randint(0, max_value))
    p_3 = Point(random.randint(0, max_value), random.randint(0, max_value))
    # 3 points generate a plane
    cons = []

    def if_feasible_constraint(c: Constraints) -> bool:
        return c.contains(p_1) or c.contains(p_2) or c.contains(p_3)

    while len(cons) < num_constrains:
        c = Constraints(a=random.randint(-max_value, max_value), b=random.randint(-max_value, max_value),
                        lessOrGreater=GreaterOrLess.LESS, c=random.randint(10*max_value, 10*max_value*max_value))

        if if_feasible_constraint(c) or if_feasible_constraint(c.flip_sign()):
            cons.append(c)

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
        
    

def generate_to_file(num_of_constraints: int,  max_value: int = 100) -> str:
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
