from enum import Enum
from typing import Tuple, List

from linear_programming.classes.two_d.constraints import Constraints

Program = Tuple['ObjectiveFunction', List['Constraints']]
Program3d = Tuple['ObjectiveFunction3D', List['Constraints3D']]

class MaxOrMin(Enum):
    MAX = 0
    MIN = 1

class Facing(Enum):
    LEFT = True
    RIGHT = False

class GreaterOrLess(Enum):
    GREATER = 0
    LESS = 1
    
class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class CheckBoundResult2D:
    def __init__(self, bounded: bool, unbound_certificate: Constraints = None, unbounded_index=-1, bound_certificate: Tuple(int, int) = None):
        assert isinstance(bounded, bool)
        assert isinstance(unbound_certificate,
                          Constraints) or unbound_certificate == None
        assert isinstance(bound_certificate,
                          tuple) or bound_certificate == None

        # if bounded, the bound
        self.bounded = bounded
        self.unbound_certificate = unbound_certificate
        self.unbounded_index = unbounded_index
        self.bound_certificate = bound_certificate

        # only one of them can be None, and at least one of them must be None, XOR
        assert (bound_certificate == None) != (unbound_certificate == None)

    def __str__(self):
        if self.bounded:
            return f"bounded, bound certificate: {self.bound_certificate}"
        else:
            return f"unbounded, unbound certificate: {self.unbound_certificate}"