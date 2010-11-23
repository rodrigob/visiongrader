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

from comparator_helpers import compare_images_default, \
    compare_datasets_default, compare_images_gprims

name = "Overlap50PercentComparator"
p_overlap = 0.5

def describe():
    return "The boxes match iff intersection/union > " + str(p_overlap)

def match_objs(obj, gndtruth, p):
    '''p is the maximum ratio allowed between the intersection and the union.
    Set it to 0.5 to have 50%.'''
    b1 = obj.bounding_box()
    b2 = gndtruth.bounding_box()
    inter = b1.overlapping_area(b2)
    union = b1.area() + b2.area() - inter
    return inter / union > p

def match_score(obj, gndtruth):
    b1 = obj.bounding_box()
    b2 = gndtruth.bounding_box()
    inter = b1.overlapping_area(b2)
    union = b1.area() + b2.area() - inter
    return inter / union

def compare_images(toscore, groundtruth, gtignore = None):
    return compare_images_default(toscore, groundtruth,
                                  lambda a, b: match_objs(a, b, p_overlap),
                                  lambda a, b: match_score(a, b),
                                  gtignore)

def compare_datasets(toscore, groundtruth, gtignore = None):
    return compare_datasets_default(toscore, groundtruth, compare_images,
                                    gtignore)

def get_matched_gprims(img_toscore, img_groundtruth, gtignore = None):
    return compare_images_gprims(img_toscore, img_groundtruth,
                                 lambda a, b: match_objs(a, b, p_overlap),
                                 lambda a, b: match_score(a, b),
                                 gtignore)

def set_param(param):
    if param != None:
        global p_overlap
        p_overlap = param
