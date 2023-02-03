from Convex import Convex
from Edge import Edge
from Point import Point
from Line import Line
import matplotlib.pyplot as plt

def main():
    edge1 = Edge(line=Line(1,2,3))
    edge2 = Edge(line=Line(-1, 2, 3))
    edge3 = Edge(line=Line(0.1, -2, 3))

    convex = Convex([])
    convex.add_edge(edge1)
    convex.add_edge(edge2)
    convex.add_edge(edge3)

    # print(convex.is_inside(Point(0,0)))
    edges = convex.get_edges()
    # for edge in edges:
        # plt.plot(edge.end_points()[0].x, edge.end_points()[1].y, 'ro')
    # line 1 points
    # x1 = [1,2,3]
    # y1 = [2,4,1]
    # # plotting the line 1 points 
    # plt.plot(x1, y1, label = "line 1")
    
    # # line 2 points
    # x2 = [1,2,3]
    # y2 = [4,1,3]
    # # plotting the line 2 points 
    # plt.plot(x2, y2, label = "line 2")

    edges:Edge = convex.get_edges()
    for edge in edges:
        print(edge.range)
        print(edge.end_points()[0].x, edge.end_points()[0].y)
    # for edge in edges:
    #     plt.plot([edge.end_points()[0].x], [edge.end_points()[0].y], label = "line ")

    #     # naming the x axis
    # plt.xlabel('x - axis')
    # # naming the y axis
    # plt.ylabel('y - axis')
    # # giving a title to my graph
    # plt.title('Two lines on same graph!')
    
    # # show a legend on the plot
    # plt.legend()
    
    # # function to show the plot
    # plt.show()


if __name__ == "__main__":
    main()
