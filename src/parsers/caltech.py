# Copyright (C) 2010 Michael Mathieu <michael.mathieu@ens.fr>
# 
# This file is part of visiongrader.
# 
# visiongrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# visiongrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with visiongrader.  If not, see <http://www.gnu.org/licenses/>.
# 
# Authors :
#  Michael Mathieu <michael.mathieu@ens.fr>

from dataset import DataSetMulti
from objects import BoundingBox
import os
import os.path

data_type = "images"
name = "CaltechParser"
path_is_folder = True
hratio = None # force bbox height to be height * hratio
wratio = None # force bbox width to be width * wratio
whratio = None # force bbox width to be height * whratio

def describe():
    s = "Caltech bounding boxes parser"
    if hratio:
        s += ', resizing height to be ' + str(hratio) + ' * height'
    if wratio:
        s += ', resizing width to be ' + str(wratio) + ' * width'
    if whratio:
        s += ', resizing width to be ' + str(whratio) + ' * height'
    return s

def recognize(file):
    return False

#pos_path = "/home/myrhev32/visiongrader/visiongrader/data/inria/INRIAPerson/Test/pos"
pos_path = "/data/pedestrians/inria/INRIAPerson/Test/pos"

inria_list = 'Test/pos/crop001501.png Test/pos/crop001504.png Test/pos/crop001511.png Test/pos/crop001512.png Test/pos/crop001514.png Test/pos/crop001520.png Test/pos/crop001521.png Test/pos/crop001522.png Test/pos/crop001531.png Test/pos/crop001533.png Test/pos/crop001544.png Test/pos/crop001545.png Test/pos/crop001546.png Test/pos/crop001549.png Test/pos/crop001555.png Test/pos/crop001566.png Test/pos/crop001573.png Test/pos/crop001574.png Test/pos/crop001590.png Test/pos/crop001593.png Test/pos/crop001602.png Test/pos/crop001604.png Test/pos/crop001607.png Test/pos/crop001631.png Test/pos/crop001633.png Test/pos/crop001634.png Test/pos/crop001638.png Test/pos/crop001639.png Test/pos/crop001641.png Test/pos/crop001653.png Test/pos/crop001654.png Test/pos/crop001658.png Test/pos/crop001659.png Test/pos/crop001660.png Test/pos/crop001661.png Test/pos/crop001664.png Test/pos/crop001670.png Test/pos/crop001676.png Test/pos/crop001682.png Test/pos/crop001683.png Test/pos/crop001684.png Test/pos/crop001688.png Test/pos/crop001704.png Test/pos/crop001706.png Test/pos/crop001715.png Test/pos/crop001716.png Test/pos/crop001718.png Test/pos/crop001719.png Test/pos/crop001722.png Test/pos/crop001723.png Test/pos/crop001724.png Test/pos/crop001725.png Test/pos/crop_000001.png Test/pos/crop_000002.png Test/pos/crop_000003.png Test/pos/crop_000004.png Test/pos/crop_000005.png Test/pos/crop_000006.png Test/pos/crop_000007.png Test/pos/crop_000008.png Test/pos/crop_000009.png Test/pos/crop_000012.png Test/pos/crop_000013.png Test/pos/crop_000015.png Test/pos/crop_000016.png Test/pos/crop_000017.png Test/pos/crop_000018.png Test/pos/crop_000019.png Test/pos/crop_000020.png Test/pos/crop_000021.png Test/pos/crop_000023.png Test/pos/crop_000024.png Test/pos/crop_000025.png Test/pos/crop_000026.png Test/pos/crop_000027.png Test/pos/crop_000604.png Test/pos/person_007.png Test/pos/person_008.png Test/pos/person_009.png Test/pos/person_010.png Test/pos/person_011.png Test/pos/person_012.png Test/pos/person_013.png Test/pos/person_014.png Test/pos/person_015.png Test/pos/person_026.png Test/pos/person_028.png Test/pos/person_029.png Test/pos/person_030.png Test/pos/person_032.png Test/pos/person_033.png Test/pos/person_034.png Test/pos/person_036.png Test/pos/person_037.png Test/pos/person_038.png Test/pos/person_039.png Test/pos/person_040.png Test/pos/person_051.png Test/pos/person_052.png Test/pos/person_053.png Test/pos/person_055.png Test/pos/person_056.png Test/pos/person_058.png Test/pos/person_059.png Test/pos/person_062.png Test/pos/person_063.png Test/pos/person_064.png Test/pos/person_065.png Test/pos/person_070.png Test/pos/person_071.png Test/pos/person_073.png Test/pos/person_075.png Test/pos/person_076.png Test/pos/person_085.png Test/pos/person_087.png Test/pos/person_088.png Test/pos/person_089.png Test/pos/person_090.png Test/pos/person_092.png Test/pos/person_093.png Test/pos/person_094.png Test/pos/person_095.png Test/pos/person_096.png Test/pos/person_098.png Test/pos/person_099.png Test/pos/person_100.png Test/pos/person_104.png Test/pos/person_105.png Test/pos/person_107.png Test/pos/person_115.png Test/pos/person_118.png Test/pos/person_120.png Test/pos/person_122.png Test/pos/person_127.png Test/pos/person_132.png Test/pos/person_134.png Test/pos/person_135.png Test/pos/person_136.png Test/pos/person_137.png Test/pos/person_138.png Test/pos/person_159.png Test/pos/person_161.png Test/pos/person_164.png Test/pos/person_186.png Test/pos/person_188.png Test/pos/person_189.png Test/pos/person_190.png Test/pos/person_191.png Test/pos/person_193.png Test/pos/person_194.png Test/pos/person_198.png Test/pos/person_200.png Test/pos/person_204.png Test/pos/person_206.png Test/pos/person_207.png Test/pos/person_210.png Test/pos/person_212.png Test/pos/person_216.png Test/pos/person_217.png Test/pos/person_218.png Test/pos/person_222.png Test/pos/person_230.png Test/pos/person_236.png Test/pos/person_246.png Test/pos/person_247.png Test/pos/person_248.png Test/pos/person_249.png Test/pos/person_250.png Test/pos/person_251.png Test/pos/person_255.png Test/pos/person_263.png Test/pos/person_265.png Test/pos/person_272.png Test/pos/person_280.png Test/pos/person_282.png Test/pos/person_290.png Test/pos/person_293.png Test/pos/person_303.png Test/pos/person_306.png Test/pos/person_314.png Test/pos/person_315.png Test/pos/person_316.png Test/pos/person_317.png Test/pos/person_318.png Test/pos/person_323.png Test/pos/person_325.png Test/pos/person_335.png Test/pos/person_336.png Test/pos/person_337.png Test/pos/person_347.png Test/pos/person_350.png Test/pos/person_and_bike_004.png Test/pos/person_and_bike_006.png Test/pos/person_and_bike_012.png Test/pos/person_and_bike_014.png Test/pos/person_and_bike_027.png Test/pos/person_and_bike_028.png Test/pos/person_and_bike_029.png Test/pos/person_and_bike_035.png Test/pos/person_and_bike_038.png Test/pos/person_and_bike_042.png Test/pos/person_and_bike_043.png Test/pos/person_and_bike_044.png Test/pos/person_and_bike_045.png Test/pos/person_and_bike_046.png Test/pos/person_and_bike_047.png Test/pos/person_and_bike_048.png Test/pos/person_and_bike_049.png Test/pos/person_and_bike_050.png Test/pos/person_and_bike_051.png Test/pos/person_and_bike_052.png Test/pos/person_and_bike_053.png Test/pos/person_and_bike_054.png Test/pos/person_and_bike_055.png Test/pos/person_and_bike_056.png Test/pos/person_and_bike_057.png Test/pos/person_and_bike_058.png Test/pos/person_and_bike_059.png Test/pos/person_and_bike_060.png Test/pos/person_and_bike_061.png Test/pos/person_and_bike_062.png Test/pos/person_and_bike_063.png Test/pos/person_and_bike_064.png Test/pos/person_and_bike_065.png Test/pos/person_and_bike_066.png Test/pos/person_and_bike_067.png Test/pos/person_and_bike_069.png Test/pos/person_and_bike_070.png Test/pos/person_and_bike_071.png Test/pos/person_and_bike_072.png Test/pos/person_and_bike_073.png Test/pos/person_and_bike_076.png Test/pos/person_and_bike_077.png Test/pos/person_and_bike_079.png Test/pos/person_and_bike_080.png Test/pos/person_and_bike_081.png Test/pos/person_and_bike_082.png Test/pos/person_and_bike_083.png Test/pos/person_and_bike_084.png Test/pos/person_and_bike_085.png Test/pos/person_and_bike_086.png Test/pos/person_and_bike_087.png Test/pos/person_and_bike_088.png Test/pos/person_and_bike_089.png Test/pos/person_and_bike_090.png Test/pos/person_and_bike_091.png Test/pos/person_and_bike_092.png Test/pos/person_and_bike_093.png Test/pos/person_and_bike_094.png Test/pos/person_and_bike_095.png Test/pos/person_and_bike_096.png Test/pos/person_and_bike_097.png Test/pos/person_and_bike_098.png Test/pos/person_and_bike_099.png Test/pos/person_and_bike_100.png Test/pos/person_and_bike_101.png Test/pos/person_and_bike_102.png Test/pos/person_and_bike_103.png Test/pos/person_and_bike_104.png Test/pos/person_and_bike_105.png Test/pos/person_and_bike_106.png Test/pos/person_and_bike_107.png Test/pos/person_and_bike_108.png Test/pos/person_and_bike_109.png Test/pos/person_and_bike_110.png Test/pos/person_and_bike_111.png Test/pos/person_and_bike_112.png Test/pos/person_and_bike_113.png Test/pos/person_and_bike_114.png Test/pos/person_and_bike_126.png Test/pos/person_and_bike_133.png Test/pos/person_and_bike_136.png Test/pos/person_and_bike_140.png Test/pos/person_and_bike_141.png Test/pos/person_and_bike_149.png Test/pos/person_and_bike_153.png Test/pos/person_and_bike_159.png Test/pos/person_and_bike_160.png Test/pos/person_and_bike_161.png Test/pos/person_and_bike_162.png Test/pos/person_and_bike_163.png Test/pos/person_and_bike_164.png Test/pos/person_and_bike_165.png Test/pos/person_and_bike_177.png Test/pos/person_and_bike_181.png Test/pos/person_and_bike_188.png Test/pos/person_and_bike_189.png Test/pos/person_and_bike_190.png'

try:
#    pos.sort()
    corresp = {}
    for i in range(0, 288):
        name = inria_list[:inria_list.find(".")]
        corresp["I%05d"%(i)] = name
#        print 'name: ' + name
        inria_list = inria_list[inria_list.find(" ") + 1 : ]
#        corresp["I%05d"%(i)] = pos[i+1][:pos[i+1].rfind(".")]
#        print "I%05d: "%(i) + corresp["I%05d"%(i)]
except OSError:
    print "Warning : caltech parser won't be available. Please set pos_path to the path to INRIAPerson positives, such as inria/INRIAPerson/Test/pos"

def parse_file_multi(file, filename, dataset):
    for line in file:
        (x, y, w, h, score) = \
            tuple([float(a) for a in line.strip().rstrip().split(",")])
        if filename not in corresp:
            print 'warning: image ' + filename + ' not found in groundtruth'
        else:
            if hratio != None:
                h2 = h * hratio
                y += (h - h2) / 2.0
                h = h2
            if wratio != None:
                w2 = w * wratio
                x += (w - w2) / 2.0
                w = w2
            if whratio != None:
                w2 = h * whratio
                x += (w - w2) / 2.0
                w = w2
            dataset.add_obj(score, corresp[filename], \
                                BoundingBox(x, y, x+w, y+h, score))

def parse_multi(path, crawl = False, groundtruth = None):
    if crawl == True:
        raise StandardError()
    ret = DataSetMulti()
    filenames = os.listdir(path)
    for filename in filenames:
        #TODO : check validity
        file = open(os.path.join(path, filename), "r")
        parse_file_multi(file, filename[:filename.rfind(".")], ret)
        file.close()
    #print ret
    return ret
