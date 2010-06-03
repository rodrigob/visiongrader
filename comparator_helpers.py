from result import DataSetResult, ImageResult
from dataset import ImageDataSet

def compare_images_default(toscore, groundtruth, match_objs):
    result = ImageResult()
    #TODO : do not copy all the boxes
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

def compare_datasets_default(toscore, groundtruth, compare_images):
    result = DataSetResult()
    for img in groundtruth:
        if img not in toscore:
            result.add_image_result(compare_images(ImageDataSet(), groundtruth[img]))
        else:
            result.add_image_result(compare_images(toscore[img], groundtruth[img]))
    for img in toscore:
        if img not in groundtruth:
            result.add_image_result(compare_images(toscore[img], ImageDataSet()))
    return result
