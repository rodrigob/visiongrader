import os
import os.path
import subprocess
import stat
import shutil

name = "eblearnGenerator"

def describe():
    return "The eblearn results generator"

def generate(threshold, destination):
    #set the config file
    eblearn_path = "/home/mfm352/eblearn/current/eblearn"
    conf_path = os.path.join(eblearn_path, "demos/obj/face/trained/best.conf")
    conf_file = open(conf_path, "r")
    conf = conf_file.read()
    conf_file.close()
    thres_begin = conf.find("threshold")
    thres_end = thres_begin + conf[thres_begin:].find("\n")
    equals = conf[:thres_end].rfind("=")
    conf = conf[:equals+1] + str(threshold) + conf[thres_end:]
    conf_file = open(conf_path, "w")
    conf_file.write(conf)
    conf_file.close()

    eblearn_bin = os.path.join(eblearn_path, "bin/objdetect")
    eblearn_best_conf = os.path.join(eblearn_path, "demos/obj/face/trained/best.conf")
    images = "/home/mfm352/scolearn/data/CMU/test/"
    eblearn_command_line = "%s %s %s"%(eblearn_bin, eblearn_best_conf, images)
    eblearn = subprocess.Popen([eblearn_command_line], shell = True,
                               stdout = subprocess.PIPE)
    eblearn.wait()
    print eblearn.stdout.read()

    detections_path = "."
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
                destination)
    

generate(-0.6, ".")
