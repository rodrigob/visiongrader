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

def single_scoring(ts_filename, ts_parser, gt_filename, gt_parser, comparator):
    ts = ts_parser.parse(ts_filename)
    gt = gt_parser.parse(gt_filename)
    return comparator.compare_datasets(ts, gt)

def display(ts_filename, ts_parser, gt_filename, gt_parser, img_path,
            parent_window = None, set_legend = None):
    if ts_filename != None and ts_parser != None:
        ts = ts_parser.parse_multi(ts_filename)
    else:
        ts = dataset.DataSetMulti()
    gt = gt_parser.parse(gt_filename)
    v = viewer.GUI(parent_window)
    if set_legend != None:
        v.set_legend = set_legend
    keys = ts.images_keys()
    for key in gt.keys():
        if key not in keys:
            keys.append(key)
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
        filename = gt_parser.get_img_from_name(img_name, gt_filename, img_path)
        v.set_title(img_name)
        confidence = v.get_slider_position()
        ts2 = ts[confidence]
        v.display(filename, gt.get_gprims(img_name), ts2.get_gprims(img_name))
    def on_next():
        global i
        i = (i + 1) % len(keys)
        on_refresh()
    def on_activate(text):
        print "opening image %s"%text
        on_refresh(ts, v, text)
    def on_prev():
        global i
        i = (i - 1) % len(keys)
        on_refresh()
    v.on_activate = on_activate
    v.on_next = on_next
    v.on_prev = on_prev
    v.on_slider_moved = on_refresh
    v.set_slider_params(ts.confidence_min(), ts.confidence_max(), 2)
    on_refresh()
    if parent_window == None:
        v.start()

def multi_scoring(ts_filename, ts_parser, gt_filename, gt_parser, comparator,
                  crawl, sampling, confidence_min):
    ts = ts_parser.parse_multi(ts_filename, crawl)
    gt = gt_parser.parse(gt_filename)
    multi_result = result.MultiResult()
    if sampling == None:
        n = 200
    else:
        n = int(ts.n_confidences() / sampling)
    for i in xrange(0, n):
        confidence = ts.keys()[ts.n_confidences() / n * i]
        if confidence_min != None:
            if confidence < confidence_min:
                continue
        print i
        dataset = ts[confidence]
        multi_result.add_result(comparator.compare_datasets(dataset, gt))
    return (multi_result, ts)

def plot_ROC(gt_parser, n_imgs, multi_result, saving_file, show_curve,
             xmin, ymin, xmax, ymax):
    if gt_parser.data_type == "images":
        plot.print_ROC(multi_result, n_imgs, saving_file, show_curve,
                       xmin, ymin, xmax, ymax)
    elif gt_parser.data_type == "posneg":
        raise NotImplementedError() #TODO: bug in plotter with posneg
        plot.print_DET_posneg(multi_result)
    else:
        raise StandardError("Parser %s : data type %s not \
recognized"%(gt_parser.name, gt_parser.data_type))

def plot_DET(gt_parser, n_imgs, multi_result, saving_file, show_curve,
             xmin, ymin, xmax, ymax):
    if gt_parser.data_type == "images":
        plot.print_DET(multi_result, n_imgs, saving_file, show_curve,
                       xmin, ymin, xmax, ymax)
    elif gt_parser.data_type == "posneg":
        raise NotImplementedError() #TODO: bug in plotter with posneg
        plot.print_DET_posneg(multi_result)
    else:
        raise StandardError("Parser %s : data type %s not \
recognized"%(gt_parser.name, gt_parser.data_type))
