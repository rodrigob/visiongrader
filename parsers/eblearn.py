from dataset import DataSet
from objects import BoundingBox

name = "eblearnParser"

def desctibe():
    return "Parser for eblearn result files"

def recognize(file):
    return False

def parse(file, threshold = -0.6):
    ret = DataSet()
    for line in file:
        line = line.strip().rstrip()
        splited = line.split()
        filename = splited[0]
        filename = filename[filename.rfind("/")+1:]
        class_id = int(splited[1])
        (confidence, x, y, x2, y2) = tuple([float(a) for a in splited[2:]])
        if confidence > threshold:
            ret.add_obj(filename, BoundingBox(x, y, x2, y2))
    return ret
