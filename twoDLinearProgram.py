from typing import List, Union
from oneDLinearProgram import Line
from oneDLinearProgram import Point

class HalfPlane:

    # ax + by + <= c
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c

    def is_inside(self, point:Point) -> bool:
        return self.a * point.x + self.b * point.y <= self.c
        
    def get_line(self) -> Line:
        return Line(self.a, self.b, self.c)

class TwoDObjective:
    # min ax + by, standard form of linear programming
    def __init__(self, a:float, b:float):
        self.a = a
        self.b = b

class Convex:
    def __init__(self, left_edges: List[HalfPlane],right_edges: List[HalfPlane]):
        for left_edge in left_edges:
            if left_edge.a > 0:
                raise Exception("left edge should have negative a")
        for right_edge in right_edges:
            if right_edge.a < 0:
                raise Exception("right edge should have positive a")
        self.left_edges = left_edges
        self.right_edges = right_edges

    def is_inside(self, point:Point) -> bool:
        for halfPlane in self.halfPlanes:
            if not halfPlane.is_inside(point):
                return False
        return True
    def intersect_halfplane(self, halfPlane:HalfPlane) -> Line:
        if halfPlane.a < 0:
            self.left_edges.append(halfPlane)
        else:
            self.right_edges.append(halfPlane)

    def find_intersection(self, line:Line) -> List[Point, Point]:
        
        

# m1, m2 bound the objective function, assume the objective function does not go horizontally (i.e. a1 != 0)
#
# -------------------------------------------------------------------------------------------------------------- m1
#
#
#
#--------------------------------------------------------------------------------------------------------------- m2
#

def decide_corner(m1:HalfPlane, m2:HalfPlane,objective:TwoDObjective) -> Point:
    raise Exception("Not implemented yet")

def calculate_v(halfPlane, added_constraints, objective):
    raise Exception("Not implemented yet")


def solve_2d_linear_program_bounded(halfPlanes: List[HalfPlane], objective: TwoDObjective, m1:HalfPlane, m2: HalfPlane) -> Point:
    v = decide_corner(m1, m2, objective)
    added_constraints = []
    added_constraints.append(m1)
    added_constraints.append(m2)
    for halfPlane in halfPlanes:
        if not halfPlane.is_inside(v):
            v = calculate_v(halfPlane, added_constraints, objective)
        added_constraints.append(halfPlane)
    return v