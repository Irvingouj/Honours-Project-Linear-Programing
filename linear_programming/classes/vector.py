from typing import List


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
            return [self.arr[i] == __o.arr[i] for i in range(len(self.arr))].count(False) == 0
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
