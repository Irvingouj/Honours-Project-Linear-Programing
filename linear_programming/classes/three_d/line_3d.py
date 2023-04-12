from linear_programming.classes.two_d.line import Line
from linear_programming.classes.two_d.point import Point
from .point3d import Point3D
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

    def __str__(self) -> str:
        return f'{self.point} + t *{self.vector}'

    def get_projection_on_x_y_plane(self) -> 'Line':
        x_1,y_1 = self.point.x,self.point.y
        x_2,y_2 = self.point.x + self.vector[0],self.point.y + self.vector[1]
        if x_1 != x_2:
            a = (y_2-y_1)/(x_1-x_2)
            b = 1
            c = a*x_1 + y_1
            return Line(a=a,b=b,c=c)
        return Line(a=1,b=0,c=x_1)
        