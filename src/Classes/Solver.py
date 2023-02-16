from abc import ABC, abstractmethod
from typing import List
from Classes.ObjectiveFunction import ObjectiveFunction
from Classes.Constraints import Constraints
from Classes.Point import Point

class Solver(ABC):
    @abstractmethod
    def solve(self, obj:ObjectiveFunction, cons:List[Constraints]) -> List[Point]:
        pass