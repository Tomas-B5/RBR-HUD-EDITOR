from Point import Point2D

class Dash_Object():
    name = ""
    hide = False
    # If group is not 0 then it is part of some group in the GUI
    group = 0

    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name

    def Up(self, step):
        return 0

    def Down(self, step):
        return 0

    def Left(self, step):
        return 0

    def Right(self, step):
        return 0
    
    def ScaleX(self, value):
        return 0
        
    def ScaleY(self, value):
        return 0


class Group(Dash_Object):
    children = 0
    
    def __init__(self, name):
        self.name = name
        #If its declared in the class it is shared with all instances of the class -_-
        self.children = {}
        
    def __str__(self):
        return "    " + self.name

    def Up(self, step):
        for o in self.children:
            self.children[o].Up(step)

    def Down(self, step):
        for o in self.children:
            self.children[o].Down(step)

    def Left(self, step):
        for o in self.children:
            self.children[o].Left(step)

    def Right(self, step):
        for o in self.children:
            self.children[o].Right(step)


class Simple(Dash_Object):
    Position = Point2D(-1000, -1000)
    hide = False
    # Limit_min = -9999
    # Limit_Max = 9999

    def __init__(self, name, pos):
        self.name = name
        self.Position = pos
        
    def __str__(self):
        return "{0} - [{1}][{2}]".format(self.name, self.Position.x, self.Position.y)

    def Up(self, step):
        self.Position.y -= step
        return 0

    def Down(self, step):
        self.Position.y += step
        return 0

    def Left(self, step):
        self.Position.x -= step
        return 0

    def Right(self, step):
        self.Position.x += step
        return 0
    
    def ScaleX(self, value):
        self.Position.x *= value
        
    def ScaleY(self, value):
        self.Position.y *= value


class Alpha(Dash_Object):
    Alpha = 1.0

    def __init__(self, name, alpha):
        self.name = name
        self.Alpha = alpha