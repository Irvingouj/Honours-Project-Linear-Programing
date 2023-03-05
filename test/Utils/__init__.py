from LinearProgramming.Classes.ObjectiveFunction import ObjectiveFunction
from LinearProgramming.Classes.Constraints import Constraints, GreaterOrLess
from LinearProgramming.Classes.Point import Point

import random
from typing import List, Tuple


def generate_random_2d_feasible_linear_program(num_of_constraints:int,  max_value:int=100)->Tuple[ObjectiveFunction,List[Constraints]]:
    p1 = Point(random.randint(0,max_value),random.randint(0,max_value))
    p2 = Point(random.randint(0,max_value),random.randint(0,max_value))
    p3 = Point(random.randint(0,max_value),random.randint(0,max_value))
    # 3 points generate a plane
    cons = []
    
    for i in len(num_of_constraints):
        c = Constraints(a = random.randint(max_value,max_value*max_value),b = random.randint(max_value,max_value*max_value),lessOrGreater=GreaterOrLess.LESS,c=0);
        
        if(c.contains(p1) and c.contains(p2) and c.contains(p3)):
            cons.append(c)
        else:
            c.flip_sign()
            if (c.contains(p1) and c.contains(p2) and c.contains(p3)):
                cons.append(c)
    return (ObjectiveFunction(a = random.randint(max_value,max_value*max_value),b = random.randint(max_value,max_value*max_value)),cons)