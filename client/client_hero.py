import math, pygame, sys

from character import Character
from transform import Transform

class ClientHero(Character):
    CHARACTER_RADIUS = 0.25
    CHARACTER_BORDER = 0.10
    VIEW_SQ_RADIUS = 5.0
    def __init__(self, screen, server_hero):
        """
        screen: PyGame Surface object.
        t: Transform object to convert game coords to screen coords.
        server_hero: Temp reference to server hero object...
        """
        super(Character, self).__init__()
        self.screen = screen
        self.t = Transform(screen, (0, ClientHero.VIEW_SQ_RADIUS*2,
                                    0, ClientHero.VIEW_SQ_RADIUS*2))
        self.server_hero = server_hero
        self.loc = (server_hero.location[0], server_hero.location[1])
        self.orientation = server_hero.orientation
        self.vel = (0, 0)

    def key_control(self, key, event):
        Character.key_control(self, key, event)
        # Custom hero control
        if (key == pygame.K_w):
            if event == pygame.KEYDOWN:
                self.vel = (self.vel[0], self.vel[1]-1)
            elif event == pygame.KEYUP:
                self.vel = (self.vel[0], self.vel[1]+1)
        elif (key == pygame.K_s):
            if event == pygame.KEYDOWN:
                self.vel = (self.vel[0], self.vel[1]+1)
            elif event == pygame.KEYUP:
                self.vel = (self.vel[0], self.vel[1]-1)
        elif (key == pygame.K_a):
            if event == pygame.KEYDOWN:
                self.vel = (self.vel[0]-1, self.vel[1])
            elif event == pygame.KEYUP:
                self.vel = (self.vel[0]+1, self.vel[1])
        elif (key == pygame.K_d):
            if event == pygame.KEYDOWN:
                self.vel = (self.vel[0]+1, self.vel[1])
            elif event == pygame.KEYUP:
                self.vel = (self.vel[0]-1, self.vel[1])

    def mouse_control(self, mouse_pos):
        # Mouse control assumes character is in the center of the screen
        delta_x = mouse_pos[0] - (self.screen.get_width()/2.0)
        delta_y = mouse_pos[1] - (self.screen.get_height()/2.0)
        self.orientation = math.atan2(-delta_y, delta_x)

    def update(self, game_map):
        # Set direction
        if self.vel == (1, 0):
            direction = 0
        elif self.vel == (1, -1):
            direction = 1
        elif self.vel == (0, -1):
            direction = 2
        elif self.vel == (-1, -1):
            direction = 3
        elif self.vel == (-1, 0):
            direction = 4
        elif self.vel == (-1, 1):
            direction = 5
        elif self.vel == (0, 1):
            direction = 6
        elif self.vel == (1, 1):
            direction = 7
        else:
            direction = -1
        self.server_hero.move(direction, game_map)
        self.loc = (self.server_hero.location[0], self.server_hero.location[1])

    def draw(self, game_map):
        self.t.update_viewport((self.loc[1] - ClientHero.VIEW_SQ_RADIUS,
                                self.loc[1] + ClientHero.VIEW_SQ_RADIUS,
                                self.loc[0] - ClientHero.VIEW_SQ_RADIUS,
                                self.loc[0] + ClientHero.VIEW_SQ_RADIUS))
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

        # Character border
        pygame.draw.circle(self.screen, (100, 0, 0), 
                           self.t.transform_coord(self.loc),
                           self.t.transform_width(ClientHero.CHARACTER_RADIUS
                                                  + ClientHero.CHARACTER_BORDER),
                           0)
        # Character fill
        pygame.draw.circle(self.screen, (200, 0, 0), 
                           self.t.transform_coord(self.loc),
                           self.t.transform_width(ClientHero.CHARACTER_RADIUS),
                           0)
        # Character orientation
        orient_delta_x = math.cos(self.orientation)*ClientHero.CHARACTER_RADIUS
        orient_delta_y = -math.sin(self.orientation)*ClientHero.CHARACTER_RADIUS
        pygame.draw.line(self.screen, (100, 0, 0),
                         self.t.transform_coord(self.loc),
                         self.t.transform_coord((self.loc[0]+orient_delta_x,
                                                 self.loc[1]+orient_delta_y)), 3)

        # Draw units
        for unit in game_map.people:
            # Skip the hero
            if isinstance(unit, ClientHero): continue
            # Unit border
            pygame.draw.circle(self.screen, (0, 100, 100), 
                               self.t.transform_coord(unit.location),
                               self.t.transform_width(ClientHero.CHARACTER_RADIUS
                                                      + ClientHero.CHARACTER_BORDER),
                               0)
            # Unit fill
            pygame.draw.circle(self.screen, (0, 200, 200), 
                               self.t.transform_coord(unit.location),
                               self.t.transform_width(ClientHero.CHARACTER_RADIUS),
                               0)
            # Unit orientation
            orient_delta_x = math.cos(unit.orientation)*ClientHero.CHARACTER_RADIUS
            orient_delta_y = -math.sin(unit.orientation)*ClientHero.CHARACTER_RADIUS
            pygame.draw.line(self.screen, (0, 100, 100),
                             self.t.transform_coord(unit.location),
                             self.t.transform_coord((unit.location[0]+orient_delta_x,
                                                     unit.location[1]+orient_delta_y)), 3)

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
