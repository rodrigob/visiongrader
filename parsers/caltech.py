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

def describe():
    return "Caltech bounding boxes parser"

def recognize(file):
    return False

#pos_path = "/home/myrhev32/visiongrader/visiongrader/data/inria/INRIAPerson/Test/pos"
pos_path = "/data/pedestrians/inria/INRIAPerson/Test/pos"

inria_list = 'crop001501.png crop001504.png crop001511.png crop001512.png crop001514.png crop001520.png crop001521.png crop001522.png crop001531.png crop001533.png crop001544.png crop001545.png crop001546.png crop001549.png crop001555.png crop001566.png crop001573.png crop001574.png crop001590.png crop001593.png crop001602.png crop001604.png crop001607.png crop001631.png crop001633.png crop001634.png crop001638.png crop001639.png crop001641.png crop001653.png crop001654.png crop001658.png crop001659.png crop001660.png crop001661.png crop001664.png crop001670.png crop001676.png crop001682.png crop001683.png crop001684.png crop001688.png crop001704.png crop001706.png crop001715.png crop001716.png crop001718.png crop001719.png crop001722.png crop001723.png crop001724.png crop001725.png crop_000001.png crop_000002.png crop_000003.png crop_000004.png crop_000005.png crop_000006.png crop_000007.png crop_000008.png crop_000009.png crop_000012.png crop_000013.png crop_000015.png crop_000016.png crop_000017.png crop_000018.png crop_000019.png crop_000020.png crop_000021.png crop_000023.png crop_000024.png crop_000025.png crop_000026.png crop_000027.png crop_000604.png person_007.png person_008.png person_009.png person_010.png person_011.png person_012.png person_013.png person_014.png person_015.png person_026.png person_028.png person_029.png person_030.png person_032.png person_033.png person_034.png person_036.png person_037.png person_038.png person_039.png person_040.png person_051.png person_052.png person_053.png person_055.png person_056.png person_058.png person_059.png person_062.png person_063.png person_064.png person_065.png person_070.png person_071.png person_073.png person_075.png person_076.png person_085.png person_087.png person_088.png person_089.png person_090.png person_092.png person_093.png person_094.png person_095.png person_096.png person_098.png person_099.png person_100.png person_104.png person_105.png person_107.png person_115.png person_118.png person_120.png person_122.png person_127.png person_132.png person_134.png person_135.png person_136.png person_137.png person_138.png person_159.png person_161.png person_164.png person_186.png person_188.png person_189.png person_190.png person_191.png person_193.png person_194.png person_198.png person_200.png person_204.png person_206.png person_207.png person_210.png person_212.png person_216.png person_217.png person_218.png person_222.png person_230.png person_236.png person_246.png person_247.png person_248.png person_249.png person_250.png person_251.png person_255.png person_263.png person_265.png person_272.png person_280.png person_282.png person_290.png person_293.png person_303.png person_306.png person_314.png person_315.png person_316.png person_317.png person_318.png person_323.png person_325.png person_335.png person_336.png person_337.png person_347.png person_350.png person_and_bike_004.png person_and_bike_006.png person_and_bike_012.png person_and_bike_014.png person_and_bike_027.png person_and_bike_028.png person_and_bike_029.png person_and_bike_035.png person_and_bike_038.png person_and_bike_042.png person_and_bike_043.png person_and_bike_044.png person_and_bike_045.png person_and_bike_046.png person_and_bike_047.png person_and_bike_048.png person_and_bike_049.png person_and_bike_050.png person_and_bike_051.png person_and_bike_052.png person_and_bike_053.png person_and_bike_054.png person_and_bike_055.png person_and_bike_056.png person_and_bike_057.png person_and_bike_058.png person_and_bike_059.png person_and_bike_060.png person_and_bike_061.png person_and_bike_062.png person_and_bike_063.png person_and_bike_064.png person_and_bike_065.png person_and_bike_066.png person_and_bike_067.png person_and_bike_069.png person_and_bike_070.png person_and_bike_071.png person_and_bike_072.png person_and_bike_073.png person_and_bike_076.png person_and_bike_077.png person_and_bike_079.png person_and_bike_080.png person_and_bike_081.png person_and_bike_082.png person_and_bike_083.png person_and_bike_084.png person_and_bike_085.png person_and_bike_086.png person_and_bike_087.png person_and_bike_088.png person_and_bike_089.png person_and_bike_090.png person_and_bike_091.png person_and_bike_092.png person_and_bike_093.png person_and_bike_094.png person_and_bike_095.png person_and_bike_096.png person_and_bike_097.png person_and_bike_098.png person_and_bike_099.png person_and_bike_100.png person_and_bike_101.png person_and_bike_102.png person_and_bike_103.png person_and_bike_104.png person_and_bike_105.png person_and_bike_106.png person_and_bike_107.png person_and_bike_108.png person_and_bike_109.png person_and_bike_110.png person_and_bike_111.png person_and_bike_112.png person_and_bike_113.png person_and_bike_114.png person_and_bike_126.png person_and_bike_133.png person_and_bike_136.png person_and_bike_140.png person_and_bike_141.png person_and_bike_149.png person_and_bike_153.png person_and_bike_159.png person_and_bike_160.png person_and_bike_161.png person_and_bike_162.png person_and_bike_163.png person_and_bike_164.png person_and_bike_165.png person_and_bike_177.png person_and_bike_181.png person_and_bike_188.png person_and_bike_189.png person_and_bike_190.png'

try:
    pos = os.listdir(pos_path)
#    pos.sort()
    corresp = {}
    for i in xrange(len(pos) - 1):
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
