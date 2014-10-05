import math, pygame, sys
sys.path.append("../server")

from draw import draw_walls, draw_hero, draw_units, draw_bullets, draw_letterbox
from hero import Hero
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
        self.firing = False
        self.fired = False

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
        elif (key == pygame.K_SPACE):
            if event == pygame.KEYDOWN:
                self.firing = True
            elif event == pygame.KEYUP:
                self.firing = False

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

        if self.firing:
            self.firing = False
            self.fired = True
            game_map.bullets.append(self.server_hero.make_bullet(game_map))

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

        draw_walls(self.screen, self.t, game_map)
        draw_hero(self.screen, self.t, game_map, self)
        draw_units(self.screen, self.t, game_map)
        draw_bullets(self.screen, self.t, game_map)
        draw_letterbox(self.screen, self.t)
