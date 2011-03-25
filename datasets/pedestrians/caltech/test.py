#!/usr/bin/python

import sys
import os
 
# parameters
vgsrc = os.path.dirname(os.path.abspath(__file__)) + '/../../../src/'
gt_parser = '--groundtruth_parser eblearn --gt_whratio .43'
sampling = "--sampling 50" # curve approx to avoid computing all possible thresh
format = '--xmin 0.003 --xmax 102 --ymin 0.01 --ymax 1.1'
compare = '--comparator overlap50percent --comparator_param .5'
caltech_input_parser = '--input_parser caltech'
eblearn_input_parser = '--input_parser eblearn'
caltech_subdir = 'set01/V000'
legend = '--xlegend \"False positives per image (FPPI)\" --ylegend \"Miss rate\"'
grid = '--grid_major --grid_minor'
newcurve_hresize = ''#'--hratio .75'
newcurve_wresize = ''#'--wratio .5'

ds = os.environ['HOME'] + '/projects/ped/caltech/samples/med'
annotations = os.path.join(ds, 'set05_select.txt')
input = os.path.join(ds, 'selected/bbox.txt')
newcurve_name = os.path.basename(input)
outdir = os.path.dirname(input) # directory where to look for existing curves

# compute curve
cmd = os.path.join(vgsrc, 'main.py') \
    + ' --input ' + input \
    + ' ' + eblearn_input_parser + ' ' + gt_parser + ' --det' \
    + ' --images_path ' + ds \
    + ' --groundtruth ' + annotations \
    + ' ' + compare + ' ' + ' ' \
    + ' ' + sampling + ' ' + format \
    + ' --saving-file ' + os.path.join(outdir, newcurve_name) + '.pickle' \
    + ' --show-no-curve ' + newcurve_hresize + ' ' + newcurve_wresize
os.system(cmd)
exit(1)

# show db
cmd = os.path.join(vgsrc, 'main.py') \
    + ' --input ' + input + ' --input_parser eblearn '\
    + ' --groundtruth_parser eblearn  --disp' \
    + ' --images_path ' + ds + ' --groundtruth ' + annotations \
    + ' ' + compare + ' '# + resize_cmd
os.system(cmd)
exit(1)

# uber parameters
ds = '/data/pedestrians/caltech'
ds_type = 'Test'
extract_newcurve = True
extract_caltech = False
show_caltech_db = False
show_caltech_db1 = 'set05' #'HOG' # show 1 caltech db
show_all_curves = True
show_newcurve_db = False

# check number of input arguments
if len(sys.argv) !=  2:
    print 'Expected 1 argument, the eblearn bbox file'
    raise
# expected arguments:
newcurve = sys.argv[1] # the eblearn bbox output file
newcurve_name = os.path.basename(sys.argv[1])
outdir = os.path.dirname(newcurve) # directory where to look for existing curves
ds_vg = os.path.dirname(os.path.abspath(__file__))
ds_ignore = os.path.join(os.path.join(ds_vg, 'ignore'), ds_type)
ds_caltech = os.path.join(ds_vg, 'caltech')
ds_dir = os.path.join(ds, ds_type)
annotations = os.path.join(ds_dir, 'annotations')
ignore = '--ignore ' + ds_ignore

# print configuration
print 'vision grader sources: ' + vgsrc
print 'ds ignore data: ' + ds_ignore
print 'ds annotations: ' + annotations

# list of algorithms to resize
caltech_resize = ('HOG', 'FtrMine', 'Shapelet-orig', 'PoseInv', 'PoseInvSvm',
    'HikSvm')
caltech_hresize = '--hratio ' + str(100.0 / 128.0)
caltech_wresize = '--wratio ' + str(43.0 / 64.0)
#caltech_wresize = '--whratio .43'

################################################################################
# show database for 1 specific algo

if show_caltech_db1 != '':
    algo = show_caltech_db1
    algo_dir = os.path.join(ds_caltech, os.path.join(algo, caltech_subdir))
    # check if algo needs to be resized
    resize_cmd = ""
    if algo in caltech_resize:
	resize_cmd = str(caltech_hresize) + ' ' + str(caltech_wresize)
	print 'Resizing algo ' + algo + ' with: ' + resize_cmd
    # start viewer for this algo
    cmd = os.path.join(vgsrc, 'main.py') \
	+ ' --input ' + algo_dir \
    	+ ' ' + caltech_input_parser + ' ' + gt_parser + ' --disp' \
    	+ ' --images_path ' + annotations + ' --groundtruth ' + annotations \
	+ ' ' + compare + ' ' + ignore + ' ' + resize_cmd
    os.system(cmd)

################################################################################
# generate caltech algos curves

if extract_caltech:
    for algo in os.listdir(ds_caltech):
       algo_full = os.path.join(ds_caltech, algo)
       if not os.path.isdir(algo_full):
	   continue
       algo_dir = os.path.join(algo_full, caltech_subdir)
       print "______________________________________________________________"
       print 'Processing algorithm ' + algo + ' from ' + algo_dir
       # check if algo needs to be resized
       resize_cmd = ""
       if algo in caltech_resize:
	   resize_cmd = str(caltech_hresize) + ' ' + str(caltech_wresize)
	   print 'Resizing algo ' + algo + ' with: ' + resize_cmd
       # start viewer for this algo
       cmd = os.path.join(vgsrc, 'main.py') \
	   + ' --input ' + algo_dir \
    	   + ' ' + caltech_input_parser + ' ' + gt_parser + ' --det' \
    	   + ' --images_path ' + annotations \
	   + ' --groundtruth ' + annotations \
	   + ' ' + compare + ' ' + ignore + ' ' + resize_cmd \
     	   + ' ' + sampling + ' ' + format \
	   + ' --saving-file ' + os.path.join(outdir, algo) + '.pickle' \
	   + ' --show-no-curve'
       os.system(cmd)
       # show images for this algo
       if show_caltech_db:
	   print "____________________________________________________________"
	   print "Showing images for " + algo
	   cmd = os.path.join(vgsrc, 'main.py') \
	       + ' --input ' + algo_dir \
    	       + ' ' + caltech_input_parser + ' ' + gt_parser + ' --disp' \
    	       + ' --images_path ' + annotations \
	       + ' --groundtruth ' + annotations \
	       + ' ' + compare + ' ' + ignore + ' ' + resize_cmd
	   os.system(cmd)

################################################################################

# generate curve for input bbox
if extract_newcurve:
    cmd = os.path.join(vgsrc, 'main.py') \
        + ' --input ' + newcurve \
        + ' ' + eblearn_input_parser + ' ' + gt_parser + ' --det' \
        + ' --images_path ' + annotations \
        + ' --groundtruth ' + annotations \
        + ' ' + compare + ' ' + ignore + ' ' \
        + ' ' + sampling + ' ' + format \
        + ' --saving-file ' + os.path.join(outdir, newcurve_name) + '.pickle' \
        + ' --show-no-curve ' + newcurve_hresize + ' ' + newcurve_wresize
    os.system(cmd)

# plot
if show_all_curves:
    cmd = os.path.join(vgsrc, 'plotpickle.py') \
        + ' --main_curve ' + newcurve + '.pickle' \
        + ' ' + format + ' ' + legend + ' ' + grid + ' ' + outdir + '/*.pickle'
    os.system(cmd)

# show db
if show_newcurve_db:
    cmd = os.path.join(vgsrc, 'main.py') \
        + ' --input ' + newcurve \
        + ' ' + eblearn_input_parser + ' ' + gt_parser + ' --disp' \
        + ' --images_path ' + annotations \
        + ' --groundtruth ' + annotations \
        + ' ' + compare + ' ' + ignore \
        + ' ' + newcurve_hresize + ' ' + newcurve_wresize
    os.system(cmd)

################################################################################
