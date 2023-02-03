from Edge import Edge
from Point import Point
from Line import Line

def main():
    edge1 = Edge(line=Line(1,2,3), range= (-10, 10), direction= True)
    edge2 = Edge(line=Line(-1, 2, 3), range= (-10, 10),direction= True)
    edge3 = Edge(line=Line(0.1, -2, 3), range= (-10, 10),direction= False)
    p1 = edge1.find_intersection(edge2)
    p2 = edge1.find_intersection(edge3)
    p3 = edge2.find_intersection(edge3)
    print(p1.x, p1.y)
    print(p2.x, p2.y)
    print(p3.x, p3.y)

    

if __name__ == "__main__":
    main()