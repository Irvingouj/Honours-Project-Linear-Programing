from typing import List
from Classes.OneDConstraint import OneDConstraint

POSITIVE = True
NEGATIVE = False


def solve_1d_linear_program(oneDConstraints: List[OneDConstraint],objective: bool) -> float:
    left = float('-inf')
    right = float('inf')
    for constrain in oneDConstraints:
        if(constrain.direction() == POSITIVE):
            #facing left
            right = constrain.value()
        else:
            left = constrain.value()
        if(left > right):
            raise Exception("No solution")
    if(objective == POSITIVE):
        return right
    else:
        return left