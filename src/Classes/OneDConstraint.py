from Classes.Constraints import Constraints

class OneDConstraint:
    # ax <= c
    def __init__(self, a,c):
        self.a = a
        self.c = c
    
    @classmethod
    def from_constraint(cls, constraint:Constraints) -> 'OneDConstraint':
        cls(constraint.a, constraint.c)
    
    def direction(self) -> bool:
        return self.a > 0