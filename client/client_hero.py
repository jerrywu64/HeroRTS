import math, pygame, sys
sys.path.append("../server")

from draw import draw_bg, draw_walls, draw_hero, draw_units, draw_bullets, draw_letterbox
from hero import Hero
from character import Character
from transform import Transform

class ClientHero(Character):
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
        self.vel = (0, 0)
        self.firing = False
        self.fired = False
        self.font = pygame.font.SysFont("monospace", 24)

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
        self.server_hero.orientation = math.atan2(-delta_y, delta_x)

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

        if self.firing:
            self.firing = False
            self.fired = True
            b = self.server_hero.make_bullet(game_map)
            if b is not None: game_map.bullets.append(b)

    def draw(self, game_map):
        print len(game_map.bullets)
        if self.server_hero.dead:
            # Death!!
            self.screen.fill((230, 0, 0))
            label = self.font.render("Whoops. Ate too many bullets. Nom.", 1, (100, 0, 0))
            self.screen.blit(label, ((self.screen.get_width()-label.get_width())/2.0,
                                     self.screen.get_height()/2.0))
            return

        self.t.update_viewport((self.server_hero.location[1] - ClientHero.VIEW_SQ_RADIUS,
                                self.server_hero.location[1] + ClientHero.VIEW_SQ_RADIUS,
                                self.server_hero.location[0] - ClientHero.VIEW_SQ_RADIUS,
                                self.server_hero.location[0] + ClientHero.VIEW_SQ_RADIUS))
        draw_bg(self.screen, self.t)
        draw_walls(self.screen, self.t, game_map)
        draw_hero(self.screen, self.t, game_map)
        draw_units(self.screen, self.t, game_map)
        draw_bullets(self.screen, self.t, game_map)
        draw_letterbox(self.screen, self.t)
