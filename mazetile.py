class mazetile:
    def __init__(self,x,y,s):
        self.x = x
        self.y = y
        self.posx = x*s
        self.posy = y*s
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None

    def get_top(self):
        return self.top

    def get_bottom(self):
        return self.bottom

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right
