import sys
sys.path.append("../server")

from draw import draw_bg, draw_waypoints, draw_walls, draw_hero, draw_units, draw_bullets, draw_letterbox
from character import Character
from transform import Transform
from util import dist

class ClientCommander(Character):
    def __init__(self, screen, server_commander):
        super(Character, self).__init__()
        self.screen = screen
        self.t = Transform(screen, (0, 100, 0, 100))
        self.server_commander = server_commander

    def key_control(self, key, event):
        Character.key_control(self, key, event)
        # Custom comamnder control

    def mouse_control(self, mouse_pos):
        pass

    def click_control(self, mouse_pos, button):
        removed = False
        wp = self.t.inv_transform_coord(mouse_pos)
        for waypoint in self.server_commander.waypoints:
            if dist(waypoint[0], waypoint[1], wp[0], wp[1]) < 0.25:
                self.server_commander.rmwp(waypoint[0], waypoint[1])
                removed = True
                break
        if not removed:
            self.server_commander.addwp(wp[0], wp[1])

    def update(self, game_map):
        pass

    def draw(self, game_map):
        self.t.update_viewport((0, game_map.rows, 0, game_map.cols))
        draw_bg(self.screen, self.t)
        draw_walls(self.screen, self.t, game_map)
        draw_hero(self.screen, self.t, game_map)
        draw_units(self.screen, self.t, game_map)
        draw_bullets(self.screen, self.t, game_map)
        draw_waypoints(self.screen, self.t, game_map)
        draw_letterbox(self.screen, self.t)
