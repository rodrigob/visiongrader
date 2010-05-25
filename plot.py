import pylab

def print_ROC(multi_result):
    points = []
    for thres in multi_result:
        fp = float(multi_result[thres].n_false_positives)
        missed = float(multi_result[thres].n_unrecognized)
        matches = float(multi_result[thres].n_matches)
        points.append((fp, matches / (matches + missed)))
    points.sort()
    pylab.plot([a[0] for a in points], [a[1] for a in points])
    pylab.show()

def print_DET(multi_result):
    points = []
    for thres in multi_result:
        fp = float(multi_result[thres].n_false_positives)
        missed = float(multi_result[thres].n_unrecognized)
        matches = float(multi_result[thres].n_matches)
        n_imgs = float(len(multi_result[thres].images_results))
        points.append((fp / n_imgs, missed / (matches + missed)))
    points.sort()
    pylab.plot([a[0] for a in points], [a[1] for a in points])
    pylab.show()
    
