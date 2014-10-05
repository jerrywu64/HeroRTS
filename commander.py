# (x, y) are measured from the top left.

waypoints = [] # The hero's waypoints

location = [0, 0]
orientation = 0 # Positive-x-axis, going ccw, in range [0, 2pi).
fov_angle = 1 # Angle from center, in radians, that the hero can 
    # see. This means that the central angle of the cone of the hero's
    # vision is 2 * fov_angle.
fov_radius = 10
radius = 0.3 # The hero is a circle?
    
def init(x, y, th):  # the hero's start coordinates and orientation
    location = [x, y]
    orientation = th

def addwp(x, y):
    waypoints.append([x, y])

def rmwp(x, y):
    if waypoints.count([x, y]) > 0:
        waypoints.remove([x, y])

def visible(x, y, map):  # returns if the grid-square (x, y) is visible.
    # Check if the point is in the field of view:
    if math.sqrt((x - location[0]) * (x - location[0]) + (y - location[1]) * (y - location[1])) > fov_radius:
        return False
    angle = orientation
    if x == location[0]:
        if y > location[1]:
            angle -= math.pi / 2
        else:
            angle -= 3 * math.pi / 2
    else:
        angle -= math.atan(location[1] - y,x - location[0])
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    if math.fabs(angle) > fov_angle:
        return false
    # Check if there's a wall in the way:
    curloc = location
    