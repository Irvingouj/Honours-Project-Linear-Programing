from typing import List
from enum import Enum
import re
from .edge import Edge
from .line import Line
from .point import Point
from .vector import Vector


class GreaterOrLess(Enum):
    GREATER = 0
    LESS = 1


class Constraints:
    # always less than
    def __init__(self, a: float, b: float, lessOrGreater: GreaterOrLess = GreaterOrLess.LESS, c: float = 0) -> None:
        if a == 0 and b == 0:
            raise ValueError('Cannot create constraint with a=0 and b=0')
        if lessOrGreater == GreaterOrLess.LESS:
            self.a = a
            self.b = b
            self.c = c
        else:
            self.a = -a
            self.b = -b
            self.c = -c

    @classmethod
    def from_string(cls, string: str) -> 'Constraints':
        pattern = re.compile(
            r'\s?[+-]?([0-9]*[.])?[0-9]+x\s?\+\s?[+-]?([0-9]*[.])?[0-9]+y\s?(<=|>=)\s?[+-]?([0-9]*[.])?[0-9]+')
        if pattern.match(string) is None:
            raise ValueError('Invalid string : ' + string +
                             ' does not match pattern')
        a_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+x',
                          string).group(0).split('x')[0]
        b_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+y',
                          string).group(0).split('y')[0]
        a = float(a_str)
        b = float(b_str)
        lessOrGreater = GreaterOrLess.GREATER if string.find(
            '>=') != -1 else GreaterOrLess.LESS
        c = float(string.split('=')[1])
        return cls(a, b, lessOrGreater, c)

    def to_edge(self) -> Edge:
        return Edge(line=Line(self.a, self.b, self.c))

    def contains(self, point) -> bool:
        return self.a * point.x + self.b * point.y <= self.c

    def find_all_intersection_with_Constraints(self, cons: List['Constraints']) -> List[Point]:
        points = []
        for con in cons:
            point = self.find_intersection(con)
            if point is not None:
                points.append(point)
        return points

    def find_intersection(self, edge: 'Constraints') -> Point:
        return self.to_edge().find_intersection(edge.to_edge())

    @classmethod
    def from_edge(cls, edge: Edge) -> 'Constraints':
        return cls(edge.line.a, edge.line.b, edge.line.c)

    def find_point_with_x(self, x: float) -> Point:
        return Point(x, (self.c - self.a * x) / self.b)

    def find_point_with_y(self, y: float) -> Point:
        return Point((self.c - self.b * y) / self.a, y)

    def is_vertical(self) -> bool:
        return self.b == 0

    def rotate(self) -> 'Constraints':
        return Constraints(self.b, -self.a, c=self.c)

    def to_or_string(self) -> str:
        return str(self.a) + '*x + ' + str(self.b) + '*y <= ' + str(self.c)

    def to_line(self) -> Line:
        return Line(self.a, self.b, self.c)
    # returns 1 or -1 or 0 if facing up or down

    def facing_direction_on_x_axis(self, ) -> int:
        if self.a == 0:
            return 0
        if self.c > 0:
            return 1 if self.a > 0 else -1
        else:
            return -1 if self.a > 0 else 1

    def __str__(self) -> str:
        return str(self.a) + 'x + ' + str(self.b) + 'y <= ' + str(self.c)

    def is_parallel(self, other: 'Constraints') -> bool:
        if self.a == 0 and other.a == 0:
            return True
        if self.b == 0 and other.b == 0:
            return True
        return self.a * other.b == self.b * other.a

    def facing_direction_vector(self) -> 'Vector':
        return Vector([-self.a, -self.b])

    def is_parallel_and_contains_each_other(self, other: 'Constraints') -> bool:
        return self.is_parallel(other) and self.facing_direction_vector() == other.facing_direction_vector()

    def is_parallel_but_facing_different_direction(self, other: 'Constraints') -> bool:
        return self.is_parallel(other) and self.facing_direction_vector() != other.facing_direction_vector()

    def flip_sign(self) -> 'Constraints':
        return Constraints(-self.a, -self.b, c=-self.c)

    def is_parallel_but_share_no_common_area(self, other: 'Constraints') -> bool:
        if not self.is_parallel(other):
            return False

        p1 = None
        p2 = None
        if self.a == 0:  # horizontal line
            p1 = self.find_point_with_x(0)
            p2 = other.find_point_with_x(0)

        elif self.b == 0:  # vertical line
            p1 = self.find_point_with_y(0)
            p2 = other.find_point_with_y(0)

        else:
            p1 = self.find_point_with_x(0)
            p2 = other.find_point_with_x(0)

        return not (self.contains(p2) or other.contains(p1))

    def facing_normal_vector(self) -> 'Vector':
        return Vector([-self.b, self.a]).normalize()
    
    def get_rotate_around_origin(self, angle: float) -> 'Constraints':
        new_facing_vector = self.facing_direction_vector().get_rotate(angle)
        return Constraints(-new_facing_vector.get(0), -new_facing_vector.get(1), c=self.c)