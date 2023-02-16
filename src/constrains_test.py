
from Constraints import Constraints
from Classes.ObjectiveFunction import ObjectiveFunction
c = Constraints.from_string('1x+2y<=3')
print(c.to_edge())

o = ObjectiveFunction.from_string('max 1x+2y')
print(o)