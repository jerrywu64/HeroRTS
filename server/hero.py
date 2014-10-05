class Hero:
    def __init__(self, hp, x, y, th):  # the commander screen's start coordinates (top left?) and orientation
        self.location = [x, y]
        self.hp = hp
        self.orientation = th # Positive-x-axis, going ccw, in range [0, 2pi).
        self.fov_angle = 1 # Angle from center, in radians, that the hero can 
            # see. This means that the central angle of the cone of the hero's
            # vision is 2 * fov_angle.
        self.fov_radius = 10
        self.radius = 0.3 # The hero is a circle?
        self.speed = 0.06 # squares per tick
        
    def dist(x1, y1, x2, y2):
        return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
        
    def visible(self, x, y, gmap):  # returns if the grid-square (x, y) is visible.
        # Check if the point is in the field of view:
        if dist(x, y, self.location[0], self.location[1]) > self.fov_radius:
            return False
        angle = self.orientation
        if x == self.location[0]:
            if y > self.location[1]:
                angle -= math.pi / 2
            else:
                angle -= 3 * math.pi / 2
        else:
            angle -= math.atan(self.location[1] - y,x - self.location[0])
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        if math.fabs(angle) > fov_angle:
            return false
        # Check if there's a wall in the way:
        # curloc = self.location
        # Never mind, we'll do this later maybe. If it's a wall, though:
        if gmap.walls[x][y] == 1:
            return False
        return True
        
    def move(self, direction, map):  # direction is a number from 0 to 7, starting positive-x and going ccw, relative to your orientation.
        self.location[0] += math.cos(direction * math.pi / 4 + orientation) * self.speed
        self.location[1] += math.sin(direction * math.pi / 4 + orientation) * self.speed
        fracx, floorx = math.modf(self.location[0])
        fracy, floory = math.modf(self.location[1])
        # Collision check, orthogonal walls
        if fracx < self.radius:
            if floorx == 0 or gmap[floorx - 1][floory] == 1:
                self.location[0] += self.radius - fracx
        if 1 - fracx < self.radius:
            if floorx == gmap.cols - 1 or gmap[floorx + 1][floory] == 1:
                self.location[0] -= self.radius + fracx - 1
        if fracy < self.radius:
            if floory == 0 or gmap[floorx][floory - 1] == 1:
                self.location[1] += self.radius - fracy
        if 1 - fracy < self.radius:
            if floory = gmap.rows - 1 or gmap[floorx][floory + 1] == 1:
                self.location[1] -= self.radius + fracy - 1
        # Collision check, corners
        d = dist(floorx, floory, self.location[0], self.location[1])
        if d < self.radius:
            self.location[0] += fracx * (self.radius / d - 1)
            self.location[1] += fracy * (self.radius / d - 1)
        d = dist(floorx + 1, floory, self.location[0], self.location[1])
        if d < self.radius:
            self.location[0] -= (1 - fracx) * (self.radius / d - 1)
            self.location[1] += fracy * (self.radius / d - 1)
        d = dist(floorx, floory + 1, self.location[0], self.location[1])
        if d < self.radius:
            self.location[0] += fracx * (self.radius / d - 1)
            self.location[1] -= (1 - fracy) * (self.radius / d - 1)
        d = dist(floorx + 1, floory + 1, self.location[0], self.location[1])
        if d < self.radius:
            self.location[0] -= (1 - fracx) * (self.radius / d - 1)
            self.location[1] -= (1 - fracy) * (self.radius / d - 1)
        
        