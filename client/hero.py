import pygame

from character import Character
from transform import Transform

class Hero(Character):
    CHARACTER_RADIUS = 0.25
    CHARACTER_BORDER = 0.10
    def __init__(self, screen):
        """
        screen: PyGame Surface object.
        t: Transform object to convert game coords to screen coords.
        """
        super(Character, self).__init__()
        self.screen = screen
        self.t = Transform(screen, (-10, 10, -10, 10))

    def control(self, key):
        Character.control(self, key)
        # Add hero control here

    def draw(self):
        self.screen.fill((230, 230, 230))

        # Border
        pygame.draw.circle(self.screen, (100, 0.0, 0.0), 
                           self.t.transform_coord((0.0, 0.0)),
                           self.t.transform_width(Hero.CHARACTER_RADIUS
                                                  + Hero.CHARACTER_BORDER),
                           0)
        # Fill
        pygame.draw.circle(self.screen, (200, 0.0, 0.0), 
                           self.t.transform_coord((0.0, 0.0)),
                           self.t.transform_width(Hero.CHARACTER_RADIUS),
                           0)
