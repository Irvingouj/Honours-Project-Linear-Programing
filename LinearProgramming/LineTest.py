from Classes.Line import Line 
from Classes.Point import Point

def main():
    line1 = Line(1, 2, 3)
    line2 = Line(-1, 2, 3)
    p = line1.find_intersection(line2)
    print(p.x, p.y)

if __name__ == "__main__":
    main()