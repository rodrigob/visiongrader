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
from objects import BoundingBox
import os
import os.path
import sys

data_type = "images"

name = "INRIA_Parser"

def describe():
    return "Parser for the INRIA pedestrian dataset."

def recognize(file):
    return False

def get_object(data, i):
    xmin, xmax, ymin, ymax = None, None, None, None
    object_char = data.find("object %d"%(i,))
    while object_char != -1:
        begin_line = data[:object_char].rfind("\n") + 1
        end_line = begin_line+1 + data[begin_line+1:].find("\n")
        line = data[begin_line:end_line]
        if line.find("Bounding box") != -1:
            # if this happens, there are other objects than pedestrians in the annotation :
            assert(line.find("PASperson") != -1)
            box_begin = line.rfind(":") + 1
            box_str = line[box_begin:]
            box_str = box_str[box_str.find("(")+1:].strip()
            xmin = int(box_str[:box_str.find(",")].strip().rstrip())
            box_str = box_str[box_str.find(",")+1:].strip()
            ymin = int(box_str[:box_str.find(")")].strip().rstrip())
            box_str = box_str[box_str.find("(")+1:].strip()
            xmax = int(box_str[:box_str.find(",")].strip().rstrip())
            box_str = box_str[box_str.find(",")+1:].strip()
            ymax = int(box_str[:box_str.find(")")].strip().rstrip())
            break
        object_char = object_char+1 + data[object_char+1:].find("object %d"%(i,))
    if xmin == None:
        return None
    return BoundingBox(xmin, ymin, xmax, ymax)

def parse_file(file):
    ret = []
    i = 1
    data = file.read()
    bbox = get_object(data, i)
    while bbox != None:
        ret.append(bbox)
        i += 1
        bbox = get_object(data, i)
    return ret

def parse(path, crawl = False):
    if crawl == True:
        raise StandardError()
    ret = DataSet()
    filenames = os.listdir(path)
    for filename in filenames:
        #TODO : check validity
        file = open(os.path.join(path, filename), "r")
        bboxes = parse_file(file)
        file.close()
        filename = filename[:filename.rfind(".")]
        for bbox in bboxes:
            ret.add_obj(filename, bbox)
    return ret

def get_img_from_name(name, annotations_path, images_path):
    possible_paths = []
    if images_path != None:
        possible_paths.append(os.path.join(images_path, name + ".png"))
    possible_paths.append(os.path.join(os.path.join(annotations_path, ".."),
                                       os.path.join("pos", name + ".png")))
    possible_paths.append(os.path.join(os.path.join(annotations_path, ".."),
                                       os.path.join("neg", name + ".png")))
    for path in possible_paths:
        if os.path.exists(path):
            return path
    sys.stderr.write("%s : image not found.\n"%(name,))
    raise StandardError()
