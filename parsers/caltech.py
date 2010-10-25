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

from dataset import DataSetMulti
from objects import BoundingBox
import os
import os.path

data_type = "images"

name = "CaltechParser"

path_is_folder = True

def describe():
    return "Parser for the Caltech results."

def recognize(file):
    return False

#pos_path = "/home/myrhev32/visiongrader/visiongrader/data/inria/INRIAPerson/Test/pos"
pos_path = "/data/pedestrians/inria/INRIAPerson/Test/pos"

try:
    pos = os.listdir(pos_path)
    pos.sort()

    corresp = {}
    for i in xrange(len(pos)):
        corresp["I%05d"%(i)] = pos[i][:pos[i].rfind(".")]
except OSError:
    print "Warning : caltech parser won't be available. Please set pos_path to the path to INRIAPerson positives, such as inria/INRIAPerson/Test/pos"

def parse_file_multi(file, filename, dataset):
    for line in file:
        (x, y, w, h, score) = tuple([float(a) for a in line.strip().rstrip().split(",")])
        dataset.add_obj(score, corresp[filename], BoundingBox(x, y, x+w, y+h, score))

def parse_multi(path, crawl = False):
    if crawl == True:
        raise StandardError()
    ret = DataSetMulti()
    filenames = os.listdir(path)
    for filename in filenames:
        #TODO : check validity
        file = open(os.path.join(path, filename), "r")
        parse_file_multi(file, filename[:filename.rfind(".")], ret)
        file.close()
    #print ret
    return ret
