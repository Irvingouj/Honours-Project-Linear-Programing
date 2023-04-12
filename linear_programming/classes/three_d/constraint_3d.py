import re
from typing import Tuple
import numpy as np
from linear_programming.classes.vector import Vector
from linear_programming.classes.two_d import GreaterOrLess
from .point3d import Point3D
from .plane import Plane
from .line_3d import Line3d


class Constraints3D:
    def __init__(self, a: float, b: float, c: float, lessOrGreater: GreaterOrLess = GreaterOrLess.LESS, d: float = 0) -> None:
        if a == 0 and b == 0 and c == 0:
            raise ValueError('Cannot create constraint with a=0, b=0 and c=0')
        if lessOrGreater == GreaterOrLess.LESS:
            self.a,self.b,self.c,self.d = a,b,c,d
        else:
            self.a,self.b,self.c,self.d = -a,-b,-c,-d

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

    def find_intersection(self, other: 'Constraints3D') -> Line3d:
        if self.facing_direction_vector().normalize()* other.facing_direction_vector().normalize() == 1:
            raise ValueError('The two constraints are parallel')
        
        a1,a2,a3,l1 = self.a,self.b,self.c,self.d
        b1,b2,b3,l2 = other.a,other.b,other.c,other.d
        
        A = np.array([[a1,a2],[b1,b2]])

        # t = 1
        b1 = np.array([l1 - a3, l2 - b3])
        x1 = np.linalg.solve(A, b1)
        
        # t = 0
        b2 = np.array([l1, l2])
        x2 = np.linalg.solve(A, b2)
        
        return Line3d.from_two_points(Point3D(x1[0],x1[1],1),Point3D(x2[0],x2[1],0))
        

    def rotate_x(self, angle: float) -> 'Constraints3D':
        R = np.array([[1, 0, 0], 
                      [0, np.cos(angle), -np.sin(angle)],
                      [0, np.sin(angle), np.cos(angle)]])
        [a, b, c] = R@np.array([self.a, self.b, self.c])
        d = self.d * np.linalg.det(R)
        
        self.a,self.b,self.c,self.d = a,b,c,d
        
        
    def get_rotate_x(self,angle:float) -> 'Constraints3D':
        res = Constraints3D(self.a,self.b,self.c,GreaterOrLess.LESS,self.d)
        res.rotate_x(angle)
        return res
        
    def rotate_y(self, angle: float) -> None:
        R = np.array([[np.cos(angle), 0, np.sin(angle)], 
                      [0, 1, 0], 
                      [-np.sin(angle), 0, np.cos(angle)]])
        [a, b, c] = R @ np.array([self.a, self.b, self.c])
        d = self.d * np.linalg.det(R)
        
        self.a,self.b,self.c,self.d = a,b,c,d
    
    def get_rotate_y(self,angle:float) -> 'Constraints3D':
        res = Constraints3D(self.a,self.b,self.c,GreaterOrLess.LESS,self.d)
        res.rotate_y(angle)
        return res

    def rotate_z(self, angle: float) -> None:
        R = np.array([[np.cos(angle), -np.sin(angle), 0], 
                      [np.sin(angle), np.cos(angle), 0], 
                      [0, 0, 1]])
        [a, b, c] = R @ np.array([self.a, self.b, self.c])
        d = self.d * np.linalg.det(R)
        
        self.a,self.b,self.c,self.d = a,b,c,d
        
    def get_rotate_z(self,angle:float) -> 'Constraints3D':
        res = Constraints3D(self.a,self.b,self.c,GreaterOrLess.LESS,self.d)
        res.rotate_z(angle)
        return res
        
        
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
        if self.b == 0:
            return Vector([-self.a,0,-self.c])
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
            return vector.normalize()
        else:
            return Vector([-vector[0], -vector[1], -vector[2]]).normalize()
        
    def find_random_point_on_plane(self) -> Point3D:
        if self.c == 0:
            y = np.random.uniform(1,2)
            x = (self.d - self.b*y)/self.a
            return Point3D(x,y,0)
        x = np.random.uniform(1,2)
        y = np.random.uniform(1,2)
        z = (self.d -self.a*x - self.b*y)/self.c
        
        return Point3D(x,y,z)
    def contain_line(self, line: Line3d) -> bool:
    
        """
        returns true if the line is contained in the constraint
        cross product of the two vectors that span the vector space is perpendicular to the line if the line is contained in the plane
        """
        if not self.contains(line.point):
            return False

        vec_space = self.get_vector_space();
        cross_product = np.cross(np.array(vec_space[0].arr), np.array(vec_space[1].arr)) 
        b = np.array(line.vector.arr)
        
        return np.isclose(np.dot(cross_product, b), 0)
        
        
    def get_flip_sign(self) -> 'Constraints3D':
        res = Constraints3D(self.a,self.b,self.c,GreaterOrLess.GREATER,self.d)
        return res
    
    def __str__(self) -> str:
        return f'{self.a}x + {self.b}y + {self.c}z <= {self.d}'

    def str_float(self) -> str:
        return f'{self.a:.2f}x + {self.b:.2f}y + {self.c:.2f}z <= {self.d:.2f}'

    def to_or_string(self) -> str:
        return f'{self.a}*x + {self.b}*y + {self.c}*z <= {self.d}'
    
    def copy(self) -> 'Constraints3D':
        return Constraints3D(self.a,self.b,self.c,GreaterOrLess.LESS ,self.d)

    def angle_between(self, other: 'Constraints3D') -> float:
        """
        returns the angle between the two planes in radians
        """
        return np.arccos(np.dot(self.facing_direction_vector().normalize().arr, other.facing_direction_vector().normalize().arr))

    @classmethod
    def from_plane(cls, plane: Plane) -> 'Constraints3D':
        return cls(plane.a, plane.b, plane.c, d=plane.d)

    def flip_sign(self) -> 'Constraints3D':
        return Constraints3D(self.a,self.b,self.c,GreaterOrLess.GREATER,self.d)

    def find_point_with_x_y(self, x: float, y: float) -> Point3D:
        if self.c == 0:
            raise ValueError("c can be zero, but I'll fix it later")
        z = (self.d - self.a*x - self.b*y)/self.c
        return Point3D(x,y,z)

    def is_on_boundary(self, point: Point3D) -> bool:
        return np.isclose(self.a*point.x + self.b*point.y + self.c*point.z, self.d)