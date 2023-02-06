from typing import List
from Classes.Point import Point
from Classes.Edge import Edge
from Classes.Line import Line
from enum import Enum
import re

class GreaterOrLess(Enum):
    GREATER = 0
    LESS = 1

class Constraints:
    # always less than
    def __init__(self,a:float,b:float,lessOrGreater:GreaterOrLess = GreaterOrLess.LESS, c:float = 0) -> None:
        if lessOrGreater == GreaterOrLess.LESS:
            self.a = a
            self.b = b
            self.c = c
        else:
            self.a = -a
            self.b = -b
            self.c = -c

    @classmethod
    def from_string(cls, string:str) -> 'Constraints':
        pattern = re.compile(r'\s?[+-]?([0-9]*[.])?[0-9]+x\s?\+\s?[+-]?([0-9]*[.])?[0-9]+y\s?(<=|>=)\s?[+-]?([0-9]*[.])?[0-9]+')
        if  pattern.match(string) is None:
            raise ValueError('Invalid string : ' + string + ' does not match pattern')
        a_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+x', string).group(0).split('x')[0]
        b_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+y', string).group(0).split('y')[0]
        a = float(a_str)
        b = float(b_str)
        lessOrGreater = GreaterOrLess.GREATER if string.find('>=') != -1 else GreaterOrLess.LESS
        c = float(string.split('=')[1])
        return cls(a,b,lessOrGreater,c)

    def to_edge(self) -> Edge:
        return Edge(line=Line(self.a,self.b,self.c))

    def is_inside(self, point) -> bool:
        return self.a * point.x + self.b * point.y <= self.c
    
    def find_all_intersection_with_Constraints(self, cons:List['Constraints']) -> List[Point]:
        points = []
        for con in cons:
            point = self.find_intersection(con)
            if point is not None:
                points.append(point)
        return points
    
    def find_intersection(self, edge:'Constraints') -> Point:
        return self.to_edge().find_intersection(edge.to_edge())
    
    @classmethod
    def from_edge(cls, edge:Edge) -> 'Constraints':
        return cls(edge.line.a, edge.line.b, edge.line.c)

    def find_point_with_x(self, x:float) -> Point:
        return Point(x, (self.c - self.a * x) / self.b)

    def __str__(self) -> str:
        return str(self.a) + 'x + ' + str(self.b) + 'y <= ' + str(self.c)

