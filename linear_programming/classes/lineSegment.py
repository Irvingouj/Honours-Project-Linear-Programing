from .point import Point
from .line import Line


class LineSegment:

    # range is the range in terms of x axis
    def __init__(self, line: Line, range_of_line: tuple[float, float]) -> None:
        self.line = line
        self.range = range_of_line

    def is_on_line_segment(self, point: Point) -> bool:
        return self.line.is_on_line(point) and self.range[0] <= point.x <= self.range[1]

    def endpoints(self) -> tuple[Point, Point]:
        return Point(self.range[0], self.line.c/self.line.b), Point(self.range[1], self.line.c/self.line.b)
