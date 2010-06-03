from comparator_helpers import compare_images_default, compare_datasets_default

name = "Overlap50PercentComparator"

def describe():
    return "The boxes match iff they overlap more than 50%."

def match_objs(obj, gndtruth, p):
    '''p is the maximum ratio allowed between the intersection and the union.
    Set it to 0.5 to have 50%.'''
    b1 = obj.bounding_box()
    b2 = gndtruth.bounding_box()
    inter = b1.overlapping_area(b2)
    union = b1.area() + b2.area() - inter
    return inter / union > p

def compare_images(toscore, groundtruth):
    return compare_images_default(toscore, groundtruth, lambda a, b: match_objs(a, b, 0.3))

def compare_datasets(toscore, groundtruth):
    return compare_datasets_default(toscore, groundtruth, compare_images)
