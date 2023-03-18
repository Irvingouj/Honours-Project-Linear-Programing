import math
from linear_programming.classes.vector import Vector



v = Vector([1,2])
v1 = v.get_rotate(math.pi/2)

print(v)
print(v1)
print(v*v1)