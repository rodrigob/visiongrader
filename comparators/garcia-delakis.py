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

from comparator_helpers import compare_images_default, compare_datasets_default

name = "GarciaDelakisComparator"

def describe():
    return "Comparator described by Garcia and Delakis. It matches iff the eyes and the mouth are in the box, and the box size does not exceed 20% to the groundtruth box size."

p_max_ratio = 2.5

def match_objs(obj, gndtruth, max_area_ratio):
    points = gndtruth.get_left_eye() + gndtruth.get_right_eye() + gndtruth.get_mouth()
    for point in points:
        if not obj.bounding_box().contains(point):
            return False
    if float(obj.bounding_box().area()) / float(gndtruth.bounding_box().area()) > max_area_ratio:
        return False
    else:
        return True

def compare_images(toscore, groundtruth, max_area_ratio):
    return compare_images_default(toscore, groundtruth, lambda a, b:match_objs(a, b, max_area_ratio))

def compare_datasets(toscore, groundtruth):
    def compare(toscore, gndtruth):
        return compare_images(toscore, gndtruth, p_max_ratio)
    return compare_datasets_default(toscore, groundtruth, compare)

def set_param(param):
    if param != None:
        global p_max_ratio
        p_max_ratio = param
