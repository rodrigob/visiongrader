import pylab

def print_ROC(roc_result):
    points = []
    for thres in roc_result:
        fp = float(roc_result[thres].n_false_positives)
        missed = float(roc_result[thres].n_unrecognized)
        matches = float(roc_result[thres].n_matches)
        points.append((fp, matches / (matches + missed)))
    points.sort()
    pylab.plot([a[0] for a in points], [a[1] for a in points])
    pylab.show()
