from Classes.Convex import Convex
from Classes.ObjectiveFunction import MaxOrMin, ObjectiveFunction
from Classes.Edge import Edge
from Classes.Line import Line
from Classes.Point import Point

convex:Convex = Convex([])
obj = ObjectiveFunction(1,1,MaxOrMin.MAX)
v = convex.find_optimal(obj)
print(1.8 * 10308)
print(obj.value(v[0]))
print(v[0])