import math, pygame

def draw_bg(screen, t):
    screen.fill((230, 230, 230),
                pygame.Rect(t.surface_width_offset(),
                            t.surface_height_offset(),
                            t.surface_real_width(),
                            t.surface_real_height()))

def draw_walls(screen, t, game_map):
    """
    screen: PyGame surface
    t: Transform
    game_map: Game map info
    """
    # Draw map
    pygame.draw.rect(screen, (180, 180, 180),
                     pygame.Rect(
                         t.transform_coord((0,0)),
                         (t.transform_width(len(game_map.walls)),
                          t.transform_height(len(game_map.walls[0])))))
    for i, col in enumerate(game_map.walls):
        for j, wall in enumerate(col):
            if wall == 0: continue
            pygame.draw.rect(screen, (50, 50, 50),
                             pygame.Rect(
                                 t.transform_coord((i, j)),
                                 (t.transform_width(1),
                                  t.transform_height(1))))
            pygame.draw.rect(screen, (30, 30, 30),
                             pygame.Rect(
                                 t.transform_coord((i, j)),
                                 (t.transform_width(1),
                                  t.transform_height(1))), 3)


def draw_hero(screen, t, game_map):
    """
    screen: PyGame surface
    t: Transform
    game_map: PyGame map
    """
    hero = game_map.hero
    # Character border
    pygame.draw.circle(screen, (100, 0, 0), 
                       t.transform_coord(hero.location),
                       t.transform_width(hero.CHARACTER_RADIUS
                                         + hero.CHARACTER_BORDER),
                       0)
    # Character fill
    pygame.draw.circle(screen, (200, 0, 0), 
                       t.transform_coord(hero.location),
                       t.transform_width(hero.CHARACTER_RADIUS),
                       0)
    # Character orientation
    orient_delta_x = math.cos(hero.orientation)*hero.CHARACTER_RADIUS
    orient_delta_y = -math.sin(hero.orientation)*hero.CHARACTER_RADIUS
    pygame.draw.line(screen, (100, 0, 0),
                     t.transform_coord(hero.location),
                     t.transform_coord((hero.location[0]+orient_delta_x,
                                        hero.location[1]+orient_delta_y)), 3)

COLOR_MAP = {
    0: ((0, 100, 100), (0, 200, 200)),
    1: ((200, 50, 0), (255, 60, 0)),
    2: ((75, 0, 50), (50, 0, 25))
}
def draw_units(screen, t, game_map):
    """
    screen: PyGame surface
    t: Transform
    game_map: Game map info
    """
    # Draw units
    for unit in game_map.units:
        # Unit border
        pygame.draw.circle(screen, COLOR_MAP[unit.type][0], 
                           t.transform_coord(unit.location),
                           t.transform_width(unit.CHARACTER_RADIUS
                                             + unit.CHARACTER_BORDER),
                           0)
        # Unit fill
        pygame.draw.circle(screen, COLOR_MAP[unit.type][1], 
                           t.transform_coord(unit.location),
                           t.transform_width(unit.CHARACTER_RADIUS),
                           0)
        # Unit orientation
        orient_delta_x = math.cos(unit.orientation)*unit.CHARACTER_RADIUS
        orient_delta_y = -math.sin(unit.orientation)*unit.CHARACTER_RADIUS
        pygame.draw.line(screen, COLOR_MAP[unit.type][0],
                         t.transform_coord(unit.location),
                         t.transform_coord((unit.location[0]+orient_delta_x,
                                            unit.location[1]+orient_delta_y)), 3)

WAYPOINT_SIZE = 0.25
def draw_waypoints(screen, t, game_map):
    """
    screen: PyGame surface
    t: Transform
    game_map: Game map info
    """
    for waypoint in game_map.commander.waypoints:
        pygame.draw.line(screen, (200, 150, 0),
                         t.transform_coord((waypoint[0]-WAYPOINT_SIZE, waypoint[1]-WAYPOINT_SIZE)),
                         t.transform_coord((waypoint[0]+WAYPOINT_SIZE, waypoint[1]+WAYPOINT_SIZE)), 7)
        pygame.draw.line(screen, (200, 150, 0),
                         t.transform_coord((waypoint[0]-WAYPOINT_SIZE, waypoint[1]+WAYPOINT_SIZE)),
                         t.transform_coord((waypoint[0]+WAYPOINT_SIZE, waypoint[1]-WAYPOINT_SIZE)), 7)

def draw_bullets(screen, t, game_map):
    """
    screen: PyGame surface
    t: Transform
    game_map: Game map info
    """
    # print len(game_map.bullets)
    # Draw units
    for b in game_map.bullets:
        # Unit fill
        pygame.draw.circle(screen, (b.damage*15, 15, 15),
                           t.transform_coord(b.location),
                           t.transform_width(b.radius),
                           0)

def draw_letterbox(screen, t):
    """
    screen: PyGame surface
    t: Transform
    """
    # Letterbox - left
    pygame.draw.rect(screen, (0, 0, 0),
                     pygame.Rect(0, 0,
                                 t.surface_width_offset(),
                                 screen.get_height()))
    # Letterbox - right
    pygame.draw.rect(screen, (0, 0, 0),
                     pygame.Rect(screen.get_width() - t.surface_width_offset(), 0,
                                 t.surface_width_offset(),
                                 screen.get_height()))
    # Letterbox - top
    pygame.draw.rect(screen, (0, 0, 0),
                     pygame.Rect(0, 0,
                                 screen.get_width(),
                                 t.surface_height_offset()))
    # Letterbox - bottom
    pygame.draw.rect(screen, (0, 0, 0),
                     pygame.Rect(0, screen.get_height() - t.surface_height_offset(),
                                 screen.get_width(),
                                 t.surface_height_offset()))
