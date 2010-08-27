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

name = "Overlap50PercentComparator"

def describe():
    return "The boxes match iff they overlap more than 50%."

p_overlap = 0.3

def match_objs(obj, gndtruth, p):
    '''p is the maximum ratio allowed between the intersection and the union.
    Set it to 0.5 to have 50%.'''
    b1 = obj.bounding_box()
    b2 = gndtruth.bounding_box()
    inter = b1.overlapping_area(b2)
    union = b1.area() + b2.area() - inter
    return inter / union > p

def compare_images(toscore, groundtruth):
    return compare_images_default(toscore, groundtruth,
                                  lambda a, b: match_objs(a, b, p_overlap))

def compare_datasets(toscore, groundtruth):
    return compare_datasets_default(toscore, groundtruth, compare_images)

def set_param(param):
    if param != None:
        global p_overlap
        p_overlap = param
