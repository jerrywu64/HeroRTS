# (x, y) are measured from the top left.
class Commander:
        
    def __init__(self): 
        self.waypoints = [] # The hero's waypoints

    def addwp(self, x, y):
        self.waypoints.append([x, y])

    def rmwp(self, x, y):
        if self.waypoints.count([x, y]) > 0:
            self.waypoints.remove([x, y])

    