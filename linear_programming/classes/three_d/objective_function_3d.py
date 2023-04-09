import re
from typing import Tuple
import numpy as np

from linear_programming.classes.two_d import MaxOrMin
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

    def get_rotate_x(self,theta:float) -> 'ObjectiveFunction3D':
        
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta), np.cos(theta)]
            ]
        )

        vec = np.array([self.a, self.b, self.c])
        
        res_vec = rotation_matrix @ vec
        res = ObjectiveFunction3D(res_vec[0], res_vec[1], res_vec[2], self.maxOrMin)
    
        return res
    def get_rotate_y(self,angle:float) -> 'ObjectiveFunction3D':
            
        R = np.array([[np.cos(angle), 0, np.sin(angle)], 
                      [0, 1, 0], 
                      [-np.sin(angle), 0, np.cos(angle)]])

        vec = np.array([self.a, self.b, self.c])
        res_vec = R @ vec
        return ObjectiveFunction3D(res_vec[0], res_vec[1], res_vec[2], self.maxOrMin)
    
    def get_rotate_z(self,angle:float) -> 'ObjectiveFunction3D':
        R = np.array([[np.cos(angle), -np.sin(angle), 0],
                      [np.sin(angle), np.cos(angle), 0],
                      [0, 0, 1]])
        vec = np.array([self.a, self.b, self.c])
        vec = R @ vec
        return ObjectiveFunction3D(vec[0], vec[1], vec[2], self.maxOrMin)
    
    def get_angle_needed_for_rotation(self) -> Tuple[float,float]:
        """
        theta is the angle needed to rotate the vector around the x-axis
        phi is the angle needed to rotate the vector around the y-axis
        we are rotating the objective function vector to (0,0,1)
        """
        x = self.a
        y = self.b
        z = self.c
        theta = np.arctan2(x,y)
        
        y_prime = x * np.sin(theta) + y * np.cos(theta)
        z_prime = z
        
        phi = np.arctan2(y_prime,z_prime)

        return theta, phi

        
    def to_vector(self) -> Vector:
        return Vector([self.a, self.b, self.c])

    def __str__(self) -> str:
        return ('max' if self.maxOrMin == MaxOrMin.MAX else 'min') + ' ' + str(self.a) + 'x + ' + str(self.b) + 'y + ' + str(self.c) + 'z'

