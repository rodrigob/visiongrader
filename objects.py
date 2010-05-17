class ObjectInfos(object):
    def __init__(self):
        pass

    def bounding_box(self):
        pass

class BoundingBoxError(StandardError):
    def __init__(self):
        pass

class BoundingBox(ObjectInfos):
    def __init__(self, x, y, width = None, height = None, x2 = None, y2 = None):
        super(BoundingBox, self).__init__()
        self._x = x
        self._y = y
        self._x2 = x2
        self._y2 = y2 #TODO
        """
        if width != None:
            if x2 != None:
                print "BoundingBox : both width and x2 are set."
                raise BoundingBoxError()
            assert(width >= 0)
            self._x2 = x + width
        elif x2 != None:
            self._x = min(x, x2)
            self._x2 = max(x, x2)
        else:
            raise BoundingBoxError()
        if height != None:
            if y2 != None:
                print "BoundingBox : both height and y2 are set."
                raise BoundingBorError()
            assert(height >= 0)
            self._y2 = y + height
        elif y2 != None:
            self._y = min(y, y2)
            self._y2 = max(y, y2)
        else:
            raise BoundingBoxError()
            """
    
    def getX1(self):
        return self._x

    def getX2(self):
        return self._x2

    def getY1(self):
        return self._y

    def getY2(self):
        return self._y2

    def getHeight(self):
        return self._x2 - self._x

    def getWidth(self):
        return self._y2 - self._y

    x1 = property(getX1)
    x2 = property(getX2)
    y1 = property(getY1)
    y2 = property(getY2)
    width = property(getWidth)
    height = property(getHeight)

    def area(self):
        return self.width * self.height

    def overlap(self, other):
        return (self.x1 < other.x2 and self.x2 > other.x1 and self.y1 < other.y2 and self.y2 > other.y1)

    def overlapping_area(self, other):
        w = min(self.x2, other.x2) - max(self.x1, other.x1)
        h = min(self.y2, other.y2) - max(self.y2, other.y2)
        if (w < 0 or h < 0):
            return 0
        else:
            return w * h

    def bounding_box(self):
        return self

class PointsOnObject(ObjectInfos):
    def __init__(self):
        super(PointsOnObject, self).__init__()
        self.points = {}
        self.xmin = float("inf")
        self.xmax = float("-inf")
        self.ymin = float("inf")
        self.ymax = float("-inf")
    
    def add_point(self, name, p):
        if name in self.points:
            print "Warning : PointsOnObject.add_point : the name %s already exists."%(name,)
        self.points[name] = p
        self.xmin = min(self.xmin, p.x)
        self.xmax = max(self.xmax, p.x)
        self.ymin = min(self.ymin, p.y)
        self.ymax = max(self.ymax, p.y)

    def bounding_box(self):
        return BoundingBox(x = self.xmin, y = self.ymin,
                           x2 = self.xmax, y2 = self.ymax)

class EyesNoseMouth(PointsOnObject):
    def __init__(self, left_eye = None, right_eye = None, nose = None,
                 left_corner_mouth = None, center_mouth = None, right_corner_mouth = None):
        super(EyesNoseMouth, self).__init__()
        for name in ["left_eye", "right_eye", "nose", "left_corner_mouth",
                     "center_mouth", "right_corner_mouth"]:
            if vars()[name] != None:
                self.add_point(name, vars()[name])

    def getLeftEye(self):
        return self.points["left_eye"]

    def getRightEye(self):
        return self.points["right_eye"]

    def getNose(self):
        return self.points["nose"]

    def getLeftCornerMouth(self):
        return self.points["left_corner_mouth"]

    def getRightCornerMouth(self):
        return self.points["right_corner_mouth"]
