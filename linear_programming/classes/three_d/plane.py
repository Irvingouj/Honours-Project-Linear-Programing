import math

from linear_programming.classes.vector import Vector
from linear_programming.classes.three_d.point3d import Point3D

class Plane:
    def __init__(self, a: float, b: float, c: float, d: float):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


    def find_intersection(self, other: 'Plane') -> Point3D:
        if self.is_parallel(other):
            return None
        elif self.is_perpendicular(other):
            x = (other.d - self.d) / self.a
            y = (other.d - self.d) / self.b
            z = (other.d - self.d) / self.c
            return Point3D(x, y, z)
        else:
            # solve system of linear equations
            a1 = self.a
            b1 = self.b
            c1 = self.c
            d1 = self.d
            a2 = other.a
            b2 = other.b
            c2 = other.c
            d2 = other.d
            x = (b1*c2*d2 - b2*c1*d1) / (a1*b2 - a2*b1)
            y = (a2*c1*d1 - a1*c2*d2) / (a1*b2 - a2*b1)
            z = (a1*b2*d2 - a2*b1*d1) / (a1*b2 - a2*b1)
            return Point3D(x, y, z)

    def is_parallel(self, other: 'Plane') -> bool:
        return Vector([self.a, self.b, self.c]).is_parallel_to(Vector([other.a, other.b, other.c]))

    def is_perpendicular(self, other: 'Plane') -> bool:
        return Vector([self.a, self.b, self.c]).is_perpendicular_to(Vector([self.a, self.b, self.c]))

    def distance_to_point(self, point: Point3D) -> float:
        return abs(self.a * point.x + self.b * point.y + self.c * point.z + self.d) / math.sqrt(self.a ** 2 + self.b ** 2 + self.c ** 2)

    def get_normal_vector(self) -> Vector:
        return Vector([self.a, self.b, self.c])

    def get_signed_distance_to_point(self, point: Point3D) -> float:
        return (self.a * point.x + self.b * point.y + self.c * point.z + self.d) / math.sqrt(self.a ** 2 + self.b ** 2 + self.c ** 2)
    
        

    def __str__(self) -> str:
        return f"{self.a}x + {self.b}y + {self.c}z + {self.d} = 0"
