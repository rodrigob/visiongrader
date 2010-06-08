import pylab
import matplotlib
import cPickle

def print_ROC(multi_result, n_imgs, save_filename = None, show_curve = True,
              xmin = None, ymin = None, xmax = None, ymax = None):
    points = []
    n_imps = float(n_imgs)
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        fn = float(result.n_false_negatives())
        #n_imgs = float(len(result.images))
        points.append((fp / n_imgs, tp / (tp + fn)))
    points.sort()
    if save_filename != None:
        f = open(save_filename, "w")
        cPickle.dump(points, f)
        f.close()
    if show_curve:
        pylab.semilogx([a[0] for a in points], [a[1] for a in points])
        if xmin != None:
            pylab.axis(xmin = xmin)
        if xmax != None:
            pylab.axis(xmax = xmax)
        if ymin != None:
            pylab.axis(ymin = ymin)
        if ymax != None:
            pylab.axis(ymax = ymax)
        pylab.xlabel("False positives per image")
        pylab.ylabel("Detection rate")
        pylab.show()

def print_DET(multi_result, n_imgs, save_filename = None, show_curve = True,
              xmin = None, ymin = None, xmax = None, ymax = None):
    points = []
    n_imgs = float(n_imgs)
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        fn = float(result.n_false_negatives())
        #n_imgs = float(len(result.images))
        #the "-" is a trick for sorting
        points.append((fp / n_imgs, - fn / (tp + fn)))
    points.sort()
    if save_fulename != None:
        f = open(save_filename, "w")
        cPickle.dump(points, f)
        f.close()
    #TODO : params
    if show_curve:
        pylab.loglog([a[0] for a in points], [- a[1] for a in points])
        if xmin != None:
            pylab.axis(xmin = xmin)
        if xmax != None:
            pylab.axis(xmax = xmax)
        if ymin != None:
            pylab.axis(ymin = ymin)
        if ymax != None:
            pylab.axis(ymax = ymax)
        pylab.xlabel("False positives per image")
        pylab.ylabel("Miss rate")
        pylab.show()



################## old : ####################
        
def print_ROC_posneg(multi_result):
    raise NotImplementedError() #TODO : do not use
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

def print_DET_posneg(multi_result):
    raise NotImplementedError() #TODO : do not use
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
