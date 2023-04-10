import numpy as np
from .point import Point
from ..vector import Vector


class Line:
    # ax + by = c
    # pylint: disable=C0103
    def __init__(self, a: float, b: float, c: float):
        if c < 0:
            self.a = -a
            self.b = -b
            self.c = -c
        else:
            self.a = a
            self.b = b
            self.c = c

    def is_on_line(self, point: Point) -> bool:
        return self.a * point.x + self.b * point.y == self.c

    @staticmethod
    def from_point(p1:Point,p2:Point):
        a = p2.y - p1.y
        b = p1.x - p2.x
        c = p2.x*p1.y - p1.x*p2.y
        return Line(a,b,c)

    def find_intersection(self, line: 'Line') -> Point:
        a_1 = self.a
        b_1 = self.b
        c_1 = self.c
        a_2 = line.a
        b_2 = line.b
        c_2 = line.c
        # check if lines are parallel
        if a_1*b_2 == a_2*b_1:
            return None

        y = (a_2*c_1 - a_1*c_2)/(a_2*b_1 - a_1*b_2)
        x = (c_1 - b_1*y)/a_1 if a_1 != 0 else (c_2 - b_2*y)/a_2
        return Point(x, y)

    def to_vector(self) -> Vector:
        return Vector([-self.b, self.a])

    def is_parallel(self, other: 'Line') -> bool:
        return np.isclose(self.a * other.b, self.b * other.a)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Line):
            return self.a == __o.a and self.b == __o.b and self.c == __o.c
        raise TypeError('Cannot compare Line with ' + str(type(__o)))

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __str__(self) -> str:
        return str(self.a) + 'x + ' + str(self.b) + 'y = ' + str(self.c)

    def perpendicular_vector(self) -> Vector:
        
        return Vector([-self.a, -self.b])
