from Classes.Edge import Edge
from Classes.Line import Line
from enum import Enum
import re

class GreaterOrLess(Enum):
    GREATER = 0
    LESS = 1

class Constrains:
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
    def from_string(cls, string:str) -> 'Constrains':
        pattern = re.compile(r'\s?[+-]?([0-9]*[.])?[0-9]+x\s?\+\s?[+-]?([0-9]*[.])?[0-9]+y\s?(<=|>=)\s?[+-]?([0-9]*[.])?[0-9]+')
        if pattern.match(string) is None:
            raise ValueError('Invalid string : ' + string + ' does not match pattern')
        a_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+x', string).group(0).split('x')[0]
        b_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+y', string).group(0).split('y')[0]
        a = float(a_str)
        b = float(b_str)
        lessOrGreater = GreaterOrLess.GREATER if string.split('y')[1].split('=')[0].strip() == '<=' else GreaterOrLess.LESS
        c = float(string.split('=')[1])
        return cls(a,b,lessOrGreater,c)

    def to_edge(self) -> Edge:
        return Edge(line=Line(self.a,self.b,self.c))

