from game_map import Point
import random
from collections import deque

class Pathfinder:
    def __init__(self, map, destx, desty, currx, curry): #pathfinder that goes to (x,y)
        self.map, self.dest, self.curr = map, Point(destx, desty), Point(currx, curry)
        #map comes in the form of an array. status of a cell can be queried as map.wals[x][y].
    def can_go(self, direction):
        loc = self.curr.go(direction)
        return self.map.is_accessible(loc)
    def next_cell(self):
        pass

class DumbPathfinder(Pathfinder):
    def random_accessible(self):
        return random.choice(self.map.accessible_neighbors(self.curr))
    def next_cell(self):
        self.curr = self.random_accessible()

class BFSPathfinder(Pathfinder):
    def __init__(self):
        self.super().__init__(self)
        self.bfs()
    def bfs(self):
        self.distances = {self.dest.floor() : 0}
        visited = set([self.dest.floor()])
        queue = deque([self.dest.floor()])
        while len(queue) > 0:
            front = queue.popleft()
            to_visit = self.map.accessible_neighbors(front)
            for pt in to_visit:
                if pt not in visited:
                    self.distances[pt] = self.distances[front] + 1
                    visited.add(pt)
                    queue.append(pt)
    def change_dest(self, pt):
        self.dest = pt
        self.bfs()
    def next_cell(self):
        next = self.curr
        dist = self.distances[self.curr]
        for pt in self.map.accessible_neighbors(self.curr):
            if self.distances[pt] < dist:
                next = pt
                dist = self.distances[pt]
        return next
