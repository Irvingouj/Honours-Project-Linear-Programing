from Classes.Point import Point

class Line:
    # ax + by = c
    def __init__(self, a:float, b:float, c:float):
        self.a = a
        self.b = b
        self.c = c
    
    def is_on_line(self, point:Point) -> bool:
        return self.a * point.x + self.b * point.y == self.c
    
    def find_intersection(self,line:'Line') -> Point:
        a_1 = self.a
        b_1 = self.b
        c_1 = self.c
        a_2 = line.a
        b_2 = line.b
        c_2 = line.c
        # check if lines are parallel
        if a_1*b_2 == a_2*b_1:
            return None

        y = (a_2*c_1 - a_1*c_2)/(a_2*b_1 - a_1*b_2)
        x = (c_1 - b_1*y)/a_1
        return Point(x,y)
