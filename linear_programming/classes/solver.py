from abc import ABC, abstractmethod
from typing import List
from .point import Point
from .objectiveFunction import ObjectiveFunction
from .constraints import Constraints


class Solver(ABC):
    @abstractmethod
    def solve(self, obj: ObjectiveFunction, cons: List[Constraints]) -> List[Point]:
        pass
