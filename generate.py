import os
import os.path
import optparse

optp = optparse.OptionParser()
optp.add_option("--result_dir", dest = "result_dir", default = None)
optp.add_option("--comparator", dest = "comparator", default = None)
optp.add_option("--eblearn", action = "store_true", dest = "eblearn")
(opts, args) = optp.parse_args()

path = "data/res"
dirs = os.listdir(path)
postpath = "set01/V000"
eblpath = "bbox/20100603.123705.ped_test_duncana_16"

result_dir = opts.result_dir
comparator = opts.comparator

assert(result_dir != None)
assert(comparator != None)

if opts.eblearn:
    os.system("./main.py -i %s -t data/inria/INRIAPerson/Test/annotations --input_parser eblearn --groundtruth_parser inria -c %s --det --crawl"%(eblpath,comparator))
    os.system("mv curve.pickle %s"%(os.path.join(result_dir, "eblearn.pickle"),))
else:
    for dir in dirs:
        datapath = os.path.join(os.path.join(path, dir), postpath)
        os.system("./main.py -i %s -t data/inria/INRIAPerson/Test/annotations --input_parser caltech --groundtruth_parser inria -c %s --det"%(datapath,comparator))
        os.system("mv curve.pickle %s"%(os.path.join(result_dir, "%s.pickle"%(dir,)),))
