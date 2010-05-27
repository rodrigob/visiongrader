import pylab

def print_ROC(multi_result):
    points = []
    for result in multi_result:
        tp = float(result.n_true_positives)
        fp = float(result.n_false_positives)
        fn = float(result.n_false_negatives)
        n_imgs = float(len(result.images_results))
        points.append((fp / n_imgs, tp / (tp + fn)))
    points.sort()
    pylab.plot([a[0] for a in points], [a[1] for a in points])
    pylab.show()

def print_ROC_posneg(multi_result):
    prints = []
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        tn = float(result.n_true_negatives())
        fn = float(result.n_false_nogatices())
        points.append(fp / (fp + tn), tp / (tp + fn))
    points.sort()
    pylab.plot([a[0] for a in points], [a[1] for a in points])
    pylab.show()

def print_DET(multi_result):
    points = []
    for result in multi_result:
        tp = float(result.n_true_positives)
        fp = float(result.n_false_positives)
        fn = float(result.n_false_negatives)
        n_imgs = float(len(result.images_results))
        #the "-" is a trick for sorting
        points.append((fp / n_imgs, - fn / (tp + fn)))
    points.sort()
    pylab.plot([a[0] for a in points], [- a[1] for a in points])
    pylab.show()

def print_DET_posneg(multi_result):
    prints = []
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        tn = float(result.n_true_negatives())
        fn = float(result.n_false_nogatices())
        #the "-" is a trick for sorting
        points.append(fp / (fp + tn), - fn / (tp + fn))
    points.sort()
    pylab.plot([a[0] for a in points], [- a[1] for a in points])
    pylab.show()
