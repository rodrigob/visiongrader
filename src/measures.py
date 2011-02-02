#!/usr/bin/python

# Copyright (C) 2011 Pierre Sermanet <pierre.sermanet@gmail.com>
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
#  Pierre Sermanet <pierre.sermanet@gmail.com>

# Compute maximum possible area under curve (AUC),
# assuming a rectangle area of height y0 and width x1 - x0
def auc_max(x0, y0, x1):
    return (x1 - x0) * y0

# Return the percentage of AUC over its maximum possible area, times 100.
def auc_percent(points, x0, y0, x1):
    return auc(points, x0, y0, x1) / auc_max(x0, y0, x1) * 100

# Return the area under curve (AUC) of curve defined by 'points'
# in the [x0, x1] x-range and [0, y0] y-range.
def auc(points, x0, y0, x1):
    # we assume that points are ordered in increasing x order
    minx = points[0][0]
    minxy = -points[0][1]
    maxx = points[len(points) - 1][0]
    maxxy = -points[len(points) - 1][1]
#    print label + ": min x: " + str(minx) + " (y: " + str(minxy) \
#        + ") max x: " + str(maxx) + " (y: " + str(maxxy) + ")"
    auc = 0
    # build integral of curve
    # special cases: integral's limits
    # TODO: we assume x0 is always 0 and points don't go below 0 for now,
    # handle when many points can be below whatever x0's value
    if minx > x0: # fill integral gap between x0 and minx with y0
        auc += y0 * (minx - x0)
    # loop on all points
    p0x = minx
    p0y = minxy
    for p in points:
        p1x = p[0]
        p1y = -p[1]
        # stop if p1x is beyond x1
        if p1x >= x1:
            # interpolate point to the x limit
            y1 = p0y + (p1y - p0y) * (x1 - p0x)
            auc += ((x1 - p0x) / 2) * (y1 + p0y)
            # stop loop
            break
        # update auc with trapezoid
        auc += ((p1x - p0x) / 2) * (p1y + p0y)
        # shift p1 to p0
        p0x = p1x
        p0y = p1y
    # special case: end limit
    if p1x < x1: # fill integral gap between maxx and x1 with maxxy
        auc += p1y * (x1 - p1x)
    return auc
