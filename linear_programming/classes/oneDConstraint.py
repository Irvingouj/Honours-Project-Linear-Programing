from .point import Point
from .constraints import Constraints


class OneDConstraint:
    # ax <= c
    def __init__(self, a,c):
        self.a = a
        self.c = c
    
    @classmethod
    def from_constraint(cls, constraint:Constraints,p:Point) -> 'OneDConstraint':
       return cls(constraint.a, constraint.c)
    
    # which side of the constraint is facing, left is true, right is false
    def direction(self) -> bool:
        return self.a > 0

    def value(self) -> float:
        return self.c/self.a
    
    def __str__(self):
        return str(self.a) + 'x <= ' + str(self.c)