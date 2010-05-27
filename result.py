class ImageResult(object):
    def __init__(self):
        self.matches = []
        self.false_positives = []
        self.false_negatives = []

    def add_match(self, box1, box2):
        self.matches.append((box1, box2))
        #print "match", box1, box2

    def add_false_positive(self, box):
        self.false_positives.append(box)
        #print "false positive", box

    def add_unrecognized(self, box):
        self.false_negatives.append(box)
        #print "missed", box

    def n_matches(self):
        return len(self.matches)

    def n_false_positives(self):
        return len(self.false_positives)

    def n_unrecognized(self):
        return len(self.false_negatives)


class DataSetResult(object):
    def __init__(self):
        self.images_results = []
        self.n_matches = 0
        self.n_false_positives = 0
        self.n_unrecognized = 0

    def add_image_result(self, result):
        self.images_results.append(result)
        self.n_matches += result.n_matches()
        self.n_false_positives += result.n_false_positives()
        self.n_unrecognized += result.n_unrecognized()

    def __str__(self):
        return "DataSetResult : %d matches, %d false positive, %d missed"%(self.n_matches,
                                                                           self.n_false_positives,
                                                                           self.n_unrecognized)
class MultiResult(object):
    def __init__(self):
        self.datasets = []

    def add_result(self, result):
        self.datasets.append(result)

    def __str__(self):
        ret = "MultiResult : "
        for th in self.datasets:
            ret += "%s "%(self.datasets[th],)
        return ret[:-1]

    def __getitem__(self, i):
        return self.datasets[i]

def BoolResult(object):
    def __init__(self):
        self.images = {}

    def add_true_positive(self, filename):
        if filename in self.images:
            print "Warning : BoolResult : %s already exists."%(filename,)
        self.images[filename] = "TP"

    def add_false_positive(self, filename):
        if filename in self.images:
            print "Warning : BoolResult : %s already exists."%(filename,)
        self.images[filename] = "FP"

    def add_true_negative(self, filename):
        if filename in self.images:
            print "Warning : BoolResult : %s already exists."%(filename,)
        self.images[filename] = "TN"

    def add_false_negative(self, filename):
        if filename in self.images:
            print "Warning : BoolResult : %s already exists."%(filename,)
        self.images[filename] = "FN"

    def n_true_positives(self):
        return len(self.true_positives)

    def n_false_positives(self):
        return len(self.false_positives)

    def n_true_negatives(self):
        return len(self.true_negatives)

    def n_false_negatives(self):
        return len(self.false_negatives)
