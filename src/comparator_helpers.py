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

# Return the bbox found in intersecting_boxes and present in all_boxes
# that matches best 'box', based on the matching criterion function match_objs
# and the matching score funciton match_score.
def best_match(box, intersecting_boxes, all_boxes, match_objs, match_score):
    best_bb = None
    best_score = 0
    # loop on objects in input boxes that intersect with box1
    for box2 in intersecting_boxes[:]:
        if match_objs(box, box2) and box2 in all_boxes:
            score = match_score(box, box2)
            if best_bb == None or score > best_score:
                best_bb = box2
                best_score = score
    return best_bb

# Compare 1 image to score with 1 groundtruth image
# Return a ImageResult object that contains tallies of false positives,
# true positives, etc.
def get_matches(toscore, groundtruth, match_objs, match_score, gtignore = None):
    matched_pairs = []
    unmatched = []
    unmatched_gt = []
    matched_pairs_ignore = []
    unmatched_ignore = []
    # loop on groundtruth bboxes
    boxes1 = groundtruth.get_objs()
    boxes2 = toscore.get_objs()
    for box1 in boxes1[:]:
        best_bb = best_match(box1, toscore.get_intersecting_objs(box1), boxes2,
                             match_objs, match_score)
        # if match, remove box from input so it cannot be matched anymore
        if best_bb:
            matched_pairs.append((box1, best_bb))
            boxes1.remove(box1)
            boxes2.remove(best_bb)
    # loop on ignored bboxes
    if gtignore:
        igboxes = gtignore.get_objs()
        for igbox in igboxes[:]:
            best_bb = best_match(igbox, toscore.get_intersecting_objs(igbox),
                                 boxes2, match_objs, match_score)
            # if match, remove box from input so it cannot be matched anymore
            if best_bb:
                matched_pairs_ignore.append((igbox, best_bb))
                igboxes.remove(igbox)
                boxes2.remove(best_bb)
        # remaining ignored boxes go to unmatched_ignore
        for b in igboxes:
            unmatched_ignore.append(b)
    # remaining boxes in groundtruth are false negatives
    for box1 in boxes1:
        unmatched_gt.append(box1)
    # remaining boxes in input boxes are false positives
    for box2 in boxes2:
        unmatched.append(box2)
    return (matched_pairs, unmatched, unmatched_gt, matched_pairs_ignore,
            unmatched_ignore)

# Compare 1 image to score with 1 groundtruth image
# Return a ImageResult object that contains tallies of false positives,
# true positives, etc.
def compare_images_default(toscore, groundtruth, match_objs, match_score,
                           gtignore = None):
    result = ImageResult()
#    for matched_pairs, unmatched, unmatched_gt in \
#            in get_matches(toscore, groundtruth, match_objs, match_score):
    (matched_pairs, unmatched, unmatched_gt, matched_pairs_ignore,
     unmatched_ignore) = \
     get_matches(toscore, groundtruth, match_objs, match_score, gtignore)
    for pair in matched_pairs:
        result.add_true_positive(pair[0], pair[1])
    for u in unmatched:
        result.add_false_positive(u)
    for u in unmatched_gt:
        result.add_false_negative(u)
        # print 'toscore len: ' + str(len(toscore.get_objs())) \
    #     + ' gt len: ' + str(len(groundtruth.get_objs())) \
    #     + ' m0: ' + str(len(m0)) \
    #     + ' m1: ' + str(len(m1)) \
    #     + ' m2: ' + str(len(m2)) \
#        print 'pairs: ' + str(len(matched_pairs)) + ' unmatched: ' + str(len(unmatched)) + ' unmatched_gt ' + str(len(unmatched_gt))

    return result

# # Compare 1 image to score with 1 groundtruth image
# # Return a ImageResult object that contains tallies of false positives,
# # true positives, etc.
# def compare_images_default(toscore, groundtruth, match_objs, match_score):
#     result = ImageResult()
#     #TODO : do not copy all the boxes
#     #TODO: rank matches across all possible combinations,
#     #      instead of matching first occuring match.
#     boxes1 = groundtruth.get_objs()
#     boxes2 = toscore.get_objs()
#     for box1 in boxes1: # loop on groundtruth bboxes
#         matched = False
#         # loop on objects in input boxes that intersect with box1
#         best_bb = None
#         best_score = 0
#         for box2 in toscore.get_intersecting_objs(box1):
#             if match_objs(box1, box2) and box2 in boxes2:
#                 matched = True
#                 score = match_score(box1, box2)
#                 if best_bb == None or score > best_score:
#                     best_bb = box2
#                     best_score = score
#         # if match, remove box from input so it cannot be matched anymore
#         if matched:
#             result.add_true_positive(box1, best_bb)
#             boxes1.remove(box1)
#             boxes2.remove(best_bb)
#     # remaining boxes in groundtruth are false negatives
#     for box1 in boxes1:
#         result.add_false_negative(box1)
#     # remaining boxes in input boxes are false positives
#     for box2 in boxes2:
#         result.add_false_positive(box2)
#     return result

# Return rectangle primitives of matched bboxes for dataset 1 and dataset 2,
# as a pair of primitives. This is used for display to differentiate
# matched boxes from non matched boxes
def compare_images_gprims(toscore, groundtruth, match_objs, match_score,
                          gtignore = None):
    prims1 = []
    prims2 = []
    prims3 = []
    prims4 = []

    (matched_pairs, unmatched, unmatched_gt, matched_pairs_ignore,
     unmatched_ignore) = \
        get_matches(toscore, groundtruth, match_objs, match_score, gtignore)
    for pair in matched_pairs:
        prims1.append(pair[0].get_gprim())
        prims2.append(pair[1].get_gprim())
    for pair in matched_pairs_ignore:
        prims3.append(pair[0].get_gprim())
        prims4.append(pair[1].get_gprim())
    

# #TODO : do not copy all the boxes
#     #TODO: rank matches across all possible combinations,
#     #      instead of matching first occuring match.
#     boxes1 = toscore.get_objs()
#     boxes2 = groundtruth.get_objs()
#     for box1 in boxes1:
#         for box2 in groundtruth.get_intersecting_objs(box1):
#             if match_objs(box1, box2) and box2 in boxes2:
#                 prims1.append(box1.get_gprim())
#                 prims2.append(box2.get_gprim())
#                 boxes2.remove(box2)
#                 break
    return (prims1, prims2, prims3, prims4)

# compare a set of groundtruth images against a set of new images
def compare_datasets_default(toscore, groundtruth, compare_images,
                             gtignore = None):
    result = DataSetResult(288, 589)
    # for each image in the groundtruth, compare with image to score if exists
    for img in groundtruth:
        gti = None
        if gtignore: gti = gtignore[img]
        if img not in toscore:
            result.add_image_result(compare_images(ImageDataSet(),
                                                   groundtruth[img], gti))
        else:
            result.add_image_result(compare_images(toscore[img],
                                                   groundtruth[img], gti))
    # for each image to score, compare with groundtruth image if exists
    for img in toscore:
        if img not in groundtruth:
            gti = None
            if gtignore: gti = gtignore[img]
            result.add_image_result(compare_images(toscore[img],
                                                   ImageDataSet(), gti))
    return result
