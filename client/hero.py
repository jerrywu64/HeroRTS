import pygame, sys

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
        self.t = Transform(screen, (0, 20, 0, 20))

    def control(self, key):
        Character.control(self, key)
        # Add hero control here

    def draw(self, game_map):
        self.screen.fill((230, 230, 230))

        # Draw map
        for i, col in enumerate(game_map.walls):
            for j, wall in enumerate(col):
                if wall == 0: continue
                pygame.draw.rect(self.screen, (50, 50, 50),
                                 pygame.Rect(
                                     self.t.transform_coord((i, j)),
                                     (self.t.transform_width(1),
                                      self.t.transform_height(1))))
                pygame.draw.rect(self.screen, (30, 30, 30),
                                 pygame.Rect(
                                     self.t.transform_coord((i, j)),
                                     (self.t.transform_width(1),
                                      self.t.transform_height(1))), 3)

        # Border
        pygame.draw.circle(self.screen, (100, 0, 0), 
                           self.t.transform_coord((11.0, 11.0)),
                           self.t.transform_width(Hero.CHARACTER_RADIUS
                                                  + Hero.CHARACTER_BORDER),
                           0)
        # Fill
        pygame.draw.circle(self.screen, (200, 0, 0), 
                           self.t.transform_coord((11.0, 11.0)),
                           self.t.transform_width(Hero.CHARACTER_RADIUS),
                           0)
