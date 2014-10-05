import math
import random
from unit import Unit

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
    def floor(self, other):
        return Point(math.floor(self.x), math.floor(self.y))
    def distance(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

class GameMap:

    def __init__(self, rows, cols, map, hero, commander, units, bullets=[]):  # map is a string (or 1d array) of 0s and 1s,
        # 0 meaning no wall, 1 meaning wall.
        # The coordinate of a wall is the top left corner's cartesian coordinate.
        # walls is referenced by walls[x][y] (x goes left to right, y goes top to bottom)
        self.rows = rows
        self.cols = cols
        self.hero = hero
        self.commander = commander
        self.units = units
        self.bullets = bullets
        self.walls = []
        self.map_inp = map
        for c in xrange(cols):
            self.walls.append([])
            for r in xrange(rows):
                self.walls[c].append(int(map[r * cols + c]))
    
    def generate_hostiles(self, num):
        for i in xrange(num):
            ifloorx = 0
            ifloory = 0
            x = 0
            y = 0
            while self.walls[ifloorx][ifloory] == 1:
                x = 1 + random.random() * (self.cols - 1)
                y = 1 + random.random() * (self.rows - 1)
                ifloorx = int(x)
                ifloory = int(y)
            self.units.append(Unit(10, x, y, 0))
            
    def generate_friendlies(self, num):
        for i in xrange(num):
            ifloorx = 0
            ifloory = 0
            x = 0
            y = 0
            while self.walls[ifloorx][ifloory] == 1:
                x = 1 + random.random() * (self.cols - 1)
                y = 1 + random.random() * (self.rows - 1)
                ifloorx = int(x)
                ifloory = int(y)
            self.units.append(Unit(10, x, y, 0, 0))

    def is_accessible(self, pt):
        cell = pt.floor()
        try:
            if self.walls[cell.x][cell.y] == 1:
                return False
            else:
                return True
        except:
            return False

    def accessible_neighbors(self, pt):
        neighbors = []
        for i in xrange(4):
            if self.is_accessible(pt.go(i)):
                neighbors.append(pt.go(i))
        return neighbors


