class Bullet:
    def __init__(damage, x, y, velx, vely, radius = 0.2, bounces = 3):
        self.damage = damage
        self.location = [x, y]
        self.velocity = [velx, vely] # units per tick
        self.radius = radius
        self.bounces = bounces