class Unit:
    def __init__(self, hp, x, y, th):
        self.location = [x, y]
        self.hp = hp
        self.orientation = th 
        self.radius = 0.3
        self.speed = 0.015
    
    def dist(x1, y1, x2, y2):
        return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
        
    def move(self, direction, gmap):  # direction is a number from 0 to 7, starting positive-x and going ccw, relative to your orientation.
        self.location[0] += math.cos(direction * math.pi / 4) * self.speed
        self.location[1] += math.sin(direction * math.pi / 4) * self.speed
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
        
        