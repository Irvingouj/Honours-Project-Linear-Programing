from typing import Tuple, List
from linear_programming.classes import ObjectiveFunction, Constraints
from linear_programming.classes.three_d import Constraints3D, ObjectiveFunction3D

Program = Tuple[ObjectiveFunction, List[Constraints]]
Program3d = Tuple[ObjectiveFunction3D, List[Constraints3D]]
