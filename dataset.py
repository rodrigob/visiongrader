import copy
import slist

class ImageDataSet(object):
    def __init__(self):
        self.objs = []
        self.xmins = slist()
        self.xmaxs = slist()

    def add_obj(self, obj):
        box = obj.bounding_box()
        self.objs.append(obj)
        self.xmins.insert((box.x1, obj))
        self.xmaxs.insert((box.x2, obj))

    def __len__(self):
        return len(self.objs)

    def __getitem__(self, i):
        return self.objs[i]

    def get_objs(self):
        #shallow copy
        return copy.copy(self.objs)

    def get_intersecting_objs(self, other):
        #TODO
        ret = []
        for obj in self.objs:
            if obj.bounding_box().overlap(other.bounding_box()):
                ret.append(obj)
        return ret
    

class DataSet(object):
    def __init__(self, label = ""):
        self.images = {}
        self.label = label

    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, i):
        return self.images.values()[i]

    def add_obj(self, image, obj):
        if image not in self.images:
            self.images[image] = ImageDataSet()
        self.images[image].add_obj(obj)
    

class ROCDataSet(object):
    def __init__(self):
        self.results = []
