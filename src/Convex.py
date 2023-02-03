from Edge import Edge
from typing import List, Set
from Point import Point


class Convex:
    def __init__(self,edges:List[Edge]) -> None:
        self.edges = edges

    def is_inside(self, point:Point) -> bool:
        for edge in self.edges:
            if not edge.is_in_area(point):
                return False
        return True

    def add_edge(self, new_edge:Edge) -> None:
        #calculate the intersection of the new edge with all the other edges
        #if the intersection is on the edge, then update the range of the edges to include the intersection
        toRemove = []
        print("new edge: ", new_edge)
        for edge in self.edges:
            intersection = new_edge.find_intersection(edge)
            print("intersection: ", intersection , " edge1: [", edge , "] edge2: [", new_edge, "]" )
            if intersection is None:
                endpoints = edge.end_points()
                # if niether end point is in the area, then the edge is not in the area, remove it
                if not self.is_inside(endpoints[0]) and not self.is_inside(endpoints[1]):
                    toRemove.append(edge)
            else:#update the range of the edges
                edge.update_range(intersection)
                new_edge.update_range(intersection)

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


