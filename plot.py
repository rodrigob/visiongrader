import pylab
import matplotlib

save_curve = True
if save_curve:
    import cPickle

show_curve = False

def print_ROC(multi_result, n_imgs):
    points = []
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        fn = float(result.n_false_negatives())
        #n_imgs = float(len(result.images))
        points.append((fp / n_imgs, tp / (tp + fn)))
    points.sort()
    pylab.semilogx([a[0] for a in points], [a[1] for a in points])
    pylab.xlabel("False positives per image")
    pylab.ylabel("Detection rate")
    pylab.show()

def print_ROC_posneg(multi_result):
    raise NotImplementedError()
    prints = []
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        tn = float(result.n_true_negatives())
        fn = float(result.n_false_negatives())
        points.append((fp / (fp + tn), tp / (tp + fn)))
    points.sort()
    pylab.plot([a[0] for a in points], [a[1] for a in points])
    pylab.show()

def print_DET(multi_result, n_imgs):
    points = []
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        fn = float(result.n_false_negatives())
        #n_imgs = float(len(result.images))
        print tp, fp, fn
        #the "-" is a trick for sorting
        points.append((fp / n_imgs, - fn / (tp + fn)))
    points.sort()
    pylab.loglog([a[0] for a in points], [- a[1] for a in points])
    if save_curve:
        f = open("curve.pickle", "w")
        cPickle.dump(points, f)
        f.close()
        #print max([a[0] for a in points]), n_imgs
    #TODO : params
    pylab.axis(xmin=0.005, xmax=10)
    pylab.axis(ymin=0.05,  ymax=1)
    pylab.xlabel("False positives per image")
    pylab.ylabel("Miss rate")
    if show_curve:
        pylab.show()

def print_DET_posneg(multi_result):
    raise NotImplementedError()
    points = []
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        tn = float(result.n_true_negatives())
        fn = float(result.n_false_negatives())
        #the "-" is a trick for sorting
        points.append((fp / (fp + tn), - fn / (tp + fn)))
    points.sort()
    print points
    pylab.plot([a[0] for a in points], [- a[1] for a in points])
    pylab.show()
