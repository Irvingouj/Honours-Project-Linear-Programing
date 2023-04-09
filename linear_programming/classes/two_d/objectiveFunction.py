import re

from linear_programming.utils.types import MaxOrMin
from .point import Point
from ..vector import Vector




class ObjectiveFunction:
    # ax + by
    def __init__(self, a, b, maxOrMin=MaxOrMin.MAX):
        if (maxOrMin == MaxOrMin.MAX):
            self.a = a
            self.b = b
        else:
            self.a = -a
            self.b = -b
        self.maxOrMin = MaxOrMin.MAX

    def value(self, point: Point) -> float:
        return self.a * point.x + self.b * point.y

    @classmethod
    def from_string(cls, string: str) -> 'ObjectiveFunction':
        pattern = re.compile(
            r'(max|min)\s?[+-]?([0-9]*[.])?[0-9]+x\s?\+\s?[+-]?([0-9]*[.])?[0-9]+y\s?')
        if pattern.match(string) is None:
            raise ValueError('Invalid string : ' + string)
        maxOrMin = MaxOrMin.MAX if string.find('max') != -1 else MaxOrMin.MIN
        a_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+x',
                          string).group(0).split('x')[0]
        b_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+y',
                          string).group(0).split('y')[0]
        a = float(a_str)
        b = float(b_str)
        return cls(a, b, maxOrMin)

    def get_direction_for_x_axis(self) -> bool:
        return self.a / self.b > 0

    def __str__(self) -> str:
        return ('max' if self.maxOrMin == MaxOrMin.MAX else 'min') + ' ' + str(self.a) + 'x + ' + str(self.b) + 'y'

    def to_or_string(self) -> str:
        return str(self.a) + '*x + ' + str(self.b) + '*y'

    def to_vector(self) -> 'Vector':
        return Vector([self.a, self.b])
