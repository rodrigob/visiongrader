import os

pos_path = "/home/myrhev32/visiongrader/visiongrader/data/inria/INRIAPerson/Test/pos"

try:
    pos = os.listdir(pos_path)
    pos.sort()

    corresp = {}
    for i in xrange(len(pos)):
        corresp["I%05d"%(i)] = pos[i][:pos[i].rfind(".")]
except OSError:
    print "Warning : caltech parser won't be available. Please set pos_path to the path to INSIAPerson positives, such as inria/INRIAPerson/Test/pos"
