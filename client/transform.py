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

    # Implement letterboxing by scaling using "real" width and height, then
    # adding letterboxing offsets
    def surface_real_width(self):
        game_width = self.viewport[3] - self.viewport[2] # right - left
        game_height = self.viewport[1] - self.viewport[0] # bottom - top
        screen_width = self.surface.get_width()
        screen_height = self.surface.get_height()
        # Game aspect ratio is more width-ful than screen -- letterbox height
        if (game_width/float(game_height)) >= (screen_width/float(screen_height)):
            return screen_width
        # Letterbox width
        else:
            return (game_width/float(game_height))*screen_height
    def surface_real_height(self):
        game_width = self.viewport[3] - self.viewport[2] # right - left
        game_height = self.viewport[1] - self.viewport[0] # bottom - top
        screen_width = self.surface.get_width()
        screen_height = self.surface.get_height()
        # Game aspect ratio is more width-ful than screen -- letterbox height
        if (game_width/float(game_height)) >= (screen_width/float(screen_height)):
            return (game_height/float(game_width))*screen_width
        # Letterbox width
        else:
            return screen_height
    def surface_width_offset(self):
        return (self.surface.get_width() - self.surface_real_width())/2.0
    def surface_height_offset(self):
        return (self.surface.get_height() - self.surface_real_height())/2.0

    def transform_coord(self, coord):
        """
        Transform the given game coordinate into screen coords.
        """
        delta_x = coord[0] - self.viewport[2] # x - left
        delta_y = coord[1] - self.viewport[0] # y - top
        game_width = self.viewport[3] - self.viewport[2] # right - left
        game_height = self.viewport[1] - self.viewport[0] # bottom - top
        return (int((delta_x / float(game_width))*self.surface_real_width()
                    + self.surface_width_offset()),
                int((delta_y / float(game_height))*self.surface_real_height()
                    + self.surface_height_offset()))

    def inv_transform_coord(self, screen_coord):
        """
        Transform the given screen coord into game coords.
        """
        game_width = self.viewport[3] - self.viewport[2] # right - left
        game_height = self.viewport[1] - self.viewport[0] # bottom - top
        delta_x = ((screen_coord[0] - self.surface_width_offset())/
                   self.surface_real_width()*(game_width))
        delta_y = ((screen_coord[1] - self.surface_height_offset())/
                   self.surface_real_height()*(game_height))
        return (delta_x + self.viewport[2], delta_y + self.viewport[0])
        

    def transform_width(self, width):
        game_width = self.viewport[3] - self.viewport[2]
        return int((width/float(game_width))*self.surface_real_width())

    def transform_height(self, height):
        game_height = self.viewport[1] - self.viewport[0]
        return int((height/float(game_height))*self.surface_real_height())
