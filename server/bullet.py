import math

class Bullet:
    def __init__(self, damage, x, y, velx, vely, radius = 0.06, bounces = 3):
        # Speed should always be lower than radius, lest bad things happen.
        self.damage = damage
        self.location = [x, y]
        self.velocity = [velx, vely] # units per tick
        self.radius = radius
        self.bounces = bounces
        
    # Returns the index (in gmap.units) of person collided with, or -1 for hero, or False if didn't hit anyone.
    def move(self, gmap):
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        fracx, floorx = math.modf(self.location[0])
        fracy, floory = math.modf(self.location[1])
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
            normal = math.atan(self.location[1] - floory, self.location[0] - floorx)
            vangle = math.atan(-self.velocity[1], -self.velocity[0])
            self.velocity[0] = spd * math.cos(2 * normal - vangle)
            self.velocity[1] = spd * math.sin(2 * normal - vangle)
        d = dist(floorx + 1, floory, self.location[0], self.location[1])
        if d < self.radius and gmap.walls[ifloorx+1][ifloory-1]:
            self.location[0] -= (1 - fracx) * (self.radius / d - 1)
            self.location[1] += fracy * (self.radius / d - 1)
            spd = math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])
            normal = math.atan(self.location[1] - floory, self.location[0] - (floorx + 1))
            vangle = math.atan(-self.velocity[1], -self.velocity[0])
            self.velocity[0] = spd * math.cos(2 * normal - vangle)
            self.velocity[1] = spd * math.sin(2 * normal - vangle)
        d = dist(floorx, floory + 1, self.location[0], self.location[1])
        if d < self.radius and gmap.walls[ifloorx-1][ifloory+1]:
            self.location[0] += fracx * (self.radius / d - 1)
            self.location[1] -= (1 - fracy) * (self.radius / d - 1)
            spd = math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])
            normal = math.atan(self.location[1] - (floory + 1), self.location[0] - floorx)
            vangle = math.atan(-self.velocity[1], -self.velocity[0])
            self.velocity[0] = spd * math.cos(2 * normal - vangle)
            self.velocity[1] = spd * math.sin(2 * normal - vangle)
        d = dist(floorx + 1, floory + 1, self.location[0], self.location[1])
        if d < self.radius and gmap.walls[ifloorx+1][ifloory+1]:
            self.location[0] -= (1 - fracx) * (self.radius / d - 1)
            self.location[1] -= (1 - fracy) * (self.radius / d - 1)
            spd = math.sqrt(self.velocity[0] * self.velocity[0] + self.velocity[1] * self.velocity[1])
            normal = math.atan(self.location[1] - (floory + 1), self.location[0] - (floorx + 1))
            vangle = math.atan(-self.velocity[1], -self.velocity[0])
            self.velocity[0] = spd * math.cos(2 * normal - vangle)
            self.velocity[1] = spd * math.sin(2 * normal - vangle)
        # Collision check, people
        for i, person in enumerate([gmap.hero] + gmap.units):
            distp = dist(person.location[0], person.location[1], self.location[0], self.location[1])
            if distp < self.radius + person.radius:
                return i-1
        return False
