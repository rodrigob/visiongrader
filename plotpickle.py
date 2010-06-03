import pylab
import cPickle
import sys

i = 0
def plot(arg):
    global i
    f = open(arg, "r")
    points = cPickle.load(f)
    f.close()
    label = arg
    if label.find(".") != -1:
        label = label[:label.rfind(".")]
    if label.find("/") != -1:
        label = label[label.rfind("/")+1:]
    if i < 7:
        style = "-"
    elif i < 14:
        style = "--"
    elif i < 21:
        style = ":"
    else:
        style = "-."
    i += 1
    pylab.loglog([a[0] for a in points], [- a[1] for a in points], style, label = label)

for arg in [a for a in sys.argv[1:] if a.find("eblearn") == -1]:
    plot(arg)
for arg in [a for a in sys.argv[1:] if a.find("eblearn") != -1]:
    plot(arg)
pylab.legend(loc=3)
pylab.xlabel("False positives per image")
pylab.ylabel("Miss rate")
pylab.show()
