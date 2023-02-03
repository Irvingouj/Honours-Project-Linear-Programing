from Line import Line
from typing import Tuple
from Point import Point

class Edge:
    # edge is a line with a range of x values and direction
    # tuple is the range of x indices, direction is ax + by<c (true) or ax + by>c (false)
    def __init__(self, line:Line, direction:bool = True ,range:Tuple[float,float] = (float('-inf'),float('inf'))):
        # make sure you is is always less than
        if(direction):
            self.a = line.a
            self.b = line.b
            self.c = line.c
        else:
            self.a = -line.a
            self.b = -line.b
            self.c = -line.c
        self.range = range
        
        
    def is_on_edge(self, point:Point) -> bool:
        return self.range[0] <= point.x <= self.range[1] and self.a * point.x + self.b * point.y == self.c

    def is_in_area(self, point:Point) -> bool:
        return self.range[0] <= point.x <= self.range[1] and self.a * point.x + self.b * point.y <= self.c

    def find_intersection(self, edge:'Edge') -> Point:
        line1 = Line(self.a, self.b, self.c)
        line2 = Line(edge.a, edge.b, edge.c)
        point = line1.find_intersection(line2)
        
        # if point is inside both ranges, then return the point
        if self.range[0] <= point.x <= self.range[1] and edge.range[0] <= point.x <= edge.range[1]:
            return point
        else:
            return None
    
    def update_range(self, point:Point) -> None:
        # update the range of the edge to include the point
        if point.x > self.range[0]:
            self.range = (point.x, self.range[1])
        elif point.x < self.range[1]:
            self.range = (self.range[0], point.x)
        else:
            return
    
    def end_points(self) -> Tuple[Point,Point]:
        # return the end points of the edge
        return (Point(self.range[0], (self.c - self.a * self.range[0])/self.b), Point(self.range[1], (self.c - self.a * self.range[1])/self.b))

    def range(self) -> Tuple[float,float]:
        return self.range
    def __str__(self) -> str:
        return self.end_points()[0].__str__() + " " + self.end_points()[1].__str__() + " "+ str(self.a)+"x+" +str(self.b)+ "y<="+str(self.c)
