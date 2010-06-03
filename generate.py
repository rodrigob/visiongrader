import os
import os.path

path = "data/res"
dirs = os.listdir(path)
postpath = "set01/V000"
result_dir = "results"

for dir in dirs:
    datapath = os.path.join(os.path.join(path, dir), postpath)
    os.system("./main.py -i %s -t data/inria/INRIAPerson/Test/annotations --input_parser caltech --groundtruth_parser inria -c overlap50percent --det"%(datapath,))
    os.system("mv curve.pickle %s"%(os.path.join(result_dir, "%s.pickle"%(dir,)),))
