from linear_programming.classes.two_d import Point, Constraints

from linear_programming.utils.types import Facing



class OneDConstraint:
    # ax <= c
    def __init__(self, a, c):
        self.a = a
        self.c = c

    @classmethod
    def from_constraint(cls, constraint: Constraints, p: Point) -> 'OneDConstraint':
        return cls(constraint.a, constraint.c)

    # which side of the constraint is facing, left is true, right is false
    def direction(self) -> Facing:
        return Facing.LEFT if self.a > 0 else Facing.RIGHT


    def value(self) -> float:
        return self.c/self.a
    
    def contains(self, value:float) -> bool:
        return self.a*value <= self.c
   
    # def value_str(self) -> str:
    #     return f"x<= {self.value()}" 

    def __str__(self):
        return str(self.a) + '*x <= ' + str(self.c)
