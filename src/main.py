#!/usr/bin/python

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

import optparse
import os
import os.path
import sys
import core
import plot
from modules import ModuleHandler

if __name__=="__main__":
    usage = "usage: %prog -i input -g groundtruth --input_parser inputparser \
--groundtruth_parser groundtruthparser [-c comparator] [--roc] [--det] [--disp] \
[OPTIONS]\n       %prog --help"
    op = optparse.OptionParser(add_help_option = True, usage = usage,
                               prog = "./main.py")
    # input files
    op.add_option("-i", "--input", dest = "input", default = None, type = "str",
                  help = "Input file to score (if not specified, a generator \
must be specified)")
    op.add_option("-t", "--groundtruth", dest = "groundtruth", default = None,
                  type = "str", help = "Ground truth file(s) (required)")
    op.add_option("--ignore", dest = "gtignore", default = None,
                  type = "str",
                  help = "Ignored ground truth file(s) (optional)")
    op.add_option("--input_parser", dest = "input_parser", default = None,
                  type = "str", help = "Parser to use for the file to score")
    op.add_option("--groundtruth_parser", dest = "groundtruth_parser",
                  default = None, type = "str",
                  help = "Parser to use for the ground truth file")
    op.add_option("--parser_dir", dest = "parser_dir", default = "parsers",
                  type = "str", help = "Parser directory")
    # comparator
    op.add_option("--comparator_dir", dest = "comparator_dir",
                  default = "comparators", type = "str",
                  help = "Comparator directory")
    op.add_option("-c", "--comparator", dest = "comparator",
                  default = None, type = "str",
                  help = "Comparator to use (required)")
    op.add_option("--comparator_param", dest = "comp_param", default = None,
                  type = "float", help = "Parameter to pass to the comparator.")
    # mode
    op.add_option("--roc", dest = "roc", action = "store_true", default = False,
                  help = "Print ROC curve.")
    op.add_option("--det", dest = "det", action = "store_true", default = False,
                  help = "Print DET curve.")
    op.add_option("--disp", dest = "display", action = "store_true",
                  default = False,
                  help = "Display the images, groundtruths and bounding boxes.")
    # mode-specific options
    op.add_option("--confidence_min", dest = "confidence_min",
                  default = None, type = "float",
                  help = "Mminimum confidence to display for the curves.")
    op.add_option("--crawl", action = "store_true", dest = "crawl",
                  default = False, help = "Crawls eblearn files.")
    op.add_option("--sampling", dest = "sampling", default = None,
                  type = "int",
                  help = "Sampling rate for the curves. With 1 all the points are \
used, with 10, one on 10 is used, and so on.")
    op.add_option("--show-no-curve", dest = "show_curve", action = "store_false",
                  help = "Do not display the ROC/DET curve.", default = True)
    op.add_option("--saving-file", dest = "saving_file", default = None,
                  type = "str", help = "Name of the file to save the curve. \
The curve is not saved if no file is specified.")
    op.add_option("--grid_major", dest = "grid_major",
                  action = "store_true", default = False,
                  help = "Display major grid")
    op.add_option("--grid_minor", dest = "grid_minor",
                  action = "store_true", default = False,
                  help = "Display minor grid")
    op.add_option("--xmin", dest = "xmin", default = None, type ="float",
                  help = "Minimum of the x axis for ROC/DET curve.")
    op.add_option("--xmax", dest = "xmax", default = None, type ="float",
                  help = "Maximum of the x axis for ROC/DET curve.")
    op.add_option("--ymin", dest = "ymin", default = None, type ="float",
                  help = "Minimum of the y axis for ROC/DET curve.")
    op.add_option("--ymax", dest = "ymax", default = None, type ="float",
                  help = "Maximum of the y axis for ROC/DET curve.")
    op.add_option("--images_path", dest = "img_path", default = None,
                  type = "str",
                  help = "Path to the images if 'disp' mode.")
    op.add_option("--gt_whratio", dest = "gt_whratio", default = None,
                  type ="float",
                  help = "Force groundtruth's bboxes width to be this \
ratio * the height.")
    op.add_option("--whratio", dest = "whratio", default = None,
                  type ="float",
                  help = "Force input curve's bboxes width to be this \
ratio * height.")
    op.add_option("--hratio", dest = "hratio", default = None,
                  type ="float",
                  help = "Force input curve's bboxes height to be this \
ratio * height.")
    op.add_option("--wratio", dest = "wratio", default = None,
                  type ="float",
                  help = "Force input curve's bboxes width to be this \
ratio * width.")
    (options, args) = op.parse_args()
    
    modes = [("roc", "ROC"), ("det", "DET"), ("display", "display")]
    mode = None
    for (mode_opt, mode_name) in modes:
        if getattr(options, mode_opt) == True:
            if mode != None:
                sys.stderr.write("You cannot choose mode than one mode \
(--roc, --det or --disp).\n")
                sys.exit(0)
            mode = mode_name
    if mode == None:
        mode = "input_file"

    if options.input == None and mode != "display":
        op.print_usage()
        sys.stderr.write("input missing.\n")
        sys.exit(0)
    toscore_filename = options.input

    if options.groundtruth == None:
        op.print_usage()
        sys.stderr.write("groundtruth missing.\n")
        sys.exit(0)
    groundtruth_filename = options.groundtruth

    parser_dir = options.parser_dir
    comparator_dir = options.comparator_dir
    main_path = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))
    parsers = ModuleHandler(main_path, parser_dir)
    comparators = ModuleHandler(main_path, comparator_dir)

    if options.groundtruth_parser == None:
        op.print_usage()
        sys.stderr.write("groundtruth parser is missing.\n")
        sys.exit(0)
    groundtruth_parser = parsers.get_module(options.groundtruth_parser)
    groundtruth_parser.whratio = options.gt_whratio
    areas = groundtruth_parser.find_minmax_areas(options.groundtruth)
    groundtruth_parser.min_area = areas[0]
    groundtruth_parser.max_area = areas[1]
    groundtruth_parser.min_area_ratio = areas[2]
    groundtruth_parser.max_area_ratio = areas[3]
    print "Groundtruth parser: " + groundtruth_parser.describe()

    # groundtruth ignore parser
    gti = None
    if options.gtignore:
        gti_parser = parsers.get_module(options.groundtruth_parser)
        gti_parser.whratio = options.gt_whratio
        gti = gti_parser.parse(options.gtignore)
        print 'Found ignore dataset in ' + options.gtignore + ' with ' \
            + str(len(gti)) + ' images' #: ' + str(gti)
    
    if options.input_parser == None:
        if toscore_filename != None:
            op.print_usage()
            sys.stderr.write("input parser is missing.\n")
            sys.exit(0)
        else:
            toscore_parser = None
    else:
        #TODO : check existence
        toscore_parser = parsers.get_module(options.input_parser)
        toscore_parser.whratio = options.whratio
        toscore_parser.hratio = options.hratio
        toscore_parser.wratio = options.wratio
        # toscore_parser.min_area = groundtruth_parser.min_area
        # toscore_parser.max_area = groundtruth_parser.max_area
        # toscore_parser.min_area_ratio = groundtruth_parser.min_area_ratio
        # toscore_parser.max_area_ratio = groundtruth_parser.max_area_ratio
        # toscore_parser.min_area_ratio = 0.0037559298603
        # toscore_parser.min_area_ratio = 0.0015
        # toscore_parser.max_area_ratio = 0.53286546224
        # toscore_parser.max_area_ratio = 0.7
        print "Input parser: " + toscore_parser.describe()


    if mode != "display":
        if options.comparator == None:
            op.print_usage()
            sys.stderr.write("comparator missing.\n")
            sys.exit(0)
        comparator = comparators.get_module(options.comparator)
        comparator.set_param(options.comp_param)
        print "Comparator: " + comparator.describe()
    
    if mode == "input_file":
        print core.single_scoring(toscore_filename, toscore_parser,
                                  groundtruth_filename, groundtruth_parser,
                                  comparator, gti)
    elif mode == "display":
        comparator = None
        if options.comparator != None:
            comparator = comparators.get_module(options.comparator)
            comparator.set_param(options.comp_param)

        core.display(toscore_filename, toscore_parser,
                     groundtruth_filename, groundtruth_parser, options.img_path,
                     options.gtignore, gti, None, None, comparator)
    elif mode == "ROC" or mode == "DET":
        (multi_result, ts) = core.multi_scoring(toscore_filename,
                                                toscore_parser,
                                                groundtruth_filename,
                                                groundtruth_parser, comparator,
                                                options.crawl, options.sampling,
                                                options.confidence_min,
                                                gti)
        if mode == "ROC":
            core.plot_ROC(groundtruth_parser, len(ts), multi_result,
                          options.saving_file, options.show_curve,
                          options.xmin, options.ymin, options.xmax,
                          options.ymax, options.grid_major, options.grid_minor)
        elif mode == "DET":
            core.plot_DET(groundtruth_parser, len(ts), multi_result,
                          options.saving_file, options.show_curve,
                          options.xmin, options.ymin, options.xmax,
                          options.ymax, options.grid_major, options.grid_minor)
