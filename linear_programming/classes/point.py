from typing import List

error = 0.001

class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(" + str(round(self.x,5)) + "," + str(round(self.y,5)) + ")"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Point):
            return o.x - error<= self.x <= o.x+error and o.y-error<= self.y <= o.y+error
        return False
    
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def is_inside(self, c:'Constraints') -> bool:
        return c.contains(self)