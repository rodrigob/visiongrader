from dataset import DataSet
from objects import BoundingBox

name = "eblearnParser"

def desctibe():
    return "Parser for eblearn result files"

def recognize(file):
    return False

def parse(file):
    ret = DataSet()
    for line in file:
        line = line.strip().rstrip()
        splited = line.split()
        filename = splited[0]
        filename = filename[filename.rfind("/")+1:]
        class_id = int(splited[1])
        (confidence, x, y, w, h) = tuple([float(a) for a in splited[2:]])
        #TODO confidence
        ret.add_obj(filename, BoundingBox(x, y, x + w, y + h))
    return ret
