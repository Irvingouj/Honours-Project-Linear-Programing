from linear_programming.classes.three_d import Point3D
from linear_programming.classes.vector import Vector


class Line3d:
    def __init__(self,point:Point3D,vector:Vector) -> None:
        assert vector.dimension() == 3
        self.point = point
        self.vector = vector

    @classmethod
    def from_two_points(cls,point1:Point3D,point2:Point3D) -> 'Line3d':
        vec = Vector([point2.x-point1.x,point2.y-point1.y,point2.z-point1.z])
        return cls(point1,vec)