import copy


class ImageDataSet(object):
    def __init__(self, objs = []):
        self.objs = objs

    def add_obj(self, obj):
        self.objs.append(obj)

    def __len__(self):
        return len(self.objs)

    def __getitem__(self, i):
        return self.objs[i]

    def get_objs(self):
        #shallow copy
        return copy.copy(self.objs)
    

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
