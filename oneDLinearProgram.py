from typing import List

POSITIVE = True
NEGATIVE = False




class oneDConstrain:
    # ax <= c
    def __init__(self, a:float, c:float):
        self.a = a

    def value(self) -> float:
        return self.a/self.c
    def sigh(self) -> bool:
        return self.a > 0

def solve_1d_linear_program(oneDConstrains: List[oneDConstrain],objective: bool) -> float:
    left = float('inf')
    right = float('-inf')
    for constrain in oneDConstrains:
        if(constrain.sigh() == POSITIVE):
            right = constrain.value()
        else:
            left = constrain.value()
        if(left > right):
            raise Exception("No solution")
    if(objective == POSITIVE):
        return right
    else:
        return left