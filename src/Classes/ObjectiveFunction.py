from enum import Enum
import re

from Classes.Point import Point

class MaxOrMin(Enum):
    MAX = 0
    MIN = 1

class ObjectiveFunction:
    #ax + by
    def __init__(self, a, b, maxOrMin = MaxOrMin.MAX):
        self.a = a
        self.b = b
        self.maxOrMin = maxOrMin

    def value(self, point:Point) -> float:
        return self.a * point.x + self.b * point.y

    @classmethod
    def from_string(cls, string:str) -> 'ObjectiveFunction':
        pattern = re.compile(r'(max|min)\s?[+-]?([0-9]*[.])?[0-9]+x\s?\+\s?[+-]?([0-9]*[.])?[0-9]+y\s?')
        if pattern.match(string) is None:
            raise ValueError('Invalid string : ' + string)
        maxOrMin = MaxOrMin.MAX if string.split(' ')[0].strip() == 'max' else MaxOrMin.MIN
        a_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+x', string).group(0).split('x')[0]
        b_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+y', string).group(0).split('y')[0]
        a = float(a_str)
        b = float(b_str)
        return cls(a,b,maxOrMin)