import pygame, sys

from character import Character
from transform import Transform

class Hero(Character):
    CHARACTER_RADIUS = 0.25
    CHARACTER_BORDER = 0.10
    VIEW_SQ_RADIUS = 5.0
    def __init__(self, screen):
        """
        screen: PyGame Surface object.
        t: Transform object to convert game coords to screen coords.
        """
        super(Character, self).__init__()
        self.screen = screen
        self.t = Transform(screen, (0, Hero.VIEW_SQ_RADIUS*2,
                                    0, Hero.VIEW_SQ_RADIUS*2))
        self.loc = (11.0, 11.0)
        self.vel = (0.0, 0.0)

    def control(self, key, event):
        Character.control(self, key, event)
        # Custom hero control
        if (key == pygame.K_w):
            if event == pygame.KEYDOWN:
                self.vel = (self.vel[0], self.vel[1]-0.1)
            elif event == pygame.KEYUP:
                self.vel = (self.vel[0], self.vel[1]+0.1)
        elif (key == pygame.K_s):
            if event == pygame.KEYDOWN:
                self.vel = (self.vel[0], self.vel[1]+0.1)
            elif event == pygame.KEYUP:
                self.vel = (self.vel[0], self.vel[1]-0.1)
        elif (key == pygame.K_a):
            if event == pygame.KEYDOWN:
                self.vel = (self.vel[0]-0.1, self.vel[1])
            elif event == pygame.KEYUP:
                self.vel = (self.vel[0]+0.1, self.vel[1])
        elif (key == pygame.K_d):
            if event == pygame.KEYDOWN:
                self.vel = (self.vel[0]+0.1, self.vel[1])
            elif event == pygame.KEYUP:
                self.vel = (self.vel[0]-0.1, self.vel[1])

    def update(self):
        self.loc = (self.loc[0]+self.vel[0], self.loc[1]+self.vel[1])

    def draw(self, game_map):
        self.t.update_viewport((self.loc[1] - Hero.VIEW_SQ_RADIUS,
                                self.loc[1] + Hero.VIEW_SQ_RADIUS,
                                self.loc[0] - Hero.VIEW_SQ_RADIUS,
                                self.loc[0] + Hero.VIEW_SQ_RADIUS))
        self.screen.fill((230, 230, 230),
                         pygame.Rect(self.t.surface_width_offset(),
                                     self.t.surface_height_offset(),
                                     self.t.surface_real_width(),
                                     self.t.surface_real_height()))

        # Draw map
        pygame.draw.rect(self.screen, (180, 180, 180),
                         pygame.Rect(
                             self.t.transform_coord((0,0)),
                             (self.t.transform_width(len(game_map.walls)),
                              self.t.transform_height(len(game_map.walls[0])))))
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
                           self.t.transform_coord(self.loc),
                           self.t.transform_width(Hero.CHARACTER_RADIUS
                                                  + Hero.CHARACTER_BORDER),
                           0)
        # Fill
        pygame.draw.circle(self.screen, (200, 0, 0), 
                           self.t.transform_coord(self.loc),
                           self.t.transform_width(Hero.CHARACTER_RADIUS),
                           0)

        # Letterbox - left
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect(0, 0,
                                     self.t.surface_width_offset(),
                                     self.screen.get_height()))
        # Letterbox - right
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect(self.screen.get_width() - self.t.surface_width_offset(), 0,
                                     self.t.surface_width_offset(),
                                     self.screen.get_height()))
        # Letterbox - top
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect(0, 0,
                                     self.screen.get_width(),
                                     self.t.surface_height_offset()))
        # Letterbox - bottom
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect(0, self.screen.get_height() - self.t.surface_height_offset(),
                                     self.screen.get_width(),
                                     self.t.surface_height_offset()))
