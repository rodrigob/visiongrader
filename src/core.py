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

import viewer
import result
import plot
import dataset
import os
from dataset import DataSetMulti

################################################################################
def single_scoring(ts_filename, ts_parser, gt_filename, gt_parser, comparator,
                   gti):
    ts = ts_parser.parse(ts_filename)
    gt = gt_parser.parse(gt_filename)
    return comparator.compare_datasets(ts, gt, gti)

################################################################################
def display(ts_filename, ts_parser, gt_filename, gt_parser, img_path,
            gti = None, parent_window = None, set_legend = None,
            comparator = None):
    if ts_filename != None and ts_parser != None:
        ts = ts_parser.parse_multi(ts_filename)
    else:
        ts = dataset.DataSetMulti()
    v = viewer.GUI(parent_window)
    v.gt = gt_parser.parse(gt_filename)
    if set_legend != None:
        v.set_legend = set_legend
    keys = ts.images_keys()
    gtkeys = v.gt.keys()
    for key in keys[:]: # remove images that are not found in groundtruth
        if key not in gtkeys:
            keys.remove(key)
    if len(keys) != len(gtkeys):
        print 'warning: ' + str(len(ts.images_keys())) \
            + ' images to test but only '\
            + str(len(gtkeys)) + ' images found in groundtruth.'
    print 'Testing ' + str(len(keys)) + ' images...'
    global i
    i = 0
    def on_refresh(ts = ts, v = v, img_name = None):
        global i
        if img_name == None:
            img_name = keys[i]
        else:
            for j in range(0, len(keys)):
                if (keys[j] == img_name):
                    i = j
                    break
        v.img_name = img_name
        filename = gt_parser.get_img_from_name(img_name, gt_filename, img_path)
        v.set_title(img_name)
        v.set_slider_params(0, 1, 6)
        confidence = v.get_slider_position()
        ts2 = ts[confidence]
        matched_gt = None
        matched_ts = None
        matched_gti = None
        matched_tsi = None
        img_gti = None
        if gti: img_gti = gti[img_name]
        if comparator != None and ts2[img_name] != []:
            (matched_gt, matched_ts, matched_gti, matched_tsi) = \
                comparator.get_matched_gprims(ts2[img_name],
                                              v.gt[img_name], img_gti)
        gti_prims = None
        if gti:
            gti_prims = gti.get_gprims(img_name)
        v.display(filename, v.gt.get_gprims(img_name), ts2.get_gprims(img_name),
                  matched_gt, matched_ts, gti_prims, matched_gti, matched_tsi)
    def on_next():
        global i
        i = (i + 1) % len(keys)
        v.boxes = [] # clear added boxes for this frame
        on_refresh()
    def on_activate(text):
        print "opening image %s"%text
        on_refresh(ts, v, text)
    def on_save(text):
        fname = os.path.join(text, v.img_name) + '.txt'
        annotation = os.path.join(img_path, v.img_name) + '.txt'
        (fn, width, height, chans, boxes) = gt_parser.parse_file(annotation)
        gt_parser.save_bboxes(fname, fn, (width, height, chans), v.boxes);
        print 'saving to ' + fname
    def on_prev():
        global i
        i = (i - 1) % len(keys)
        v.boxes = [] # clear added boxes for this frame
        on_refresh()
    v.on_activate = on_activate
    v.on_save = on_save
    v.on_next = on_next
    v.on_prev = on_prev
    v.on_slider_moved = on_refresh
    v.input_save.set_text(img_path)
    v.set_slider_params(ts.confidence_min(), ts.confidence_max(), 2)
    on_refresh()
    if parent_window == None:
        v.start()

################################################################################
        
def multi_scoring(ts_filename, ts_parser, gt_filename, gt_parser, comparator,
                  crawl, sampling, confidence_min, gti = None):
    gt = gt_parser.parse(gt_filename)
    ts = ts_parser.parse_multi(ts_filename, crawl, gt)
    multi_result = result.MultiResult()
    print "Input contains %d confidences" % ts.n_confidences()
    print "Confidence min: %f max: %f" % (ts.confidence_min(),
                                          ts.confidence_max())

    # add empty dataset result to make sure we get a point at (1,1)
    dataset = DataSetMulti()
    multi_result.add_result(comparator.compare_datasets(dataset, gt, gti))
    print "Empty dataset " + str(multi_result)
    
    if sampling == None:
        n = ts.n_confidences()
        print "Looking at all " + str(n) + " confidences to compute curve"
    else:
        n = int(sampling) #int(ts.n_confidences() / sampling)
        print "Sampling confidences to " + str(n) + " steps"
    ts.sort_confidences() # sort confs for an evenly distributed sampling
    for i in xrange(0, n + 1):
        # get only n confidences out of all existing ones, to get an
        # approximation of the curve.
        # if n == n_confidences, then we output the exact curve
        index=int(((ts.n_confidences() - 1) / float(n)) * float(i))
        confidence = ts.get_confidences()[index]
        # ignore confidences lower than confidence_min
        if confidence_min != None:
            if confidence < confidence_min:
                continue
        # get a subset of the dataset using that confidence as threshold
        dataset = ts[confidence]
        # compare this subset with grountruth
        res = comparator.compare_datasets(dataset, gt, gti)
        # add result to results
        multi_result.add_result(res)
        print "i=%d confidence=%f (min %f max %f)" \
            % (i, confidence, dataset.confidence_min(), \
                   dataset.confidence_max()) \
                   + " Subset size: " + str(len(dataset)) + " " + str(res)
    return (multi_result, ts)

################################################################################

def plot_ROC(gt_parser, n_imgs, multi_result, saving_file, show_curve,
             xmin, ymin, xmax, ymax, grid_major, grid_minor):
    if gt_parser.data_type == "images":
        plot.print_ROC(multi_result, n_imgs, saving_file, show_curve,
                       xmin, ymin, xmax, ymax, grid_major, grid_minor)
    elif gt_parser.data_type == "posneg":
        raise NotImplementedError() #TODO: bug in plotter with posneg
        plot.print_DET_posneg(multi_result)
    else:
        raise StandardError("Parser %s : data type %s not \
recognized"%(gt_parser.name, gt_parser.data_type))

################################################################################
    
def plot_DET(gt_parser, n_imgs, multi_result, saving_file, show_curve,
             xmin, ymin, xmax, ymax, grid_major, grid_minor):
    if gt_parser.data_type == "images":
        plot.print_DET(multi_result, n_imgs, saving_file, show_curve,
                       xmin, ymin, xmax, ymax, grid_major, grid_minor)
    elif gt_parser.data_type == "posneg":
        raise NotImplementedError() #TODO: bug in plotter with posneg
        plot.print_DET_posneg(multi_result)
    else:
        raise StandardError("Parser %s : data type %s not \
recognized"%(gt_parser.name, gt_parser.data_type))
