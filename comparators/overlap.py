from result import DataSetResult, ImageResult

name = "OverlapComparator"

def describe():
    return "The boxes match iff they overlap"

def match_objs(obj, gndtruth):
    return obj.bounding_box().overlap(gndtruth.bounding_box())

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
    result = DataSetResult()
    i = 0
    for (image_toscore, image_groundtruth) in zip(toscore, groundtruth):
        print i
        i += 1
        result.add_image_result(compare_images(image_toscore, image_groundtruth))
    return result
