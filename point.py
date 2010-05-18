class Point(object):
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%f, %f)"%(self.x, self.y)
