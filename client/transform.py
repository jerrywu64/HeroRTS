# Display transformation
class Transform(object):
    def __init__(self, surface, viewport):
        """
        surface: PyGame Surface object.
        viewport: Tuple of (top, bottom, left, right) in game coords.
        """
        self.surface = surface
        self.viewport = viewport

    def update_viewport(self, viewport):
        self.viewport = viewport

    def transform_coord(self, coord):
        """
        Transform the given game coordinate into screen coords.
        """
        delta_x = coord[0] - self.viewport[2] # x - left
        delta_y = coord[1] - self.viewport[0] # y - top
        game_width = self.viewport[3] - self.viewport[2] # right - left
        game_height = self.viewport[1] - self.viewport[0] # bottom - top
        return (int((delta_x / float(game_width))*self.surface.get_width()),
                int((delta_y / float(game_height))*self.surface.get_height()))

    def transform_width(self, width):
        game_width = self.viewport[3] - self.viewport[2]
        return int((width/float(game_width))*self.surface.get_width())

    def transform_height(self, height):
        game_height = self.viewport[1] - self.viewport[0]
        return int((height/float(game_height))*self.surface.get_height())
