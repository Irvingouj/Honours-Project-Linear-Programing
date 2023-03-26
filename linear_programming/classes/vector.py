import math
from typing import List

import numpy as np


class Vector:
    def __init__(self, arr: List[float]) -> None:
        self.arr = arr

    def __str__(self) -> str:
        return str(self.arr)

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector([self.arr[i] + other.arr[i] for i in range(len(self.arr))])

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector([self.arr[i] - other.arr[i] for i in range(len(self.arr))])

    def __mul__(self, other: 'Vector') -> float:
        if isinstance(other, self.__class__):
            return sum([self.arr[i] * other.arr[i] for i in range(len(self.arr))])
        if isinstance(other, float):
            return Vector([self.arr[i] * other for i in range(len(self.arr))])
        raise TypeError('Invalid type of argument')

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            return np.allclose(self.arr, __o.arr)
        return False

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def projection_on_to(self, other: 'Vector') -> 'Vector':
        return other*(self * other / (other * other))

    def find_orthogonal_vector(self) -> 'Vector':
        arr = [-self.arr[1], self.arr[0]]
        return Vector(arr)

    def length(self) -> float:
        return (self * self)**0.5

    def normalize(self) -> 'Vector':
        return self * (1 / self.length())

    def is_parallel_to(self, other: 'Vector') -> bool:
        return self.find_orthogonal_vector() * other == 0

    def get_rotate(self,degree) -> 'Vector':
        x = self.arr[0]
        y = self.arr[1]
        sin = math.sin(degree)
        cos = math.cos(degree)
        return Vector([x*cos - y*sin, x*sin + y*cos])
    
    def get(self, index):
        return self.arr[index]
    
    def degree_needed_to_rotate_to(self, other: 'Vector') -> float:
        x1 = self.arr[0]
        x2 = other.arr[0]
        y1= self.arr[1]
        y2= other.arr[1]
        dot = x1*x2 + y1*y2      # dot product between [x1, y1] and [x2, y2]
        det = x1*y2 - y1*x2      # determinant
        return math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)

    
    
    def is_perpendicular_to(self, other: 'Vector') -> bool:
        return self * other == 0
