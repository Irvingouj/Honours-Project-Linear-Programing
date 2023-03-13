from .edge import Edge
from .point import Point
from .line import Line
from .objectiveFunction import ObjectiveFunction,MaxOrMin
from .constraints import Constraints
from .oneDConstraint import OneDConstraint
from .oneDLinearProgram import solve_1d_linear_program


class LineSegment:

    # range is the range in terms of x axis
    def __init__(self, line:Line,range:tuple[float,float]) -> None:
        self.line = line
        self.range = range
    
    def is_on_line_segment(self, point:Point) -> bool:
        return self.line.is_on_line(point) and self.range[0] <= point.x <= self.range[1]

    def endpoints(self) -> tuple[Point,Point]:
        return Point(self.range[0],self.line.c/self.line.b),Point(self.range[1],self.line.c/self.line.b)
    