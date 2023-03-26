import math
from typing import List

from linear_programming.classes.vector import Vector

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: 'Point3D') -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

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
