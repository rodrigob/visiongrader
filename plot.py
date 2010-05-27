import pylab

def print_ROC(multi_result):
    points = []
    for result in multi_result:
        fp = float(result.n_false_positives)
        missed = float(result.n_unrecognized)
        matches = float(result.n_matches)
        points.append((fp, matches / (matches + missed)))
    points.sort()
    pylab.plot([a[0] for a in points], [a[1] for a in points])
    pylab.show()

def print_DET(multi_result):
    points = []
    for result in multi_result:
        fp = float(result.n_false_positives)
        missed = float(result.n_unrecognized)
        matches = float(result.n_matches)
        n_imgs = float(len(result.images_results))
        points.append((fp / n_imgs, missed / (matches + missed)))
    points.sort()
    pylab.plot([a[0] for a in points], [a[1] for a in points])
    pylab.show()
