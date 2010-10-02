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

from result import DataSetResult, ImageResult
from dataset import ImageDataSet

# compare 1 image to score with 1 groundtruth image
# return a ImageResult object that contains tallies of false positives,
# true positives, etc.
def compare_images_default(toscore, groundtruth, match_objs):
    result = ImageResult()
    #TODO : do not copy all the boxes
    #TODO: rank matches across all possible combinations,
    #      instead of matching first occuring match.
    boxes1 = toscore.get_objs()
    boxes2 = groundtruth.get_objs()
    for box1 in boxes1:
        matched = False
        for box2 in groundtruth.get_intersecting_objs(box1):
            if match_objs(box1, box2) and box2 in boxes2:
                result.add_true_positive(box1, box2)
                matched = True
                boxes2.remove(box2)
                break
        if not matched:
            result.add_false_positive(box1)
    for box2 in boxes2:
        result.add_false_negative(box2)
    return result

# Return rectangle primitives of matched bboxes for dataset 1 and dataset 2,
# as a pair of primitives. This is used for display to differentiate
# matched boxes from non matched boxes
def compare_images_gprims(toscore, groundtruth, match_objs):
    prims1 = []
    prims2 = []
    #TODO : do not copy all the boxes
    #TODO: rank matches across all possible combinations,
    #      instead of matching first occuring match.
    boxes1 = toscore.get_objs()
    boxes2 = groundtruth.get_objs()
    for box1 in boxes1:
        for box2 in groundtruth.get_intersecting_objs(box1):
            if match_objs(box1, box2) and box2 in boxes2:
                prims1.append(box1.get_gprim())
                prims2.append(box2.get_gprim())
                boxes2.remove(box2)
                break
    return (prims1, prims2)

# compare a set of groundtruth images against a set of new images
def compare_datasets_default(toscore, groundtruth, compare_images):
    result = DataSetResult()
    # for each image in the groundtruth, compare with image to score if exists
    for img in groundtruth:
        if img not in toscore:
            result.add_image_result(compare_images(ImageDataSet(),
                                                   groundtruth[img]))
        else:
            result.add_image_result(compare_images(toscore[img],
                                                   groundtruth[img]))
    # for each image to score, compare with groundtruth image if exists
    for img in toscore:
        if img not in groundtruth:
            result.add_image_result(compare_images(toscore[img],
                                                   ImageDataSet()))
    return result
