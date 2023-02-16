from Classes.Convex import Convex
from Classes.Edge import Edge
from Classes.Line import Line
import matplotlib.pyplot as plt

def main():
    edge1 = Edge(line=Line(1,2,3))
    edge2 = Edge(line=Line(-1, 2, 3))
    edge3 = Edge(line=Line(0.1, -2, 3))

    convex = Convex([])
    convex.add_edge(edge1)
    convex.add_edge(edge2)
    convex.add_edge(edge3)

    edges = convex.get_edges()

    edges:Edge = convex.get_edges()
    for edge in edges:
        print(edge.range)
        print(edge.end_points()[0].x, edge.end_points()[0].y)

if __name__ == "__main__":
    main()
