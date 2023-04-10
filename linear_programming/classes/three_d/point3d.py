import math
from typing import List

import numpy as np
from ..vector import Vector

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: 'Point3D') -> bool:
        if not isinstance(other, Point3D):
            return False
        return np.allclose([self.x, self.y, self.z], [other.x, other.y, other.z])

    def __add__(self, other: 'Point3D') -> 'Point3D':
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Point3D') -> 'Vector':
        return Vector([self.x - other.x, self.y - other.y, self.z - other.z])

    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]

    def distance_to(self, other: 'Point3D') -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def midpoint(self, other: 'Point3D') -> 'Point3D':
        return Point3D((self.x + other.x) / 2, (self.y + other.y) / 2, (self.z + other.z) / 2)

    def is_in(self, constraints: 'Constraints3D') -> bool:
        return constraints.contains(self)