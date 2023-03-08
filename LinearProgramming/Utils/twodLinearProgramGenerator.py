from LinearProgramming.Classes.ObjectiveFunction import ObjectiveFunction
from LinearProgramming.Classes.Constraints import Constraints, GreaterOrLess
from LinearProgramming.Classes.Point import Point

import random
from typing import List, Tuple
import os

LINEAR_POROGRAMS_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'LinearPrograms'))


def generate_random_2d_feasible_linear_program(num_of_constraints:int,  max_value:int=100)->Tuple[ObjectiveFunction,List[Constraints]]:
    p1 = Point(random.randint(0,max_value),random.randint(0,max_value))
    p2 = Point(random.randint(0,max_value),random.randint(0,max_value))
    p3 = Point(random.randint(0,max_value),random.randint(0,max_value))
    # 3 points generate a plane
    cons = []
    
    while len(cons) < num_of_constraints:
        c = Constraints(a = random.randint(1,max_value),b = random.randint(1,max_value),lessOrGreater=GreaterOrLess.LESS,c=random.randint(10*max_value,10*max_value*max_value));
        
        if(c.contains(p1) or c.contains(p2) or c.contains(p3)):
            cons.append(c)
        else:
            c.flip_sign()
            if (c.contains(p1) or c.contains(p2) or c.contains(p3)):
                cons.append(c)
            else:
                print("unlucky, you will missing a constraint, but this happens rarely, so it is ok")
                # raise RuntimeError("this should not happen, check code");
                
    return (ObjectiveFunction(a = random.randint(1,max_value),b = random.randint(1,max_value)),cons)

def generate_to_file(num_of_constraints:int,  max_value:int=100, file_name:str="") -> str:
    obj,cons = generate_random_2d_feasible_linear_program(num_of_constraints, max_value)
    files = [f for f in os.listdir(LINEAR_POROGRAMS_DIR) if f.startswith("bounded_problem")]
    if file_name == "":
        file_name = "bounded_problem"+str(int(files.pop().replace("bounded_problem",""))+1)
    file_path = os.path.join(LINEAR_POROGRAMS_DIR,file_name)
    file = open(file_path, 'w')
    file.write(str(obj))
    [file.write(str(c)) for c in cons]
    file.close()
    return file_path


