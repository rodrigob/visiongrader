from result import ImageResult
from comparator_helpers import compare_datasets_default

name = "GarciaDelakisComparator"

def describe():
    return "Comparator described by Garcia and Delakis. It matches iff the eyes and the mouth are in the box, and the box size does not exceed 20% to the groundtruth box size."

def match_objs(obj, gndtruth, max_area_ratio):
    points = gndtruth.get_left_eye() + gndtruth.get_right_eye() + gndtruth.get_mouth()
    for point in points:
        if not obj.bounding_box().contains(point):
            return False
    #return float(obj.bounding_box().area()) / float(gndtruth.bounding_box().area()) <= max_area_ratio
    if float(obj.bounding_box().area()) / float(gndtruth.bounding_box().area()) > max_area_ratio:
        print obj.bounding_box().x1, obj.bounding_box().x2, \
              gndtruth.bounding_box().x1, gndtruth.bounding_box().x2
        return False
    else:
        return True

def compare_images(toscore, groundtruth, max_area_ratio):
    result = ImageResult()
    #TODO : do not copy all the boxes
    boxes1 = toscore.get_objs()
    boxes2 = groundtruth.get_objs()
    for box1 in boxes1:
        matched = False
        for box2 in groundtruth.get_intersecting_objs(box1):
            if match_objs(box1, box2, max_area_ratio) and box2 in boxes2:
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
    def compare(toscore, gndtruth):
        return compare_images(toscore, gndtruth, 2.5)
    return compare_datasets_default(toscore, groundtruth, compare)
