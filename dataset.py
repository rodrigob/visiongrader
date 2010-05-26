import copy
from slist import slist

class ImageDataSet(object):
    def __init__(self):
        self.objs = []
        self.xmins = slist()
        self.xmaxs = slist()
        self.xmin_dict = {}
        self.xmax_dict = {}

    def add_obj(self, obj):
        box = obj.bounding_box()
        self.objs.append(obj)
        self.xmins.insert(box.x1)
        self.xmaxs.insert(box.x2)
        if box.x1 not in self.xmin_dict:
            self.xmin_dict[box.x1] = []
        self.xmin_dict[box.x1].append(obj)
        if box.x2 not in self.xmax_dict:
            self.xmax_dict[box.x2] = []
        self.xmax_dict[box.x2].append(obj)

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

    def add_obj(self, image, obj):
        if image not in self.images:
            self.images[image] = ImageDataSet()
        self.images[image].add_obj(obj)

    def __str__(self):
        ret = "(DataSet %s : "%(self.label,)
        for img in self.images:
            ret += "(%s : %s) "%(img, str(self.images[img]))
        ret = ret[:-1] + ")"
        return ret

class DataSetMulti(DataSet):
    def __init__(self, label = ""):
        DataSet.__init__(self, label)
        self.confidences = {}

    def add_obj(self, confidence, filename, obj):
        DataSet.add_obj(self, filename, obj)
        while confidence in self.confidences:
            confidence += 0.00001 #TODO
        self.confidences[confidence] = (filename, self.images[filename][-1])

    def __str__(self):
        return "MultiDataSet " + DataSet.__str__(self)

    def __iter__(self):
        return self.confidences.__iter__()

    def __getitem__(self, i):
        ret = DataSet()
        for confidence in self.confidences:
            if confidence > i:
                ret.add_obj(*self.confidences[confidence])
        return ret
