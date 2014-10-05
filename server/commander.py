# (x, y) are measured from the top left.
class Commander:
        
    def __init__(self, x, y, th):  # the hero's start coordinates and orientation
        self.location = [x, y]
        self.orientation = th # Positive-x-axis, going ccw, in range [0, 2pi).
        self.waypoints = [] # The hero's waypoints
        self.fov_angle = 1 # Angle from center, in radians, that the hero can 
            # see. This means that the central angle of the cone of the hero's
            # vision is 2 * fov_angle.
        self.fov_radius = 10
        self.radius = 0.3 # The hero is a circle?

    def addwp(self, x, y):
        waypoints.append([x, y])

    def rmwp(self, x, y):
        if waypoints.count([x, y]) > 0:
            waypoints.remove([x, y])

    def visible(self, x, y, map):  # returns if the grid-square (x, y) is visible.
        # Check if the point is in the field of view:
        if math.sqrt((x - self.location[0]) * (x - self.location[0]) + (y - self.location[1]) * (y - self.location[1])) > self.fov_radius:
            return False
        angle = self.orientation
        if x == self.location[0]:
            if y > self.location[1]:
                angle -= math.pi / 2
            else:
                angle -= 3 * math.pi / 2
        else:
            angle -= math.atan(self.location[1] - y,x - self.location[0])
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        if math.fabs(angle) > fov_angle:
            return false
        # Check if there's a wall in the way:
        #curloc = self.location
        # Never mind, we'll do this later maybe.
        return True