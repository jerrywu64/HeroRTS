import math

from bullet import Bullet
from util import dist

class Hero:
    CHARACTER_RADIUS = 0.25
    CHARACTER_BORDER = 0.10
    def __init__(self, hp, x, y, th, dead=False):  # the commander screen's start coordinates (top left?) and orientation
        self.location = [x, y]
        self.hp = hp
        self.orientation = th # Positive-x-axis, going ccw, in range [0, 2pi).
        self.cd = 0
        self.fov_angle = 1 # Angle from center, in radians, that the hero can 
            # see. This means that the central angle of the cone of the hero's
            # vision is 2 * fov_angle.
        self.fov_radius = 5
        self.radius = 0.3 # The hero is a circle?
        self.speed = 0.04 # squares per tick
        self.dead = dead

    def dictify(self):
        return {"type": "hero",
                "location": self.location,
                "hp": self.hp,
                "orientation": self.orientation,
                "fov_angle": self.fov_angle,
                "fov_radius": self.fov_radius,
                "radius": self.radius,
                "speed": self.speed,
                "dead": self.dead}

    @classmethod
    def from_dict(cls, d):
        return cls(d["hp"], d["location"][0], d["location"][1],
                   d["orientation"], d["dead"])

    def update_from_dict(self, d):
        self.hp = d["hp"]
        self.location = d["location"]
        self.orientation = d["orientation"]
        self.dead = d["dead"]

    def visible(self, x, y, gmap):  # returns if the grid-square (x, y) is visible.
        # Check if the point is in the field of view:
        xoff = x+0.5
        yoff = y+0.5
        if dist(xoff, yoff, self.location[0], self.location[1]) > self.fov_radius:
            return False
        if dist(xoff, yoff, self.location[0], self.location[1]) < 1:
            return True
        angle = self.orientation
        if xoff == self.location[0]:
            if yoff > self.location[1]:
                angle -= 3 * math.pi / 2
            else:
                angle -= math.pi / 2
        else:
            angle -= math.atan2(self.location[1] - yoff, xoff - self.location[0])
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        if math.fabs(angle) > self.fov_angle:
            return False
        # Check if there's a wall in the way:
        # curloc = self.location
        # Never mind, we'll do this later maybe. If it's a wall, though:
        if gmap.walls[x][y] == 1:
            return True
        return True
        
    def make_bullet(self, gmap):
        bdam = 2
        bspd = 0.05
        brad = 0.06 # radius
        targetx, targety = self.location
        targetx += (self.radius + brad) * math.cos(self.orientation)
        targety -= (self.radius + brad) * math.sin(self.orientation)
        if gmap.walls[int(targetx)][int(targety)] == 0: # can't make a bullet in a wall
            return Bullet(bdam, targetx, targety, math.cos(self.orientation) * bspd, -math.sin(self.orientation) * bspd, brad)
        # maybe later: don't allow bullets to be made that overlap with the walls
    
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
            for person in gmap.units:
                if person.location[0] != self.location[0] or person.location[1] != self.location[1]:
                    distp = dist(person.location[0], person.location[1], self.location[0], self.location[1])
                    if distp < self.radius + person.radius:
                        self.location[0] += (self.location[0] - person.location[0]) * ((self.radius + person.radius)/ distp - 1)
                        self.location[1] += (self.location[1] - person.location[1]) * ((self.radius + person.radius)/ distp - 1)
                        newcycles = cycles + 1
        if cycles == 100: # Wow, you broke it!
            self.location = [oldx, oldy] # Movement rejected.
            
        return self.location != [oldx, oldy]
            
