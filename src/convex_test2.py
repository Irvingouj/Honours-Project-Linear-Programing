from Classes import *;
from typing import List;

def print_edges(c:Convex):
    edges:List[Edge] = c.get_edges();
    for edge in edges:
        print(edge);

c:Convex = Convex([]);
print_edges(c);
c.add_edge(Edge(Line(1,2,3)));
print("after add edge1 -----------------------------------");
print_edges(c);
c.add_edge(Edge(Line(-1,2,3)));
print("after add edge2 -----------------------------------");

