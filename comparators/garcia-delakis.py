from result import ImageResult
from comparator_helpers import compare_images_default, compare_datasets_default

name = "GarciaDelakisComparator"

def describe():
    return "Comparator described by Garcia and Delakis. It matches iff the eyes and the mouth are in the box, and the box size does not exceed 20% to the groundtruth box size."

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
        return compare_images(toscore, gndtruth, 2.5)
    return compare_datasets_default(toscore, groundtruth, compare)
