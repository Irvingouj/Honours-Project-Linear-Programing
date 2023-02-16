from Classes import *;
"-1x +1e-05y<= 18554.4 [-18554.214456 0.0]"
"1x +2y<= 3"

e1 = Edge(Line(-1,0.00001,18554.4),range=(-18554.214456,0))
e2 = Edge(Line(1,2,3))

e1.is_intersect_with(e2)