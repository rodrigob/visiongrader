from dataset import DataSetMulti
from objects import BoundingBox
import os
import os.path
import name_converter

data_type = "images"

name = "CaltechParser"

def describe():
    return "Parser for the Caltech results."

def recognize(file):
    return False

def parse_file_multi(file, filename, dataset):
    for line in file:
        (x, y, w, h, score) = tuple([float(a) for a in line.strip().rstrip().split(",")])
        dataset.add_obj(score, name_converter.corresp[filename], BoundingBox(x, y, x+w, y+h))

def parse_multi(path, crawl = None):
    ret = DataSetMulti()
    filenames = os.listdir(path)
    for filename in filenames:
        #TODO : check validity
        file = open(os.path.join(path, filename), "r")
        parse_file_multi(file, filename[:filename.rfind(".")], ret)
        file.close()
    #print ret
    return ret
