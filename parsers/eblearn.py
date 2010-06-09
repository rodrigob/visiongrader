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

from dataset import DataSet, DataSetMulti
from objects import BoundingBox
import os
import os.path

name = "eblearnParser"

data_type = "images"

drop_neg = True
negs = "/home/myrhev32/visiongrader/visiongrader/data/inria/INRIAPerson/Test/neg"

def desctibe():
    return "Parser for eblearn result files"

def recognize(file):
    return False

def parse(filen, crawl = False):
    raise NotImplementedError()
    file = open(filen, "r")
    ret = DataSet()
    for line in file:
        line = line.strip().rstrip()
        splited = line.split()
        filename = splited[0]
        filename = filename[filename.rfind("/")+1:]
        filename = filename[:filename.rfind(".")]
        class_id = int(splited[1])
        (confidence, x, y, x2, y2) = tuple([float(a) for a in splited[2:]])
        if confidence > 1.5: #TODO
            ret.add_obj(filename, BoundingBox(x, y, x2, y2))
    file.close()
    return ret

def parse_multi_file(filen, ret = None):
    file = open(filen, "r")
    if ret == None:
        ret = DataSetMulti()
    if drop_neg:
        negs_files = [f[:f.rfind(".")] for f in os.listdir(negs)]
    for line in file:
        line = line.strip().rstrip()
        splited = line.split()
        filename = splited[0]
        filename = filename[filename.rfind("/")+1:]
        filename = filename[:filename.rfind(".")]
        if drop_neg:
            if filename in negs_files:
                continue
        class_id = int(splited[1])
        (confidence, x, y, x2, y2) = tuple([float(a) for a in splited[2:]])
        ret.add_obj(confidence, filename, BoundingBox(x, y, x2, y2))
    file.close()
    return ret

def parse_multi(filen, crawl = False):
    if not crawl:
        return parse_multi_file(filen)
    else:
        ret = DataSetMulti()
        for (root, dirs, files) in os.walk(filen):
            for file in [os.path.join(root, file) for file in files if file == "bbox.txt"]:
                parse_multi_file(file, ret)
        return ret
