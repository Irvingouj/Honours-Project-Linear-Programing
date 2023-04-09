from enum import Enum
from typing import Tuple, List

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

