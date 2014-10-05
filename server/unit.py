import math

from util import dist, incline
from bullet import Bullet
import random

class Unit:
    CHARACTER_RADIUS = 0.25
    CHARACTER_BORDER = 0.10
    def __init__(self, hp, x, y, th, mode = 1):
        self.location = [x, y]
        self.hp = hp
        self.orientation = th 
        self.cd = 0
        self.radius = 0.3
        self.speed = 0.015
        self.mode = mode # 0 if allied, 1 or 2 otherwise
        if mode != 0:
            mode = random.randint(1, 2)
        if mode == 2:
            self.speed = 0.035
        self.state = 0

    def dictify(self):
        return {"type": "unit",
                "location": self.location,
                "hp": self.hp,
                "orientation": self.orientation,
                "radius": self.radius,
                "speed": self.speed,
                "mode": self.mode}

    @classmethod
    def from_dict(cls, d):
        return cls(d["hp"], d["location"][0], d["location"][1],
                   d["orientation"], d["mode"])

    def update_from_dict(self, d):
        self.hp = d["hp"]
        self.location = d["location"]
        self.orientation = d["orientation"]
        self.mode = d["mode"]
    
    def make_bullet(self, gmap):
        bdam = 1
        bspd = 0.05
        brad = 0.06 # radius
        targetx, targety = self.location
        targetx += (self.radius + brad) * math.cos(self.orientation)
        targety -= (self.radius + brad) * math.sin(self.orientation)
        if gmap.walls[int(targetx)][int(targety)] == 0: # can't make a bullet in a wall
            return Bullet(bdam, targetx, targety, math.cos(self.orientation) * bspd, -math.sin(self.orientation) * bspd, brad)
        return None
        # maybe later: don't allow bullets to be made that overlap with the walls
    
    def ai(self, game_map):
        hero = game_map.hero
        if self.mode == 0:
            if len(game_map.commander.waypoints) == 0:
                return
            self.turn((incline(self.location[0], self.location[1], game_map.commander.waypoints[len(game_map.commander.waypoints) - 1][0], game_map.commander.waypoints[len(game_map.commander.waypoints) - 1][1]) - self.orientation))
            self.move(int((self.orientation + 2 * math.pi) / (math.pi / 4)), game_map)
        if self.mode == 1:
            self.turn((incline(self.location[0], self.location[1], hero.location[0], hero.location[1]) - self.orientation) * 1.2)
            if self.state % 12 == 0: self.fire(game_map)
            self.move(int((self.orientation + 2 * math.pi) / (math.pi / 4)), game_map)
            self.state += 1
        if self.mode >= 2:
            self.turn((incline(self.location[0], self.location[1], hero.location[0], hero.location[1]) - self.orientation) * 1.2)
            if self.state % 30 == 0: self.fire(game_map)
            self.move(int((self.orientation + 2 * math.pi) / (math.pi / 4)), game_map)
            self.state += 1
        
    
    def turn(self, angle):
        self.orientation += angle
        self.orientation = self.orientation
        while self.orientation < -math.pi:
            self.orientation += 2 * math.pi
        while self.orientation > math.pi:
            self.orientation -= 2 * math.pi
    
    def fire(self, gmap):
        b = self.make_bullet(gmap)
        if b is not None: gmap.bullets.append(b)
    
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
            for person in gmap.units + [gmap.hero]:
                if person.location[0] != self.location[0] or person.location[1] != self.location[1]:
                    distp = dist(person.location[0], person.location[1], self.location[0], self.location[1])
                    if distp < self.radius + person.radius:
                        self.location[0] += (self.location[0] - person.location[0]) * ((self.radius + person.radius)/ distp - 1)
                        self.location[1] += (self.location[1] - person.location[1]) * ((self.radius + person.radius)/ distp - 1)
                        newcycles = cycles + 1
        if cycles == 100: # Wow, you broke it!
            self.location = [oldx, oldy] # Movement rejected.
            
        return self.location != [oldx, oldy]
        
        
