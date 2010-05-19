from result import ImageResult
from comparator_helpers import compare_datasets_default

name = "GarciaDelakisComparator"

def describe():
    return "Comparator described by Garcia and Delakis. It matches iff the eyes and the mouth are in the box, and the box size does not exceed 20% to the groundtruth box size."

def match_objs(obj, gndtruth):
    points = gndtruth.get_left_eye() + gndtruth.get_right_eye() + gndtruth.get_mouth()
    for point in points:
        if not obj.bounding_box().contains(point):
            return False
    return float(obj.bounding_box().area()) / float(gndtruth.bounding_box().area()) <= 1.20

def compare_images(toscore, groundtruth):
    result = ImageResult()
    #TODO : do not copy all the boxes
    boxes1 = toscore.get_objs()
    boxes2 = groundtruth.get_objs()
    for box1 in boxes1:
        matched = False
        for box2 in groundtruth.get_intersecting_objs(box1):
            if match_objs(box1, box2) and box2 in boxes2:
                result.add_match(box1, box2)
                matched = True
                boxes2.remove(box2)
                break
        if not matched:
            result.add_false_positive(box1)
    for box2 in boxes2:
        result.add_unrecognized(box2)
    return result

def compare_datasets(toscore, groundtruth):
    return compare_datasets_default(toscore, groundtruth, compare_images)
