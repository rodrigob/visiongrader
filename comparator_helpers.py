from result import DataSetResult
from dataset import ImageDataSet

def compare_datasets_default(toscore, groundtruth, compare_images):
    result = DataSetResult()
    i = 0
    for img in groundtruth:
        print i, img
        i += 1
        if img not in toscore:
            result.add_image_result(compare_images(ImageDataSet(), groundtruth[img]))
        else:
            result.add_image_result(compare_images(toscore[img], groundtruth[img]))
        #TODO : look for the img in toscore but not in gndtruth
    return result
