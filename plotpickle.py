import pylab
import cPickle
import sys

n_colors = 6
colors = ['b', 'g', 'c', 'm', 'y', 'k']
xmin = 0.003
xmax = 200
ymin = 0.04
ymax = 1.01
i = 0
def get_y1(points):
    return int(float([-a[1] for a in points if a[0] <= 1][-1]) * 100.)

toplot = []

def plot(arg, main = False):
    global i
    f = open(arg, "r")
    points = cPickle.load(f)
    f.close()
    label = arg
    if label.find(".") != -1:
        label = label[:label.rfind(".")]
    if label.find("/") != -1:
        label = label[label.rfind("/")+1:]
    if label == "eblearn":
        label = "U+_tanh R+_tanh"
    label += " (%d%%)"%(get_y1(points),)
    color = colors[i%6]
    width = 1
    if main == True:
        style = "-"
        color = "r"
        width = 2
        i -= 1
    elif i < n_colors:
        style = "-"
    elif i < 2*n_colors:
        style = "--"
    elif i < 3*n_colors:
        style = ":"
    else:
        style = "-."
    i += 1
    toplot.append([[-get_y1(points), main], [a[0] for a in points],
                   [- a[1] for a in points], style,
                   color, label, width])

def plot_bar(x):
    pylab.plot([x, x], [ymin, ymax], color = 'k')

for arg in [a for a in sys.argv[1:] if a.find("eblearn") == -1]:
    plot(arg)
for arg in [a for a in sys.argv[1:] if a.find("eblearn") != -1]:
    plot(arg, True)
toplot.sort()
for p in toplot:
    pylab.loglog(p[1], p[2], p[3], color = p[4], label = p[5], linewidth = p[6])
plot_bar(1.0)

pylab.legend(loc=4)
pylab.xlabel("False positives per image")
pylab.ylabel("Miss rate")
pylab.axis(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax)
pylab.show()
