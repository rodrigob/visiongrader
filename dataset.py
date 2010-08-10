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

class ImageDataSet(object):
    def __init__(self):
        self.objs = []
        #self.xmins = slist()
        #self.xmaxs = slist()
        #self.xmin_dict = {}
        #self.xmax_dict = {}

    def add_obj(self, obj):
        #box = obj.bounding_box()
        self.objs.append(obj)
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

    def add_obj(self, image, obj):
        if image not in self.images:
            self.add_empty_image(image)
        self.images[image].add_obj(obj)

    def get_gprims(self, key):
        if key in self.images:
            return self.images[key].get_gprims()
        else:
            return []

    def __str__(self):
        ret = "(DataSet %s : "%(self.label,)
        for img in self.images:
            ret += "(%s : %s) "%(img, str(self.images[img]))
        #ret[-1] = ")"
        return ret[:-1] + ")"

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
        self.confidences = {}

    def add_obj(self, confidence, filename, obj):
        DataSet.add_obj(self, filename, obj)
        while confidence in self.confidences:
            confidence += 0.000001 #TODO
        self.confidences[confidence] = (filename, self.images[filename][-1])

    def __str__(self):
        return "MultiDataSet " + DataSet.__str__(self)

    def __iter__(self):
        return self.confidences.__iter__()

    def __getitem__(self, conf):
        ret = DataSet()
        for confidence in self.confidences:
            if confidence > conf:
                ret.add_obj(*self.confidences[confidence])
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

    def keys(self):
        return self.confidences.keys()

    def images_keys(self):
        return DataSet.keys(self)

    def n_confidences(self):
        return len(self.confidences)

    def confidence_max(self):
        return max(self.confidences.keys())

    def confidence_min(self):
        return min(self.confidences.keys())
