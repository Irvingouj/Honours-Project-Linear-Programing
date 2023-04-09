from enum import Enum
import re
import numpy as np

from linear_programming.utils.types import Direction, GreaterOrLess

from .edge import Edge
from .line import Line
from .point import Point
from ..vector import Vector



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

    def is_a_num(self, num) -> bool:
        if num is None or np.isnan(num) or np.isinf(num):
            return False
        return isinstance(num, int) or isinstance(num, float)
    
    def contains(self, point) -> bool:
        assert self.is_a_num(self.a), "a is not a number"
        assert self.is_a_num(self.b), "b is not a number"
        assert self.is_a_num(point.x), "x is not a number"
        assert self.is_a_num(point.y), "y is not a number"
        
        result = self.a * point.x + self.b * point.y
        # Check for NaN or infinity values
        if np.isnan(result) or np.isinf(result):
            return False

        return result < self.c or np.isclose(result, self.c)

    def find_intersection(self, edge: 'Constraints') -> Point:
        if self.is_parallel(edge):
            return None
        return self.to_edge().find_intersection(edge.to_edge())

    @classmethod
    def from_edge(cls, edge: Edge) -> 'Constraints':
        return cls(edge.line.a, edge.line.b, edge.line.c)

    def find_point_with_x(self, x: float) -> Point:
        return Point(x, (self.c - self.a * x) / self.b)

    def find_point_with_y(self, y: float) -> Point:
        return Point((self.c - self.b * y) / self.a, y)

    def is_vertical(self) -> bool:
        return np.isclose(self.a, 0)

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
        return np.isclose(self.a * other.b, self.b * other.a)
        # return self.a * other.b == self.b * other.a

    def facing_direction_vector(self) -> 'Vector':
        return Vector([-self.a, -self.b])

    def is_parallel_and_contains_each_other(self, other: 'Constraints') -> bool:
        return self.is_parallel(other) and self.facing_direction_vector() == other.facing_direction_vector()

    def is_parallel_but_facing_different_direction(self, other: 'Constraints') -> bool:
        return self.is_parallel(other) and self.facing_direction_vector() != other.facing_direction_vector()

    #bad name, refractor later :TODO
    def flip_sign(self) -> 'Constraints':
        return Constraints(-self.a, -self.b, c=-self.c)
    
    def get_flip_sign(self) -> 'Constraints':
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
        return Vector([-self.a, -self.b]).normalize()
    
    def get_rotate_around_origin(self, angle: float) -> 'Constraints':
        new_facing_vector = self.facing_direction_vector().get_rotate(angle)
        return Constraints(-new_facing_vector.get(0), -new_facing_vector.get(1), c=self.c)


    def get_moved(self,direction:Direction, distance:float) -> 'Constraints':
        if direction == Direction.LEFT:
            return Constraints(self.a, self.b, c=self.c - distance)
        elif direction == Direction.RIGHT:
            return Constraints(self.a, self.b, c=self.c + distance)
        elif direction == Direction.UP:
            return Constraints(self.a, self.b, c=self.c + distance)
        elif direction == Direction.DOWN:
            return Constraints(self.a, self.b, c=self.c - distance)
        
    def move(self,direction:Direction, distance:float):
        if direction == Direction.LEFT:
            self.c -= distance
        elif direction == Direction.RIGHT:
            self.c += distance
        elif direction == Direction.UP:
            self.c += distance
        elif direction == Direction.DOWN:
            self.c -= distance
            
    def rotate_around_origin(self, angle: float):
        new_facing_vector = self.facing_direction_vector().get_rotate(angle)
        self.a = -new_facing_vector.get(0)
        self.b = -new_facing_vector.get(1)

    def str_float(self) -> str:
        return f'{self.a:.2f}x + {self.b:.2f}y   <= {self.c:.2f}'

    @staticmethod
    def from_line_and_vector(line: Line, vector: Vector) -> 'Constraints':
        """
        return the constraint that has line as boundary and facing the direction of vector
        
        """        
        # assert np.isclose(line.to_vector()*vector, 0), "line and vector are not perpendicular"
        res = Constraints(line.a, line.b,lessOrGreater=GreaterOrLess.LESS, c=line.c)
        random_point = res.find_point_with_x(0)
        point_off_set_vec = random_point + Point(vector.get(0), vector.get(1))
        if not res.contains(point_off_set_vec):
            return res.flip_sign()
        return res