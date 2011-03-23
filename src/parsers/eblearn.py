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
import sys

name = "eblearnParser"
data_type = "images"
path_is_folder = False
whratio = None # force bbox width to be height * whratio
hratio = None # force bbox height to be height * hratio
wratio = None # force bbox width to be width * wratio
min_area = None
max_area = None
min_area_ratio = None
max_area_ratio = None

drop_neg = False
negs = "/home/myrhev/visiongrader/visiongrader/data/inria/INRIAPerson/Test/neg"
if not os.path.exists(negs):
    print "Please specify the negs path in parsers/eblearn (TODO)"
parse_confidence_min = 1

def describe():
    return "Eblearn bounding boxes parser, min_area: " + str(min_area) \
        + " max_area: " + str(max_area)

def recognize(file):
    return False

def parse(filen, crawl = False):
    file = open(filen, "r")
    ret = DataSet()
    for line in file:
        line = line.strip().rstrip()
        splited = line.split()
        filename = splited[0]
        # filename = filename[filename.rfind("/")+1:]
        # filename = filename[:filename.rfind(".")]
        height = int(splited[1])
        width = int(splited[2])
        class_id = int(splited[3])
        (confidence, x, y, x2, y2) = tuple([float(a) for a in splited[4:]])
        #if confidence > parse_confidence_min: #TODO
        if hratio != None:
            height = y2 - y
            height2 = height * hratio
            y += (height - height2) / 2.0
            y2 = y + height2
        if wratio != None:
            width = x2 - x
            width2 = width * wratio
            x += (width - width2) / 2.0
            x2 = x + width2
        if whratio != None:
            height = y2 - y
            width = x2 - x
            width2 = height * whratio
            x += (width - width2) / 2.0
            x2 = x + width2
        bb = BoundingBox(x, y, x2, y2)
        area = bb.area()
        if (min_area == None or area >= min_area) and \
                (max_area == None or area <= max_area):
            ret.add_obj(filename, bb)
    file.close()
    return ret

def parse_multi_file(filen, ret = None, groundtruth = None):
    file = open(filen, "r")
    if ret == None:
        ret = DataSetMulti()
    if drop_neg:
        negs_files = [f[:f.rfind(".")] for f in os.listdir(negs)]
    i = 0
    for line in file:
        line = line.strip().rstrip()
        splited = line.split()
        filename = splited[0]
        # filename = filename[filename.rfind("/")+1:]
        # filename = filename[:filename.rfind(".")]
        if drop_neg:
            if filename in negs_files:
                continue
        height = int(splited[1])
        width = int(splited[2])
        class_id = int(splited[3])
        (confidence, x, y, x2, y2) = tuple([float(a) for a in splited[4:]])
        if hratio != None:
            height = y2 - y
            height2 = height * hratio
            y += (height - height2) / 2.0
            y2 = y + height2
        if wratio != None:
            width = x2 - x
            width2 = width * wratio
            x += (width - width2) / 2.0
            x2 = x + width2
        if whratio != None:
            height = y2 - y
            width = x2 - x
            width2 = height * whratio
            x += (width - width2) / 2.0
            x2 = x + width2
        bb = BoundingBox(x, y, x2, y2, confidence)
        if groundtruth != None:
            img = groundtruth[filename]
            if img == []:
                print "warning: " + filename + " not found in groundtruth."
                continue ;
            # r = bb.area() / (img.height * img.width)
            # if (min_area_ratio != None and r < min_area_ratio) or \
            #     (max_area_ratio != None and r > max_area_ratio):
            #     print "not adding ratio " + str(r)
            #     continue            
        area = bb.area()
        if (min_area == None or area >= min_area) and \
                (max_area == None or area <= max_area):
            ret.add_obj(confidence, filename, bb)
            i = i + 1
    file.close()
    return ret

# Find all 'bbox.txt' files within a directory (recursively??)
def parse_multi(filen, crawl = False, groundtruth = None):
    if not crawl:
        return parse_multi_file(filen, None, groundtruth)
    else:
        ret = DataSetMulti()
        for (root, dirs, files) in os.walk(filen):
            for file in [os.path.join(root, file)
                         for file in files if file == "bbox.txt"]:
                parse_multi_file(file, ret, groundtruth)
        return ret

def get_img_from_name(name, annotations_path, images_path):
    possible_paths = []
    if images_path != None:
        possible_paths.append(os.path.join(images_path, name))
        possible_paths.append(os.path.join(images_path, name + ".png"))
        possible_paths.append(os.path.join(images_path, name + ".pgm"))
        possible_paths.append(os.path.join(images_path, name + ".jpg"))
    for path in possible_paths:
        if os.path.exists(path):
            return path
    sys.stderr.write("tried: %s\n"%(os.path.join(images_path, name + ".pgm"),))
    sys.stderr.write("%s : image not found.\n"%(name,))
    raise StandardError()
