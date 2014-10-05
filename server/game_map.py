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
