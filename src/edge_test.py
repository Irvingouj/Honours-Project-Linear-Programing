from Edge import Edge
from Point import Point
from Line import Line

def main():
    edge1 = Edge(line=Line(1,2,3))
    edge2 = Edge(line=Line(-1, 2, 3))
    edge3 = Edge(line=Line(1, -2, 3))
    edge4 = Edge(line=Line(-1, -2, 3))
    special_edge = Edge(line=Line(-1, -2, 6))
    
    ## intersect all edges between each other
    edges  = [special_edge,edge1, edge2, edge3, edge4]
    for edgei in edges:
        for edgej in edges:
            edgei.intersect_and_update_range(edgej)



    #print all the edges
    for edge in edges:
        print(edge)


    

if __name__ == "__main__":
    main()