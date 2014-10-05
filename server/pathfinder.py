from game_map import Point
import random

class Pathfinder:
    def __init__(self, map, destx, desty, currx, curry): #pathfinder that goes to (x,y)
        self.map, self.dest, self.curr = map, Point(destx, desty), Point(currx, curry)
        #map comes in the form of an array. status of a cell can be queried as map.wals[x][y].
        self.distances = {}
    def can_go(self, direction):
        loc = self.curr.go(direction)
        return self.map.is_accessible(loc)
    def next_cell(self):
        pass

class DumbPathfinder(Pathfinder):
    def next_cell(self):
        possible = []
        for i in xrange(4):
            if self.can_go(i):
                possible.append(self.curr.go(direction))
        self.curr = random.choice(possible)
