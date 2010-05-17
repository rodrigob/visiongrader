import optparse
import os
import os.path
import sys

class ParsersHandler(object):
    def __init__(self, parser_dir):
        self.parsers = {}
        parser_names = os.listdir(parser_dir)
        sys.path.append(os.path.abspath(parser_dir))
        for name in parser_names:
            if self.is_a_parser_name(name):
                name = name[:-3]
                print name
                __import__(name)
                self.parsers[name] = sys.modules[name]
        sys.path.remove(os.path.abspath(parser_dir))

    def is_a_parser_name(self, name):
        return name[-3:] == ".py"

    def get_parser_names(self):
        return self.parsers.keys()

    def get_parser(self, name):
        return self.parsers[name]

class ComparatorsHandler(object):
    def __init__(self, comparator_dir):
        self.comparators = {}
        comparator_names = os.listdir(comparator_dir)
        sys.path.append(os.path.abspath(comparator_dir))
        for name in comparator_names:
            if self.is_a_comparator_name(name):
                name = name[:-3]
                __import__(name)
                self.comparators[name] = sys.modules[name]
        sys.path.remove(os.path.abspath(comparator_dir))

    def is_a_comparator_name(self, name):
        return name[-3:] == ".py"

    def get_comparator_names(self):
        return self.comparators.keys()

    def get_comparator(self, name):
        return self.comparators[name]        

if __name__=="__main__":
    parser_dir = "parsers"
    parsers = ParsersHandler(parser_dir)
    comparator_dir = "comparators"
    comparators = ComparatorsHandler(comparator_dir)
    
    toscore_filename = "data/CMU/groundtruth/test"
    groundtruth_filename = "data/CMU/groundtruth/test"
    toscore_parser = parsers.get_parser("cmu")
    groundtruth_parser = parsers.get_parser("cmu")
    toscore_file = open(toscore_filename, "r")
    toscore = toscore_parser.parse(toscore_file)
    toscore_file.close()
    groundtruth_file = open(groundtruth_filename, "r")
    groundtruth = groundtruth_parser.parse(groundtruth_file)
    groundtruth_file.close()

    comparator = comparators.get_comparator("overlap")
    result = comparator.compare_datasets(toscore, groundtruth)
