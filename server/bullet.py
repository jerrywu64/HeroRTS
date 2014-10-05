import math

from util import dist
class Bullet:
    def __init__(self, damage, x, y, velx, vely, radius = 0.06, bounces = 3):
        # Speed should always be lower than radius, lest bad things happen.
        self.damage = damage
        self.location = [x, y]
        self.velocity = [velx, vely] # units per tick
        self.radius = radius
        self.bounces = bounces

    def dictify(self):
        return {"damage": self.damage,
                "location": self.location,
                "velocity": self.velocity,
                "radius": self.radius,
                "bounces": self.bounces}

    @classmethod
    def from_dict(cls, d):
        return cls(d["damage"], d["location"][0], d["location"][1],
                   d["velocity"][0], d["velocity"][1], d["radius"], d["bounces"])

    def update_from_dict(self, d):
        self.damage = d["damage"]
        self.location = d["location"]
        self.velocity = d["velocity"]
        self.radius = d["radius"]
        self.bounces = d["bounces"]
        
    # Returns the index (in gmap.units) of person collided with, or -1 for hero, or False if didn't hit anyone.
    def move(self, gmap):
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        fracx, floorx = math.modf(self.location[0])
        fracy, floory = math.modf(self.location[1])
        ifloorx = int(floorx)
        ifloory = int(floory)
        # Wall collisions (Adjustments are doubled since it's a reflection)
        if fracx < self.radius: # Into left square
            if gmap.walls[ifloorx - 1][ifloory] == 1:
                self.location[0] += 2 * (self.radius - fracx)
                self.velocity[0] *= -1
        if 1 - fracx < self.radius: # Into right square
            if gmap.walls[ifloorx + 1][ifloory] == 1:
                self.location[0] -= 2 * (self.radius + fracx - 1)
                self.velocity[0] *= -1
        if fracy < self.radius: # Into top square
            if gmap.walls[ifloorx][ifloory - 1] == 1:
                self.location[1] += 2 * (self.radius - fracy)
                self.velocity[1] *= -1
        if 1 - fracy < self.radius: # Into bottom square
            if gmap.walls[ifloorx][ifloory + 1] == 1:
                self.location[1] -= 2 * (self.radius + fracy - 1)
                self.velocity[1] *= -1
        # Corner collisions (oh jeez)
        # Okay, this is going to be an approximation. The bullet will be pushed away
        # the same way that units are.
        d = dist(floorx, floory, self.location[0], self.location[1])
        if d < self.radius and gmap.walls[ifloorx-1][ifloory-1]:
            self.location[0] += fracx * (self.radius / d - 1)
            self.location[1] += fracy * (self.radius / d - 1)
            spd = math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])
            normal = math.atan2(self.location[1] - floory, self.location[0] - floorx)
            vangle = math.atan2(-self.velocity[1], -self.velocity[0])
            self.velocity[0] = spd * math.cos(2 * normal - vangle)
            self.velocity[1] = spd * math.sin(2 * normal - vangle)
        d = dist(floorx + 1, floory, self.location[0], self.location[1])
        if d < self.radius and gmap.walls[ifloorx+1][ifloory-1]:
            self.location[0] -= (1 - fracx) * (self.radius / d - 1)
            self.location[1] += fracy * (self.radius / d - 1)
            spd = math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])
            normal = math.atan2(self.location[1] - floory, self.location[0] - (floorx + 1))
            vangle = math.atan2(-self.velocity[1], -self.velocity[0])
            self.velocity[0] = spd * math.cos(2 * normal - vangle)
            self.velocity[1] = spd * math.sin(2 * normal - vangle)
        d = dist(floorx, floory + 1, self.location[0], self.location[1])
        if d < self.radius and gmap.walls[ifloorx-1][ifloory+1]:
            self.location[0] += fracx * (self.radius / d - 1)
            self.location[1] -= (1 - fracy) * (self.radius / d - 1)
            spd = math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])
            normal = math.atan2(self.location[1] - (floory + 1), self.location[0] - floorx)
            vangle = math.atan2(-self.velocity[1], -self.velocity[0])
            self.velocity[0] = spd * math.cos(2 * normal - vangle)
            self.velocity[1] = spd * math.sin(2 * normal - vangle)
        d = dist(floorx + 1, floory + 1, self.location[0], self.location[1])
        if d < self.radius and gmap.walls[ifloorx+1][ifloory+1]:
            self.location[0] -= (1 - fracx) * (self.radius / d - 1)
            self.location[1] -= (1 - fracy) * (self.radius / d - 1)
            spd = math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])
            normal = math.atan2(self.location[1] - (floory + 1), self.location[0] - (floorx + 1))
            vangle = math.atan2(-self.velocity[1], -self.velocity[0])
            self.velocity[0] = spd * math.cos(2 * normal - vangle)
            self.velocity[1] = spd * math.sin(2 * normal - vangle)
        # Collision check, people
        for i, person in enumerate([gmap.hero] + gmap.units):
            distp = dist(person.location[0], person.location[1], self.location[0], self.location[1])
            if distp < self.radius + person.radius:
                return i-1
        return False
