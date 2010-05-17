#!/usr/bin/python

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
    usage = "usage: %prog -i input -g groundtruth --input_parser inputparser --groundtruth_parser groundtruthparser -c comparator [OPTIONS]"
    optparser = optparse.OptionParser(add_help_option = True, usage = usage, prog = "./main.py")
    optparser.add_option("-i", "--input", dest = "input", default = None, type = "str",
                         help = "Input file to score (required)")
    optparser.add_option("-g", "--groundtruth", dest = "groundtruth", default = None, type = "str",
                         help = "Ground truth file (required)")
    optparser.add_option("--input_parser", dest = "input_parser", default = None, type = "str",
                         help = "Parser to use for the file to score")
    optparser.add_option("--groundtruth_parser", dest = "groundtruth_parser", default = None, type = "str",
                         help = "Parser to use for the ground truth file")
    optparser.add_option("--parser_dir", dest = "parser_dir", default = "parsers", type = "str",
                         help = "Parser directory")
    optparser.add_option("--comparator_dir", dest = "comparator_dir", default = "comparators",
                         type = "str", help = "Comparator directory")
    optparser.add_option("-c", "--comparator", dest = "comparator", default = None, type = "str",
                         help = "Comparator to use")
    (options, args) = optparser.parse_args()

    if options.input == None or options.groundtruth == None:
        optparser.print_usage()
        sys.exit(0)
    toscore_filename = options.input
    groundtruth_filename = options.groundtruth

    parser_dir = options.parser_dir
    comparator_dir = options.comparator_dir
    parsers = ParsersHandler(parser_dir)
    comparators = ComparatorsHandler(comparator_dir)

    if options.input_parser == None or options.groundtruth_parser == None:
        optparser.print_usage()
        sys.exit(0)
    toscore_parser = parsers.get_parser(options.input_parser)
    groundtruth_parser = parsers.get_parser(options.groundtruth_parser)
    
    toscore_file = open(toscore_filename, "r")
    toscore = toscore_parser.parse(toscore_file)
    toscore_file.close()
    groundtruth_file = open(groundtruth_filename, "r")
    groundtruth = groundtruth_parser.parse(groundtruth_file)
    groundtruth_file.close()

    if options.comparator == None:
        optparser.print_usage()
        sys.exit(0)
    comparator = comparators.get_comparator(options.comparator)
    result = comparator.compare_datasets(toscore, groundtruth)
    print result
