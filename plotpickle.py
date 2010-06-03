import pylab
import cPickle
import sys

for arg in sys.argv[1:]:
    f = open(arg, "r")
    points = cPickle.load(f)
    f.close()
    pylab.loglog([a[0] for a in points], [- a[1] for a in points], label = arg[:arg.find(".")])
pylab.legend(loc=3)
pylab.xlabel("False positives per image")
pylab.ylabel("Miss rate")
pylab.show()
