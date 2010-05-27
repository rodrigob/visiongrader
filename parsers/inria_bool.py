from dataset import DataSet
from objects import BoundingBox
import os
import os.path

data_type = "posneg"

name = "INRIA_Bool_Parser"

def describe():
    return "Parser for the pos/neg INRIA pedestrian dataset"

def recognize(file):
    return False

def parse(path):
    pos_filename = os.join(path, "pos.lst")
    neg_filename = os.join(path, "neg.lst")
    pos_dir = os.join(path, "pos")
    neg_dit = os.join(path, "neg")
    if not os.path.isfile(pos_filename):
        print "%s is not a file."%(pos_filename,)
        return None
    if not os.path.isfile(neg_filename):
        print "%s is not a file."%(neg_filename,)
        return None
    if not os.path.isfile(pos_dir):
        print "%s is not a directory."%(pos_dir,)
        return None
    if not os.path.isfile(neg_dir):
        print "%s is not a directory."%(neg_dir,)
        return None

    ret = DataSet()
    pos = open(pos_filename, "r")
    pos_names = [line[line.rfind("/"):] for line in pos.read().split()]
    pos.close()
    for name in pos_names:
        filename = os.join(pos_dir, name)
        ret.add_obj(name, WholeImage(name))

    neg = open(neg_filename, "r")
    neg_names = [line[line.rfind("/"):] for line in neg.read().split()]
    neg.close()
    for name in neg_names:
        ret.add_empty_image(name)
        
    return ret
