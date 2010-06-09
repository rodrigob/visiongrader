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

from dataset import DataSet
from objects import BoundingBox, WholeImage
import os
import os.path

data_type = "posneg"

name = "INRIA_Bool_Parser"

def describe():
    return "Parser for the pos/neg INRIA pedestrian dataset"

def recognize(file):
    return False

def parse(path, crawl = False):
    if crawl == True:
        raise StandardError()
    pos_filename = os.path.join(path, "pos.lst")
    neg_filename = os.path.join(path, "neg.lst")
    pos_dir = os.path.join(path, "pos")
    neg_dir = os.path.join(path, "neg")
    if not os.path.isfile(pos_filename):
        print "%s is not a file."%(pos_filename,)
        return None
    if not os.path.isfile(neg_filename):
        print "%s is not a file."%(neg_filename,)
        return None
    if not os.path.isdir(pos_dir):
        print "%s is not a directory."%(pos_dir,)
        return None
    if not os.path.isdir(neg_dir):
        print "%s is not a directory."%(neg_dir,)
        return None

    ret = DataSet()
    pos = open(pos_filename, "r")
    pos_names = [line[line.rfind("/")+1:] for line in pos.read().split()]
    pos.close()
    for name in pos_names:
        filename = os.path.join(pos_dir, name)
        ret.add_obj(name, WholeImage(name))

    neg = open(neg_filename, "r")
    neg_names = [line[line.rfind("/")+1:] for line in neg.read().split()]
    neg.close()
    for name in neg_names:
        ret.add_empty_image(name)
        
    return ret
