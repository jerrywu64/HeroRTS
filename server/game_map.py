class GameMap:

    def __init__(self, rows, cols, map):  # map is a string (or 1d array) of 0s and 1s, 
        # 0 meaning no wall, 1 meaning wall.
        # The coordinate of a wall is the top left corner's cartesian coordinate.
        # walls is referenced by walls[x][y] (x goes left to right, y goes top to bottom)
        self.rows = rows
        self.cols = cols
        
        self.walls = []
        for c in xrange(cols):
            self.walls.append([])
            for r in xrange(rows):
                self.walls[c].append(int(map[r * cols + c]))
