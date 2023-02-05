from typing import List
class Point:
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def is_inside(self, Constraints:'Constraints') -> bool:
        return Constraints.is_inside(self)