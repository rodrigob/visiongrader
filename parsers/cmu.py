from dataset import DataSet
from point import Point
from objects import EyesNoseMouth

name = "CMU"

def describe():
    return "Parser for the CMU dataset."

def recognize(file):
    return False

def parse(file):
    ret = DataSet()
    for line in file:
        line = line.strip().rstrip()
        splited = line.split()
        filename = splited[0]
        (left_eye_x, left_eye_y, right_eye_x, right_eye_y,
         nose_x, nose_y, left_corner_mouth_x, left_corner_mouth_y,
         center_mouth_x, center_mouth_y, right_corner_mouth_x,
         right_corner_mouth_y) = tuple([float(a) for a in splited[1:]])
        ret.add_obj(filename, EyesNoseMouth(Point(left_eye_x, left_eye_y),
                                            Point(right_eye_x, right_eye_y),
                                            Point(nose_x, nose_y),
                                            Point(left_corner_mouth_x, left_corner_mouth_y),
                                            Point(center_mouth_x, center_mouth_y),
                                            Point(right_corner_mouth_x, right_corner_mouth_y)))
    return ret
