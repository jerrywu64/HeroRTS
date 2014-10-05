class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def go(self, direction): #returns point that is dir away. 0 is right, 1 is up, 2 is left, 3 is down.
        if direction == 0:
            return Point(self.x + 1, self.y)
        elif direction == 1:
            return Point(self.x, self.y - 1)
        elif direction == 2: 
            return Point(self.x - 1, self.y)
        elif direction == 3:
            return Point(self.x, self.y + 1)

class GameMap:

    def __init__(self, rows, cols, map):  # map is a string of 0s and 1s, 
        # 0 meaning no wall, 1 meaning wall, starting in the 
        # top left and going across first, then down.
        # The coordinate of a wall is the top left corner's cartesian coordinate.
        # walls is referenced by walls[x][y] (x goes left to right, y goes top to bottom)
        self.walls = []
        for c in xrange(cols):
            self.walls.append([])
            for r in xrange(rows):
                self.walls[c].append(int(map[r * cols + c]))

    def is_accessible(self, pt):
        if self.walls[pt.x][pt.y] == 1:
            return False
        else:
            return True


