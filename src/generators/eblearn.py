#!/usr/bin/python

import os
import os.path
import subprocess
import stat
import shutil
import sys

name = "eblearnGenerator"

def describe():
    return "The eblearn results generator"

def generate_conf(conf_src, conf_dst, threshold):
    if not os.path.isfile(conf_src):
        print "The conf file %s does not exists."%(conf_src,)
        sys.exit(0)
    shutil.copy(conf_src, conf_dst)
    conf_file = open(conf_dst, "r")
    conf = conf_file.read()
    conf_file.close()
    thres_begin = conf.find("threshold")
    thres_end = thres_begin + conf[thres_begin:].find("\n")
    equals = conf[:thres_end].rfind("=")
    conf = conf[:equals+1] + str(threshold) + conf[thres_end:]
    conf_file = open(conf_dst, "w")
    conf_file.write(conf)
    conf_file.close()

def generate_boxes(conf_path, bin_path, images_path, dst, temp_dir = "."):
    eblearn_bin = bin_path
    eblearn_best_conf = conf_path
    eblearn_command_line = "%s %s %s"%(eblearn_bin, eblearn_best_conf, images_path)
    os.system(eblearn_command_line)

    detections_path = temp_dir
    detection_dirs = []
    for filename in os.listdir(detections_path):
        if filename[0:10] == "detections":
            detection_dirs.append(filename)
    def compare(a, b):
        time_a = os.stat(os.path.join(detections_path, a))[stat.ST_MTIME]
        time_b = os.stat(os.path.join(detections_path, b))[stat.ST_MTIME]
        if time_a < time_b:
            return -1
        elif time_a == time_b:
            return 0
        else:
            return 1
    detection_dirs.sort(compare)
    shutil.copy(os.path.join(detections_path,
                             os.path.join(detection_dirs[-1], "bbox.txt")),
                dst)
    shutil.rmtree(os.path.join(detections_path, detection_dirs[-1]))

if __name__=="__main__":
    import optparse
    usage = "usage: %prog -c conf_file_model -b eblearn_bin [-t temp_dir] [-o output]"
    optparser = optparse.OptionParser(add_help_option = True, usage = usage,
                                      prog = "./eblearn.py")
    optparser.add_option("-c", "--conf_path", dest = "conf_path", default = None,
                         type = "str", help = "Path to the base conf file.")
    optparser.add_option("-t", "--temp_dir", dest = "temp_dir", default = ".",
                         type = "str", help = "Directory to store temporary files.")
    optparser.add_option("-o", "--output", dest = "output", default = "bbox.txt",
                         type = "str", help = "Name of the output.")
    optparser.add_option("-b", "--eblearn_bin", dest = "eblearn_bin", default = None,
                         type = "str", help = "Path to eblearn binary.")
    optparser.add_option("-i", "--images_input", dest = "images_dir", default = None,
                         type = "str", help = "Images directory.")
    (options, args) = optparser.parse_args()

    if options.conf_path == None or options.eblearn_bin == None \
           or options.images_dir == None:
        optparser.print_usage()
        sys.exit(0)

    new_conf_path = os.path.join(options.temp_dir, "best.conf")
    generate_conf(options.conf_path, new_conf_path, -1)
    generate_boxes(new_conf_path, options.eblearn_bin, options.images_dir,
                   options.output, options.temp_dir)
