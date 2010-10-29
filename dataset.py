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

import copy
from slist import slist

# A set of multiple objects found in 1 image.
# This set can contain the bounding boxes in the image,
# the image name and its dimensions.
class ImageDataSet(object):
    def __init__(self):
        self.objs = []
        self.height = 0
        self.width = 0
        #self.xmins = slist()
        #self.xmaxs = slist()
        #self.xmin_dict = {}
        #self.xmax_dict = {}

    def add_obj(self, obj, height = 0, width = 0):
        #box = obj.bounding_box()
        self.objs.append(obj)
        if (height != 0):
            self.height = height
        if (width != 0):
            self.width = width
        #self.xmins.insert(box.x1)
        #self.xmaxs.insert(box.x2)
        #if box.x1 not in self.xmin_dict:
        #    self.xmin_dict[box.x1] = []
        #self.xmin_dict[box.x1].append(obj)
        #if box.x2 not in self.xmax_dict:
        #    self.xmax_dict[box.x2] = []
        #self.xmax_dict[box.x2].append(obj)

    def __len__(self):
        return len(self.objs)

    def __getitem__(self, i):
        return self.objs[i]

    def get_objs(self):
        #shallow copy
        return copy.copy(self.objs)

    def get_intersecting_objs(self, other):
        #TODO : is that really useful? Anyway, one can optimize that
        ret = []
        '''
        box = other.bounding_box()
        imin = self.xmaxs.find_index(box.x1)
        imax = self.xmins.find_index(box.x2)
        x1_cur = min([obj.x1 for obj in self.xmax_dict[self.xmaxs[imin]]])
        i_x1_cur = self.xmins.find_index(x1_cur)
        x1_max = self.xmins[imax]
        while x1_cur <= x1_max:
            ret += self.xmin_dict[x1_cur]
            i_x1_cur += 1
            if i_x1_cur >= len(self.xmins):
                break
            x1_cur = self.xmins[i_x1_cur]
        '''
        for obj in self.objs:
            if obj.bounding_box().overlap(other.bounding_box()):
                ret.append(obj)
        return ret

    def get_gprims(self):
        return [obj.get_gprim() for obj in self.objs]

    def __str__(self):
        ret = "(ImageDataSet : "
        for obj in self.objs:
            ret += "%s "%(str(obj),)
        ret = ret[:-1] + ")"
        return ret
    
    def __iter__(self):
        return self.objs.__iter__()

class DataSet(object):
    def __init__(self, label = ""):
        self.images = {}
        self.label = label

    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, i):
        return self.images[i]

    def __iter__(self):
        return self.images.__iter__()

    def keys(self):
        return self.images.keys()

    def add_empty_image(self, image):
        if image not in self.images:
            self.images[image] = ImageDataSet()
        else:
            print "Warning : DataSet.add_empty_image : image already exists."

    def add_obj(self, image, obj, height = 0, width = 0):
        if image not in self.images:
            self.add_empty_image(image)
        self.images[image].add_obj(obj, height, width)

    def get_gprims(self, key):
        if key in self.images:
            return self.images[key].get_gprims()
        else:
            return []

    def get_objs(self, key):
        if key in self.images:
            return self.images[key].get_objs()
        else:
            return []

    def __str__(self):
        ret = "(DataSet %s : "%(self.label,)
        for img in self.images:
            ret += "(%s : %s) "%(img, str(self.images[img]))
        #ret[-1] = ")"
        return ret[:-1] + ")"

    def confidence_max(self):
        if self.images == []:
            return 0
        else:
            m = self.images[self.images.keys()[0]].get_objs()[0].confidence
            for im in self.images:
                for obj in self.images[im].get_objs():
                    if obj.confidence > m:
                        m = obj.confidence
            return m

    def confidence_min(self):
        if self.images == []:
            return 0
        else:
            m = self.images[self.images.keys()[0]].get_objs()[0].confidence
            for im in self.images:
                for obj in self.images[im].get_objs():
                    if obj.confidence < m:
                        m = obj.confidence
            return m

class DataSetFromMulti(object):
    def __init__(self, parent, i_conf_min, label = ""):
        self.parent = parent
        self.i_conf_min = i_conf_min
        self.label = label

    def __len__(self):
        return len(self.parent) - self.i_conf_min

    def __iter__(self):
        ret = self.parent.images.__iter__()
        for i in xrange(0, self.i_conf_min):
            ret.next()
        return ret
        #return DataSetFromMultiIterator(self, self.i_conf_min)

    def __getitem__(self, it):
        if type(i) == int:
            return self.parent[i+self.i_conf_min]

class DataSetMulti(DataSet):
    def __init__(self, label = ""):
        DataSet.__init__(self, label)
        self.confidences = []

    def add_obj(self, confidence, filename, obj, height = 0, width = 0):
        DataSet.add_obj(self, filename, obj, height, width)
        self.confidences.append(float(confidence))
        # while confidence in self.confidences:
        #     confidence += 0.000000000001 #TODO
#        self.objs[confidence] = (filename, self.images[filename][-1])
#        self.confidences[confidence] = (filename, self.images[filename][-1])
#        self.objs.append(filename, obj)

    def __str__(self):
        return "MultiDataSet " + DataSet.__str__(self)

    def __iter__(self):
        return self.confidences.__iter__()
#        return self.Dataset.images.__iter__()

    # Returns a subset of this dataset for which confidences are greater
    # or equal to 'conf'.
    def __getitem__(self, conf):
        ret = DataSet()
        for im in DataSet.__iter__(self):
            for obj in DataSet.__getitem__(self, im):
                if obj.confidence >= conf:
                    ret.add_obj(im, obj)
        return ret
        '''
        i = 0
        for c in self.confidences:
            if self.confidences[c] >= conf:
                break
            i += 1
            print i
        return DataSetFromMulti(self, i)
        '''

    def __len__(self):
        return DataSet.__len__(self)

    def sort_confidences(self):
        self.confidences.sort()
        
    def get_confidences(self):
        return self.confidences

    def images_keys(self):
        return DataSet.keys(self)

    def n_confidences(self):
        return len(self.confidences)
    
    def confidence_max(self):
        if self.confidences == []:
            return 0
        else:
            return max(self.confidences)

    def confidence_min(self):
        if self.confidences == []:
            return 0
        else:
            return min(self.confidences)
