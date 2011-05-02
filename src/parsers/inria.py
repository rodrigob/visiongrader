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
path_is_folder = True
whratio = None # force bbox width to be height * whratio
min_area = None
max_area = None
min_area_ratio = None
max_area_ratio = None

def describe():
    return "INRIA pedestrian dataset parser, forcing width to height * " \
        + str(whratio) + ", min area: " + str(min_area) + " max area: " \
        + str(max_area)

def recognize(file):
    return False

def parse_header(data):
    # get filename
    object_char = data.find("Image filename : \"")
    filename = data[object_char + data[object_char:].find("\"") + 1:]
    filename = filename[ : filename.find("\"") ]
    # get image sizes
    object_char = data.find("Image size (X x Y x C) : ")
    line = data[object_char + data[object_char:].find(": ") + 2:]
    width = int(line[:line.find(" ")])
    line = line[line.find(" x ") + 3:]
    height = int(line[:line.find(" ")])
    line = line[line.find(" x ") + 3:]
    chans = int(line[:line.find("\n")])
    # return all info
    return (filename, width, height, chans)

def get_object(data, i):
    xmin, xmax, ymin, ymax = None, None, None, None
    object_char = data.find("object %d"%(i,))
    while object_char != -1:
        begin_line = data[:object_char].rfind("\n") + 1
        end_line = begin_line+1 + data[begin_line+1:].find("\n")
        line = data[begin_line:end_line]
        if line.find("Bounding box") != -1:
            # if this happens, there are other objects than pedestrians
            # in the annotation :
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
        object_char = object_char+1 \
            + data[object_char+1:].find("object %d"%(i,))
    if xmin == None:
        return None
    if whratio != None:
        height = ymax - ymin
        width = xmax - xmin
        width2 = height * whratio
        xmin += (width - width2) / 2.0
        xmax = xmin + width2
    return BoundingBox(xmin, ymin, xmax, ymax, 1.0)

def parse_file(fname):
    file = open(fname, "r")
    # parse header
    data = file.read()
    (fn, width, height, chans) = parse_header(data)
    # parse boxes
    boxes = []
    i = 1
    bbox = get_object(data, i)
    while bbox != None:
        boxes.append(bbox)
        i += 1
        bbox = get_object(data, i)    
    file.close()
    return (fn, width, height, chans, boxes)

def parse(path, crawl = False):
    if crawl == True:
        raise StandardError()
    ret = DataSet()
    filenames = os.listdir(path)
    for filename in filenames:
        #TODO : check validity
        (fname, width, height, chans, bboxes) \
            = parse_file(os.path.join(path, filename))
        fname = os.path.basename(fname)
        for bbox in bboxes:
            ret.add_obj(fname, bbox, height, width)
    return ret

def find_minmax_areas(path, crawl = False):
    min_area = None
    max_area = None
    min_area_ratio = None
    max_area_ratio = None
    if crawl == True:
        raise StandardError()
    ret = DataSet()
    filenames = os.listdir(path)
    for filename in filenames:
        #TODO : check validity
        (fn, w, h, chans, bboxes) = parse_file(os.path.join(path, filename))
        filename = fn #filename[:filename.rfind(".")]
        for bbox in bboxes:
            area = bbox.area()
            area_ratio = bbox.area() / (w * h)
            if min_area == None or area < min_area:
                min_area = area
            if max_area == None or area > max_area:
                max_area = area
            if min_area_ratio == None or area_ratio < min_area_ratio:
                min_area_ratio = area_ratio
            if max_area_ratio == None or area_ratio > max_area_ratio:
                max_area_ratio = area_ratio
    print "min area: " + str(min_area) + " max_area: " + str(max_area) \
        + " min_area_ratio: " + str(min_area_ratio) + " max_area_ratio: " \
        + str(max_area_ratio)
    areas = []
    areas.append(min_area)
    areas.append(max_area)
    areas.append(min_area_ratio)
    areas.append(max_area_ratio)
    return areas

def get_img_from_name(name, annotations_path, images_path):
    possible_paths = []
    if images_path != None:
        possible_paths.append(os.path.join(images_path, name + ".png"))
        possible_paths.append(os.path.join(images_path, name + ".jpg"))
    possible_paths.append(os.path.join(images_path, name))
    possible_paths.append(os.path.join(os.path.join(annotations_path, ".."),
                                       os.path.join("neg", name + ".png")))
    possible_paths.append(os.path.join(os.path.join(annotations_path, ".."),
                                       os.path.join("pos", name + ".jpg")))
    possible_paths.append(os.path.join(os.path.join(annotations_path, ".."),
                                       os.path.join("neg", name + ".jpg")))
    for path in possible_paths:
        if os.path.exists(path):
            return path
    sys.stderr.write("%s : image not found.\n"%(name,))
    raise StandardError()

def save_bboxes(target_fname, imfname, imsize, boxes):
    print 'Saving reference to ' + imfname + ' (' + str(imsize[0]) + 'x' \
        + str(imsize[1]) + 'x' + str(imsize[2]) + ') to ' + target_fname \
        + ' with ' + str(len(boxes)) + ' bboxes: ' + str(boxes)
    s = '# PASCAL Annotation Version 1.00\n\nImage filename : \"' \
        + imfname + '\"\nImage size (X x Y x C) : ' + str(imsize[0]) + ' x ' \
        + str(imsize[1]) + ' x ' + str(imsize[2]) \
        + '\nDatabase : \"INRIA pedestrians to ignore\"\n' \
        + 'Objects with ground truth : ' + str(len(boxes)) + ' { '
    objname = '\"PASperson\"'
    for b in boxes:
        s += objname + ' '
    s += '}\n\n'
    i = 1
    for b in boxes:
        s += 'Bounding box for object ' + str(i) + ' ' + objname \
            + ' (Xmin, Ymin) - (Xmax, Ymax) : (' \
            + str(int(b.getX1())) + ', ' + str(int(b.getY1())) + ') - (' \
            + str(int(b.getX2())) + ', ' + str(int(b.getY2())) + ')\n'
        print 'Saving box: ' + str(b)
        i += 1
    # write file
    file = open(target_fname, "w")
    file.write(s)
    file.close()
