from abc import ABC, abstractmethod
from typing import List
from linear_programming.classes.two_d import Point, ObjectiveFunction, Constraints


class Solver(ABC):
    @abstractmethod
    def solve(self, obj: ObjectiveFunction, cons: List[Constraints]) -> List[Point]:
        pass
