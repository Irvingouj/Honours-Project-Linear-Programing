from typing import List
import numpy as np

error = 0.0001


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(" + str(round(self.x, 5)) + "," + str(round(self.y, 5)) + ")"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Point):
            return np.allclose([self.x, self.y], [o.x, o.y], atol=error)
        return False

    def __add__(self, o: 'Point') -> 'Point':
        return Point(self.x + o.x, self.y + o.y)

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def is_inside(self, c: 'Constraints') -> bool:
        return c.contains(self)
