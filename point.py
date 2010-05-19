class Point(object):
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%f, %f)"%(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

def mean(A):
    ret = Point(0., 0.)
    for a in A:
        ret += a
    return Point(float(ret.x) / float(len(A)), float(ret.y) / float(len(A)))
