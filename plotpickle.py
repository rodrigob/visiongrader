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

import pylab
import cPickle
import sys
import optparse
import os
import os.path

n_colors = 6
colors = ['b', 'g', 'c', 'm', 'y', 'k']
i = 0

toplot = []

def plot(arg, main = False):
    global i
    f = open(arg, "r")
    points = cPickle.load(f)
    f.close()
    label = arg
    if label.find(".") != -1:
        label = label[:label.rfind(".")]
    if label.find("/") != -1:
        label = label[label.rfind("/")+1:]
    color = colors[i%6]
    width = 1
    if main == True:
        style = "-"
        color = "r"
        width = 2
        i -= 1
    elif i < n_colors:
        style = "-"
    elif i < 2*n_colors:
        style = "--"
    elif i < 3*n_colors:
        style = ":"
    else:
        style = "-."
    i += 1
    index = i
    toplot.append([index, [a[0] for a in points], [- a[1] for a in points],
                   style, color, label, width])

if __name__=="__main__":
    usage = "usage: %prog [-m main_curve] [OPTIONS] [--help]\n       %prog --help"
    optp = optparse.OptionParser(add_help_option = True, usage = usage, prog = "./plotpickle.py")
    optp.add_option("-m", "--main_curve", dest = "main_curve", default = None, type = "str",
                    help = "Main curve.")
    optp.add_option("--xlegend", dest = "x_legend", default = None, type = "str",
                    help = "Legend on the x axis.")
    optp.add_option("--ylegend", dest = "y_legend", default = None, type = "str",
                    help = "Legend on the y axis.")
    optp.add_option("--xmin", dest = "xmin", default = None, type = "float",
                    help = "Minimum of the x axis.")
    optp.add_option("--xmax", dest = "xmax", default = None, type = "float",
                    help = "Maximum of the x axis.")
    optp.add_option("--ymin", dest = "ymin", default = None, type = "float",
                    help = "Minimum of the y axis.")
    optp.add_option("--ymax", dest = "ymax", default = None, type = "float",
                    help = "Maximum of the y axis.")
    optp.add_option("--legend_position", dest = "legend_position",
                    default = "lower_right", type = "str",
                    help = 'Position for the legend. Choices are either "best" to \
let pylab decide, or a combination of [lower center upper]_[left center right] \
eg. "lower_right".')
    (options, args) = optp.parse_args()
    for arg in [a for a in args if a != options.main_curve]:
        plot(arg)
    if os.path.exists(options.main_curve):
        plot(options.main_curve, True)
    else:
        print "Warning: %s does not exixts."%(option.main_curve,)
    toplot.sort()
    for p in toplot:
        pylab.loglog(p[1], p[2], p[3], color = p[4], label = p[5], linewidth = p[6])

    if options.legend_position == "best":
        pylab.legend(loc=0)
    elif options.legend_position == "center_center":
        pylab.legend(loc=10)
    else:
        (loc1, loc2) = options.legend_position.split("_")
        if (loc1 not in ["lower", "center", "upper"]) \
                or (loc2 not in ["left", "center", "right"]):
            sys.stderr.write("legend_position : invalid string.\n")
            sys.exit(0)
        pylab.legend(loc=loc1 + " " + loc2)
    if options.x_legend != None:
        pylab.xlabel(options.x_legend)
    if options.y_legend != None:
        pylab.ylabel(options.y_legend)
    if options.xmin != None:
        pylab.axis(xmin = options.xmin)
    if options.xmax != None:
        pylab.axis(xmax = options.xmax)
    if options.ymin != None:
        pylab.axis(ymin = options.ymin)
    if options.ymax != None:
        pylab.axis(ymax = options.ymax)
    
    pylab.show()
