from Convex import Convex
from Edge import Edge
from Point import Point
from Line import Line

def main():
    edge1 = Edge(line=Line(1,2,3))
    edge2 = Edge(line=Line(-1, 2, 3))
    edge3 = Edge(line=Line(0.1, -2, 3))

    convex = Convex([])
    convex.add_edge(edge1)
    convex.add_edge(edge2)
    convex.add_edge(edge3)

    print(convex.is_inside(Point(0,0)))

if __name__ == "__main__":
    main()
