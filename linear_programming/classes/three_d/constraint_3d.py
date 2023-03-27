import re
from typing import Tuple
import numpy as np

from linear_programming.classes.constraints import GreaterOrLess

from linear_programming.classes.three_d.plane import Plane
from linear_programming.classes.three_d.point3d import Point3D
from linear_programming.classes.vector import Vector


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

    def contains(self, point:Point3D) -> bool:
        # computer arithmetic is not precise enough
        return self.a * point.x + self.b * point.y + self.c * point.z < self.d or np.isclose(self.a * point.x + self.b * point.y + self.c * point.z, self.d)

    def find_intersection(self, other: 'Constraints3D') -> Point3D:
        return self.to_plane().find_intersection(other.to_plane())

    def rotate_x(self, angle: float) -> 'Constraints3D':
        R = np.array([[1, 0, 0], 
                      [0, np.cos(angle), -np.sin(angle)],
                      [0, np.sin(angle), np.cos(angle)]])
        [a, b, c] = R@np.array([self.a, self.b, self.c])
        d = self.d * np.linalg.det(R)
        
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
    def rotate_y(self, angle: float) -> None:
        R = np.array([[np.cos(angle), 0, np.sin(angle)], 
                      [0, 1, 0], 
                      [-np.sin(angle), 0, np.cos(angle)]])
        [a, b, c] = R @ np.array([self.a, self.b, self.c])
        d = self.d * np.linalg.det(R)
        
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
    def rotate_z(self, angle: float) -> None:
        R = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
        [a, b, c] = R @ np.array([self.a, self.b, self.c])
        d = self.d * np.linalg.det(R)
        
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
        
    def get_vector_space(self) -> Tuple[Vector,Vector]:
        """ 
        a plane is a vector space is R3,
        this function returns the two vectors that span the vector space
        notice that the constant on the right hand side is not considered
        
        Returns:
            Tuple[Vector,Vector]: _description_
        """
        return Vector([0,-self.c/self.b,1]), Vector([1,0,-self.a/self.c])
    
    def get_perpendicular_vector(self) -> Vector:
        """
        return the vector that is perpendicular to the constraint plane
        Returns:
            Vector: _description_
        """
        return Vector([self.a/self.b,1,self.c/self.b])

    
    def facing_direction_vector(self) -> Vector:
        """
        returns the vector that is perpendicular to the constraint plane
        and the points in the direction are contained in the constraint
        """
        vector = self.get_perpendicular_vector()
        point = self.find_random_point_on_plane()
        
        p1 = Point3D(point.x + vector[0], point.y + vector[1], point.z + vector[2])
        
        if self.contains(p1):
            return vector
        else:
            return Vector([-vector[0], -vector[1], -vector[2]])
        
    def find_random_point_on_plane(self) -> Point3D:
        x = np.random.uniform(1,2)
        y = np.random.uniform(1,2)
        z = self.d -(self.a*x + self.b*y)/self.c
        
        return Point3D(x,y,z)
    
    def __str__(self) -> str:
        return f'{self.a}x + {self.b}y + {self.c}z <= {self.d}'
    @classmethod
    def from_plane(cls, plane: Plane) -> 'Constraints3D':
        return cls(plane.a, plane.b, plane.c, d=plane.d)
