import math

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __hash__(self):
        return (self.x, self.y).__hash__()
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def go(self, direction): #returns point that is dir away. 0 is right, 1 is up, 2 is left, 3 is down.
        if direction == 0:
            return Point(self.x + 1, self.y)
        elif direction == 1:
            return Point(self.x, self.y - 1)
        elif direction == 2: 
            return Point(self.x - 1, self.y)
        elif direction == 3:
            return Point(self.x, self.y + 1)
    def floor(self):
        return Point(math.floor(self.x), math.floor(self.y))
    def distance(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

