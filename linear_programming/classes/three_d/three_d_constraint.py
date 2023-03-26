import re
import numpy as np

from linear_programming.classes.constraints import GreaterOrLess

from linear_programming.classes.three_d.plane import Plane
from linear_programming.classes.three_d.point3d import Point3D


class Constraints3D:
    def __init__(self, a: float, b: float, c: float, lessOrGreater: GreaterOrLess = GreaterOrLess.LESS, d: float = 0) -> None:
        if a == 0 and b == 0 and c == 0:
            raise ValueError('Cannot create constraint with a=0, b=0 and c=0')
        if lessOrGreater == GreaterOrLess.LESS:
            self.a = a
            self.b = b
            self.c = c
            self.d = d
        else:
            self.a = -a
            self.b = -b
            self.c = -c
            self.d = -d

    @classmethod
    def from_string(cls, string: str) -> 'Constraints3D':
        pattern = re.compile(
            r'\s?[+-]?([0-9]*[.])?[0-9]+x\s?\+\s?[+-]?([0-9]*[.])?[0-9]+y\s?\+\s?[+-]?([0-9]*[.])?[0-9]+z\s?(<=|>=)\s?[+-]?([0-9]*[.])?[0-9]+')
        if pattern.match(string) is None:
            raise ValueError('Invalid string : ' + string +
                             ' does not match pattern')
        a_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+x',
                          string).group(0).split('x')[0]
        b_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+y',
                          string).group(0).split('y')[0]
        c_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+z',
                          string).group(0).split('z')[0]
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)
        lessOrGreater = GreaterOrLess.GREATER if string.find(
            '>=') != -1 else GreaterOrLess.LESS
        d = float(string.split('=')[1])
        return cls(a, b, c, lessOrGreater, d)

    def to_plane(self) -> Plane:
        return Plane(self.a, self.b, self.c, self.d)

    def contains(self, point) -> bool:
        # computer arithmetic is not precise enough
        return self.a * point.x + self.b * point.y + self.c * point.z < self.d or np.isclose(self.a * point.x + self.b * point.y + self.c * point.z, self.d)

    def find_intersection(self, other: 'Constraints3D') -> Point3D:
        return self.to_plane().find_intersection(other.to_plane())

    @classmethod
    def from_plane(cls, plane: Plane) -> 'Constraints3D':
        return cls(plane.a, plane.b, plane.c, d=plane.d)
