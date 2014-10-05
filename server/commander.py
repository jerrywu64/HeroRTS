# (x, y) are measured from the top left.
class Commander:
        
    def __init__(self, waypoints=[]): 
        self.waypoints = waypoints # The hero's waypoints
        self.pathfinders = {} # a dict of pathfinders

    def dictify(self):
        return {"waypoints": self.waypoints}

    @classmethod
    def from_dict(cls, d):
        return cls(d["waypoints"])

    def update_from_dict(self, d):
        self.waypoints = d["waypoints"]

    def addwp(self, x, y):
        self.waypoints.append([x, y])

    def rmwp(self, x, y):
        if self.waypoints.count([x, y]) > 0:
            self.waypoints.remove([x, y])
            

    
