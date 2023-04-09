from enum import Enum
from typing import Tuple
from .point import Point
from .line import Line




class EdgeDirection(Enum):
    # ax+by <= c where a is positive
    FACING_LEFT = 0
    # ax+by <= c where a is negative
    FACING_RIGHT = 1


class ToThe(Enum):
    LEFT = 0
    RIGHT = 1


class Edge:
    # edge is a line with a range of x values and direction that it faces
    # tuple is the range of x indices, direction is ax + by<c (true) or ax + by>c (false)
    def __init__(self, line: Line, direction: bool = True, range: Tuple[float, float] = (float('-inf'), float('inf'))):
        # make sure you is is always less than
        if (direction):
            self.a = line.a
            self.b = line.b
            self.c = line.c
        else:
            self.a = -line.a
            self.b = -line.b
            self.c = -line.c
        self.range = range

    def is_on_edge(self, point: Point) -> bool:
        return self.range[0] <= point.x <= self.range[1] and self.a * point.x + self.b * point.y == self.c

    def is_in_area(self, point: Point) -> bool:
        return self.range[0] <= point.x <= self.range[1] and self.a * point.x + self.b * point.y <= self.c

    def find_intersection(self, edge: 'Edge') -> Point:
        line1 = Line(self.a, self.b, self.c)
        line2 = Line(edge.a, edge.b, edge.c)
        point = line1.find_intersection(line2)

        # parallel lines
        if (point is None):
            return None

        # if point is inside both ranges, then return the point
        if self.range[0] <= point.x <= self.range[1] and edge.range[0] <= point.x <= edge.range[1]:
            return point
        else:
            return None

    def is_intersect_with(self, edge: 'Edge') -> bool:
        return self.find_intersection(edge) is not None

    def intersect_and_update_range(self, edge: 'Edge') -> bool:
        intersection = self.find_intersection(edge)
        if intersection is None:
            return False
        else:
            a_facing = self.facing_direction()
            b_facing = edge.facing_direction()

            edge.update_range(intersection.x, ToThe.LEFT if a_facing ==
                              EdgeDirection.FACING_RIGHT else ToThe.RIGHT)
            self.update_range(intersection.x, ToThe.LEFT if b_facing ==
                              EdgeDirection.FACING_RIGHT else ToThe.RIGHT)
            return True

    def end_points(self) -> Tuple[Point, Point]:
        # return the end points of the edge
        return (Point(self.range[0], (self.c - self.a * self.range[0])/self.b), Point(self.range[1], (self.c - self.a * self.range[1])/self.b))

    def update_range(self, x: float, discard: ToThe) -> None:
        if discard == ToThe.LEFT:
            self.range = (x, self.range[1])
        else:
            self.range = (self.range[0], x)

    def to_line(self) -> Line:
        return Line(self.a, self.b, self.c)

    def facing_direction(self) -> EdgeDirection:
        if self.a > 0:
            return EdgeDirection.FACING_LEFT
        else:
            return EdgeDirection.FACING_RIGHT

    def __str__(self) -> str:
        range: str = "range = [" + \
            str(self.range[0]) + " " + str(self.range[1]) + "]"
        endPoints: str = "[left:" + self.end_points()[0].__str__() + \
            " , right = " + self.end_points()[1].__str__() + "]"
        return range + " " + endPoints + " " + str(self.a) + "x +" + str(self.b) + "y<= " + str(self.c)
