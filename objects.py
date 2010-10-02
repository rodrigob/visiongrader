# Copyright (C) 2010 Michael Mathieu <michael.mathieu@ens.fr>
# 
# This file is part of visiongrader.
# 
# visiongrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# visiongrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with visiongrader.  If not, see <http://www.gnu.org/licenses/>.
# 
# Authors :
#  Michael Mathieu <michael.mathieu@ens.fr>

import math
from point import mean
import gprimitives

class ObjectInfos(object):
    def __init__(self):
        super(ObjectInfos, self).__init__()

    def bounding_box(self):
        return BoundingBox(self.x1, self.y1, self.x2, self.y2)

    def getX1(self):
        return self.bounding_box()._x

    def getX2(self):
        return self.bounding_box()._x2

    def getY1(self):
        return self.bounding_box()._y

    def getY2(self):
        return self.bounding_box()._y2

    x1 = property(getX1)
    x2 = property(getX2)
    y1 = property(getY1)
    y2 = property(getY2)
    
    def get_grpim(self):
        raise NotImplementedError()

    def __str__(self):
        return "ObjectInfos"

class WholeImage(ObjectInfos):
    def __init__(self, filename):
        super(WholeImage, self).__init__()
        self.filename = filename

    def __str__(self):
        return "Whole Image : %s"%(self.filename,)

    def getX1(self):
        return 0

    def getY1(self):
        return 0

    def getX2(self):
        raise NotImplementedError() #TODO

    def getY2(self):
        raise NotImplementedError() #TODO

    def bounding_box(self):
        raise NotImplementedError()

class BoundingBoxError(StandardError):
    def __init__(self):
        super(BoundingBoxError, self).__init__()

class BoundingBox(ObjectInfos):
    def __init__(self, x, y, x2, y2, conf):
        super(BoundingBox, self).__init__()
        self.confidence = conf
        self._x = x
        self._y = y
        self._x2 = x2
        self._y2 = y2
        assert(self._x < self._x2)
        assert(self._y < self._y2)
    
    def getX1(self):
        return self._x

    def getX2(self):
        return self._x2

    def getY1(self):
        return self._y

    def getY2(self):
        return self._y2

    def getWidth(self):
        return self._x2 - self._x

    def getHeight(self):
        return self._y2 - self._y

    def getConfidence(self):
        return self.confidence

    width = property(getWidth)
    height = property(getHeight)

    def area(self):
        return self.width * self.height

    def overlap(self, other):
        return (self.x1 < other.x2 and self.x2 > other.x1 and self.y1 < other.y2 and self.y2 > other.y1)

    def overlapping_area(self, other):
        w = min(self.x2, other.x2) - max(self.x1, other.x1)
        h = min(self.y2, other.y2) - max(self.y1, other.y1)
        if (w < 0 or h < 0):
            return 0
        else:
            return w * h

    def contains(self, p):
        return (self.x1 <= p.x and p.x <= self.x2 and self.y1 <= p.y and p.y <= self.y2)

    def bounding_box(self):
        return self

    def get_gprim(self):
        return gprimitives.Rectangle(self.x1, self.y1,
                                     self.getWidth(), self.getHeight())

    def __str__(self):
        return "Bounding box : x1 = %f, y1 = %f, x2 = %f, y2 = %f"%(self.x1, self.y1,
                                                                    self.x2, self.y2)

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

    def get_point(self, point):
        return self.points[point]

    def __str__(self):
        ret = "Points on object : "
        for key in self.points:
            ret += "(%s, %s) "%(str(key), str(self.points[key]))
        return ret[:-1]

class Eyes(PointsOnObject):
    def __init__(self, left_eye = None, right_eye = None):
        super(Eyes, self).__init__()
        if left_eye != None:
            self.add_point("left_eye", left_eye)
        if right_eye != None:
            self.add_point("right_eye", right_eye)

    def get_left_eye(self):
        return [self.points["left_eye"]]

    def get_right_eye(self):
        return [self.points["right_eye"]]

class Nose(PointsOnObject):
    def __init__(self, nose = None):
        super(Nose, self).__init__()
        if nose != None:
            self.add_point("nose", nose)

    def get_nose(self):
        return [self.points["nose"]]

class Mouth(PointsOnObject):
    def __init__(self, mouth = None):
        super(Mouth, self).__init__()
        if mouth != None:
            self.add_point("mouth", mouth)

    def get_mouth(self):
        return [self.points["mouth"]]

class EyesMouth(Eyes, Mouth):
    def __init__(self, left_eye = None, right_eye = None, mouth = None):
        super(EyesMouth, self).__init__()
        for name in ["left_eye", "right_eye", "mouth"]:
            if vars()[name] != None:
                self.add_point(name, vars()[name])

    def bounding_box(self):
        leye = mean(self.get_right_eye())
        reye = mean(self.get_left_eye())
        deyes = reye - leye
        #xmin = leye - deyes * 0.75).x
        #xmax = reye + deyes * 0.75).x
        mean_eyes = mean([leye, reye])
        mean_mouth = mean(self.get_mouth())
        deyesmouth = mean_mouth - mean_eyes
        #ymin = (mean_eyes - deyesmouth).y
        #ymax = (mean_mouth + deyesmouth * 0.5).y
        t = leye - deyesmouth
        b = t + deyesmouth * 2.5
        tl = t - deyes * 0.75
        tr = t + deyes * 1.75
        bl = b - deyes * 1.75
        br = b + deyes * 1.75
        pts = [tl, tr, bl, br]
        xmin = min([p.x for p in pts])
        xmax = max([p.x for p in pts])
        ymin = min([p.y for p in pts])
        ymax = max([p.y for p in pts])
        return BoundingBox(xmin, ymin, xmax, ymax)

class EyesNoseMouth(EyesMouth, Nose):
    def __init__(self, left_eye = None, right_eye = None, nose = None,
                 left_corner_mouth = None, center_mouth = None, right_corner_mouth = None):
        super(EyesNoseMouth, self).__init__()
        for name in ["left_eye", "right_eye", "nose", "left_corner_mouth",
                     "center_mouth", "right_corner_mouth"]:
            if vars()[name] != None:
                self.add_point(name, vars()[name])

    def get_left_corner_mouth(self):
        return [self.points["left_corner_mouth"]]

    def get_right_corner_mouth(self):
        return [self.points["right_corner_mouth"]]

    def get_center_mouth(self):
        return [self.points["center_mouth"]]

    def get_mouth(self):
        return [self.points["left_corner_mouth"],
                self.points["right_corner_mouth"],
                self.points["center_mouth"]]
