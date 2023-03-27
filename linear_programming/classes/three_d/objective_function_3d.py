import re
from typing import Tuple
import numpy as np

from linear_programming.classes.objectiveFunction import MaxOrMin
from linear_programming.classes.vector import Vector
from .point3d import Point3D



class ObjectiveFunction3D:
    # ax + by + cz
    def __init__(self, a, b, c, maxOrMin=MaxOrMin.MAX):
        if maxOrMin == MaxOrMin.MAX:
            self.a = a
            self.b = b
            self.c = c
        else:
            self.a = -a
            self.b = -b
            self.c = -c
        self.maxOrMin = maxOrMin

    def value(self, point: Point3D) -> float:
        return self.a * point.x + self.b * point.y + self.c * point.z

    @classmethod
    def from_string(cls, string: str) -> 'ObjectiveFunction3D':
        pattern = re.compile(
            r'(max|min)\s?[+-]?([0-9]*[.])?[0-9]+x\s?\+\s?[+-]?([0-9]*[.])?[0-9]+y\s?\+\s?[+-]?([0-9]*[.])?[0-9]+z\s?')
        if pattern.match(string) is None:
            raise ValueError('Invalid string: ' + string)
        maxOrMin = MaxOrMin.MAX if string.find('max') != -1 else MaxOrMin.MIN
        a_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+x',
                          string).group(0).split('x')[0]
        b_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+y',
                          string).group(0).split('y')[0]
        c_str = re.search(r'[+-]?([0-9]*[.])?[0-9]+z',
                          string).group(0).split('z')[0]
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)
        return cls(a, b, c, maxOrMin)

    def to_or_string(self) -> str:
        return str(self.a) + '*x + ' + str(self.b) + '*y + ' + str(self.c) + '*z'

    def to_vector(self) -> Vector:
        return Vector([self.a, self.b, self.c])
    

    def get_angle_needed_for_rotation(self) -> Tuple[float,float]:
        """
        theta is the angle needed to rotate the vector around the x-axis
        phi is the angle needed to rotate the vector around the y-axis
        we are rotating the objective function vector to (0,0,1)
        """
        x = self.a
        y = self.b
        z = self.c
        theta = np.arccos(z/np.sqrt(y**2 + z**2))
        phi = np.arccos(np.sqrt(y**2 + z**2)/np.sqrt(x**2 + y**2 + z**2))

        return theta, phi

        
        

    def __str__(self) -> str:
        return ('max' if self.maxOrMin == MaxOrMin.MAX else 'min') + ' ' + str(self.a) + 'x + ' + str(self.b) + 'y + ' + str(self.c) + 'z'
