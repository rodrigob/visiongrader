# Copyright (C) 2010 Michael Mathieu <michael.mathieu@ens.fr>
# 
# This file is part of visiongrader.
# 
# visiongrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# visiongrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with visiongrader.  If not, see <http://www.gnu.org/licenses/>.
# 
# Authors :
#  Michael Mathieu <michael.mathieu@ens.fr>

import sys
#sys.path.insert(0, '/home/sermanet/installed/matplotlib/matplotlib-1.0.0/build/lib.linux-x86_64-2.4/')
import pylab
#import matplotlib
import cPickle

################################################################################
def print_ROC(multi_result, n_imgs, save_filename = None, show_curve = True,
              xmin = None, ymin = None, xmax = None, ymax = None,
              grid_major = False, grid_minor = False):
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

################################################################################
def print_DET(multi_result, n_imgs, save_filename = None, show_curve = True,
              xmin = None, ymin = None, xmax = None, ymax = None,
              grid_major = False, grid_minor = False):
    print "Printing DET curve with xmin: " + str(xmin) + " xmax: " + str(xmax) \
        + " ymin: " + str(ymin) + " ymax: " + str(ymax)
    points = []
    n_imgs = float(n_imgs)
    # each result is defined for a given threshold
    for result in multi_result:
        tp = float(result.n_true_positives())
        fp = float(result.n_false_positives())
        fn = float(result.n_false_negatives())
        #n_imgs = float(len(result.images))
        #the "-" is a trick for sorting
        points.append((max(xmin, fp / n_imgs), - fn / (tp + fn)))
        # print "appending " + str(max(xmin, fp / n_imgs)) + ", " \
        #     + str(fn / (tp + fn)) + " tp=" + str(result.n_true_positives()) \
        #     + " fp=" + str(result.n_false_positives()) \
        #     + " fn=" + str(result.n_false_negatives()) \
        #     + " nimgs=" + str(n_imgs)
    points.sort()
    # print score at 1 FPPI
    # find y for x=val
    val = 1
    y = 0
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    for a in points:
        x2 = x1
        y2 = y1
        x1 = a[0]
        y1 = -a[1]
        if (x1 > 1 and x2 <= 1): # interpolate
            y = y2 + (y1 - y2) * (val - x2) / (x1 - x2)
    if (x1 <= 1 and x2 <= 1):
        y = y1
    y = y * 100 # use percentage
    print "miss rate at " + str(val) + "FPPI=" + "%.2f%%"%y
    # save curve
    if save_filename != None:
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
        if grid_major:
            pylab.grid(True, which='major')
        if grid_minor:
            pylab.grid(True, which='minor')    
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
