class Unit:
    def __init__(self, hp, x, y, th):
        self.location = [x, y]
        self.hp = hp
        self.orientation = th 
        self.radius = 0.3
        self.speed = 0.015
    
    def dist(x1, y1, x2, y2):
        return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
        
    # Returns True if move caused the person to actually change positions, False otherwise.
    def move(self, direction, gmap):  # direction is a number from 0 to 7, starting positive-x and going ccw, relative to your orientation.
        if direction == -1:
            return
        oldx, oldy = self.location # backing it up in case something explodes
        self.location[0] += math.cos(direction * math.pi / 4) * self.speed
        # Negative, because our coordinate system is the wrong handedness
        self.location[1] -= math.sin(direction * math.pi / 4) * self.speed
        # Collision check, orthogonal walls
        cycles = 0
        newcycles = 1
        while cycles != newcycles and cycles < 100:  # This loop is for making sure that one object doesn't push you into another, and for preventing infinite loops.
            fracx, floorx = math.modf(self.location[0])
            fracy, floory = math.modf(self.location[1])
            ifloorx = int(floorx)
            ifloory = int(floory)
            cycles = newcycles
            if fracx < self.radius: # Into left square
                if gmap.walls[ifloorx - 1][ifloory] == 1:
                    self.location[0] += self.radius - fracx
                    newcycles = cycles + 1
            if 1 - fracx < self.radius: # Into right square
                if gmap.walls[ifloorx + 1][ifloory] == 1:
                    self.location[0] -= self.radius + fracx - 1
                    newcycles = cycles + 1
            if fracy < self.radius: # Into top square
                if gmap.walls[ifloorx][ifloory - 1] == 1:
                    self.location[1] += self.radius - fracy
                    newcycles = cycles + 1
            if 1 - fracy < self.radius: # Into bottom square
                if gmap.walls[ifloorx][ifloory + 1] == 1:
                    self.location[1] -= self.radius + fracy - 1
                    newcycles = cycles + 1
            # Collision check, corners
            d = dist(floorx, floory, self.location[0], self.location[1])
            if d < self.radius and gmap.walls[ifloorx-1][ifloory-1]:
                self.location[0] += fracx * (self.radius / d - 1)
                self.location[1] += fracy * (self.radius / d - 1)
                newcycles = cycles + 1
            d = dist(floorx + 1, floory, self.location[0], self.location[1])
            if d < self.radius and gmap.walls[ifloorx+1][ifloory-1]:
                self.location[0] -= (1 - fracx) * (self.radius / d - 1)
                self.location[1] += fracy * (self.radius / d - 1)
                newcycles = cycles + 1
            d = dist(floorx, floory + 1, self.location[0], self.location[1])
            if d < self.radius and gmap.walls[ifloorx-1][ifloory+1]:
                self.location[0] += fracx * (self.radius / d - 1)
                self.location[1] -= (1 - fracy) * (self.radius / d - 1)
                newcycles = cycles + 1
            d = dist(floorx + 1, floory + 1, self.location[0], self.location[1])
            if d < self.radius and gmap.walls[ifloorx+1][ifloory+1]:
                self.location[0] -= (1 - fracx) * (self.radius / d - 1)
                self.location[1] -= (1 - fracy) * (self.radius / d - 1)
                newcycles = cycles + 1
            # Collision check, people
            for person in gmap.people:
                if person.location[0] != self.location[0] or person.location[1] != self.location[1]:
                    distp = dist(person.location[0], person.location[1], self.location[0], self.location[1])
                    if distp < self.radius + person.radius:
                        self.location[0] += (self.location[0] - person.location[0]) * ((self.radius + person.radius)/ distp - 1)
                        self.location[1] += (self.location[1] - person.location[1]) * ((self.radius + person.radius)/ distp - 1)
                        newcycles = cycles + 1
        if cycles == 100: # Wow, you broke it!
            self.location = [oldx, oldy] # Movement rejected.
            
        return self.location != [oldx, oldy]
        
        