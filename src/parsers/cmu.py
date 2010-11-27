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

from dataset import DataSet
from point import Point
from objects import EyesNoseMouth

name = "CMU"

data_type = "images"

path_is_folder = False

def describe():
    return "Parser for the CMU dataset."

def recognize(file):
    return False

def parse(filen, crawl = False):
    if crawl == True:
        raise StandardError()
    file = open(filen, "r")
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
    file.close()
    return ret
