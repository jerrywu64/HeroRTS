class GameMap:

    def __init__(self, rows, cols, map):  # map is a string of 0s and 1s, 
        # 0 meaning no wall, 1 meaning wall, starting in the 
        # top left and going across first, then down.
        # The coordinate of a wall is the top left corner's cartesian coordinate.
        self.walls = [] # this will receive arrays as elements
        for r in xrange(rows):
            walls[r] = []
            for c in xrange(cols):
                walls[r][c] = int(map[r * cols + c])

