from result import ImageResult
from comparator_helpers import compare_images_default, compare_datasets_default

name = "OverlapComparator"

def describe():
    return "The boxes match iff they overlap"

def match_objs(obj, gndtruth):
    return obj.bounding_box().overlap(gndtruth.bounding_box())

def compare_images(toscore, groundtruth):
    return compare_images_default(toscore, groundtruth, match_objs)

def compare_datasets(toscore, groundtruth):
    return compare_datasets_default(toscore, groundtruth, compare_images)
