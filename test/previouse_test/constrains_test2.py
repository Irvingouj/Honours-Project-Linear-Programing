
from Classes.Constraints import Constraints
from LinearProgramming.Classes.ObjectiveFunction import ObjectiveFunction
c = Constraints.from_string('1x+1y<=3')
c2 = Constraints.from_string('1x+1y>=3')

# res = c.is_parallel_and_contains_each_other(c2)
print(c.facing_direction_vector())
print(c2.facing_direction_vector())

