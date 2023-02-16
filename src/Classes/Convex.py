from Classes.Edge import Edge
from Classes.Point import Point
from Classes.ObjectiveFunction import MaxOrMin, ObjectiveFunction
from Classes.Line import Line
from typing import List, Set

max = 1.8*10308;
edge_up = Edge(line=Line(0,1,max))
edge_down = Edge(line=Line(0,-1,max))
edge_left = Edge(line=Line(-1,0.00001,max))
edge_right = Edge(line=Line(1,0.00001,max))


class Convex:
    def __init__(self,edges:List[Edge],bounded:str = "above") -> None:
        self.edges:List[Edge] = []
        # self.add_edge(edge_left)
        # self.add_edge(edge_right)
        # if bounded == "above":
        #     self.add_edge(edge_up)
        # if bounded == "below":
        #     self.add_edge(edge_down)
        for edge in edges:
            self.add_edge(edge)

    def is_inside(self, point:Point) -> bool:
        if len(self.edges) == 0:
            return True
        for edge in self.edges:
            if not edge.is_in_area(point):
                return False
        return True

    def add_edge(self, new_edge:Edge) -> None:
        toRemove = []
        for edge in self.edges:
            if edge.is_intersect_with(new_edge):
                new_edge.intersect_and_update_range(edge)
            else:
                if not new_edge.is_in_area(edge.end_points()[0]) and not new_edge.is_in_area(edge.end_points()[1]):
                    toRemove.append(edge)

        # remove the edges that are not in the area
        for edge in toRemove:
            self.edges.remove(edge)
        # add the new edge
        self.edges.append(new_edge)

    def get_vertices(self) -> Set[Point]:
        # return the vertices of the convex
        vertices = {}
        for edge in self.edges:
            vertices.add(edge.end_points()[0])
        return vertices

    def get_edges(self) -> List[Edge]:
        return self.edges

    def intersect_two_edges(edge1:Edge, edge2:Edge) -> Point:
        point = edge1.find_intersection(edge2)
        if point is None:
            return None
        else:
            edge1.find_intersection(edge2)
            return point
    
    def find_optimal(self,obj:ObjectiveFunction) -> List[Point]:
        # find the optimal point in the convex
        # return a list of points

        optimal_values = []
        current_optimal = None
        for edge in self.edges:
            point = edge.end_points()[0]
            print("points :",point)
            if current_optimal is None:
                current_optimal = point
                optimal_values.append(current_optimal)
            else:
                if obj.maxOrMin == MaxOrMin.MAX:
                    if obj.value(point) > obj.value(current_optimal):
                        current_optimal = point
                        optimal_values.clear()
                        optimal_values.append(current_optimal)
                    elif obj.value(point) == obj.value(current_optimal):
                        optimal_values.append(current_optimal)
                else:
                    if obj.value(point) < obj.value(current_optimal):
                        current_optimal = point
                        optimal_values.clear()
                        optimal_values.append(current_optimal)
                    elif obj.value(point) == obj.value(current_optimal):
                        optimal_values.append(current_optimal)
        
        return optimal_values
        
