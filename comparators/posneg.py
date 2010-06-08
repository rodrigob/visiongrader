from comparator_helpers import compare_images_default, compare_datasets_default
from result import BoolResult

name = "PosNegComparator"

def describe():
    return "Comparator for images containing only a single person or none"

def compare_datasets(toscore, groundtruth):
    raise NotImplementedError()
    result = BoolResult()
    #print groundtruth
    for img in groundtruth:
        len_gt = len(groundtruth[img])
        if img not in toscore:
            if len_gt == 0:
                result.add_true_negative(img)
            else:
                result.add_false_negative(img)
        else:
            len_ts = len(toscore[img])
            if len_gt == 0:
                if len_ts == 0:
                    result.add_true_negative(img)
                else:
                    result.add_false_positive(img)
            else:
                if len_ts == 0:
                    result.add_false_negative(img)
                else:
                    result.add_true_positive(img)
    return result
