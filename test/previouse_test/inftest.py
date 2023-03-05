from LinearProgramming.Classes.Convex import Convex
from LinearProgramming.Classes.ObjectiveFunction import MaxOrMin, ObjectiveFunction
from LinearProgramming.Classes.Edge import Edge
from LinearProgramming.Classes.Line import Line
from LinearProgramming.Classes.Point import Point

convex:Convex = Convex([])
obj = ObjectiveFunction(1,1,MaxOrMin.MAX)
v = convex.find_optimal(obj)
print(1.8 * 10308)
print(obj.value(v[0]))
print(v[0])