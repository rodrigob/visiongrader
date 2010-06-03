#!/usr/bin/python

import optparse
import os
import os.path
import sys
import plot

from result import MultiResult

class ModuleHandler(object):
    def __init__(self, module_dir, module_name):
        self.modules = {}
        self.module_name = module_name
        modules_names = os.listdir(os.path.join(module_dir, module_name))
        if module_dir not in sys.path:
            sys.path.append(os.path.abspath(module_dir))
            remove_from_path = True
        else:
            remove_from_path = False
        __import__(module_name)
        for name in modules_names:
            if self.is_a_module_name(name):
                name = "%s.%s"%(module_name, name[:-3])
                __import__(name)
                self.modules[name] = sys.modules[name]
        if remove_from_path:
            sys.path.remove(os.path.abspath(module_dir))

    def is_a_module_name(self, name):
        return name[-3:] == ".py"

    def get_modules_names(self):
        return self.modules.keys()

    def get_module(self, name):
        return self.modules["%s.%s"%(self.module_name, name)]

if __name__=="__main__":
    usage = "usage: %prog -i input -g groundtruth --input_parser inputparser --groundtruth_parser \
    groundtruthparser -c comparator [OPTIONS] [--roc] [--det]"
    optparser = optparse.OptionParser(add_help_option = True, usage = usage, prog = "./main.py")
    optparser.add_option("-i", "--input", dest = "input", default = None, type = "str",
                         help = "Input file to score (if not specified, a generator must be specified)")
    optparser.add_option("-t", "--groundtruth", dest = "groundtruth", default = None, type = "str",
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
                         help = "Comparator to use (required)")
    optparser.add_option("--roc", dest = "roc", action = "store_true", default = False,
                         help = "Print ROC curve.")
    optparser.add_option("--det", dest = "det", action = "store_true", default = False,
                         help = "Print DET curve.")
    optparser.add_option("--confidence_max", dest = "confidence_max", default = None,
                         type = "float", help = "Maximum confidence to display for the curves.")
    optparser.add_option("--confidence_min", dest = "confidence_min", default = None,
                         type = "float", help = "Mminimum confidence to display for the curves.")
    (options, args) = optparser.parse_args()

    if options.input == None:
        optparser.print_usage()
        sys.exit(0)
    toscore_filename = options.input

    if options.roc == True:
        if options.det == True:
            print "You cannot choose both --roc and --det."
            sys.exit(0)
        mode = "ROC"
    elif options.det == True:
        mode = "DET"
    else:
        mode = "input_file"

    if options.groundtruth == None:
        optparser.print_usage()
        sys.exit(0)
    groundtruth_filename = options.groundtruth

    parser_dir = options.parser_dir
    comparator_dir = options.comparator_dir
    parsers = ModuleHandler(".", parser_dir)
    comparators = ModuleHandler(".", comparator_dir)

    if options.input_parser == None or options.groundtruth_parser == None:
        optparser.print_usage()
        sys.exit(0)
    toscore_parser = parsers.get_module(options.input_parser) #TODO : check existence
    groundtruth_parser = parsers.get_module(options.groundtruth_parser) #TODO same

    if options.comparator == None:
        optparser.print_usage()
        sys.exit(0)
    comparator = comparators.get_module(options.comparator)

    groundtruth = groundtruth_parser.parse(groundtruth_filename)
    
    if mode == "input_file":
        toscore = toscore_parser.parse(toscore_filename)
        result = comparator.compare_datasets(toscore, groundtruth)
        print result
    elif mode == "ROC" or mode == "DET":
        toscore = toscore_parser.parse_multi(toscore_filename)
        multi_result = MultiResult()
        print toscore.n_confidences()
        n = 10
        for i in xrange(0, toscore.n_confidences() / n):
            #print i
            confidence = toscore.keys()[i*n]
            if options.confidence_min != None:
                if confidence < options.confidence_min:
                    continue
            if options.confidence_max != None:
                if confidence > options.confidence_max:
                    continue
            print i
            dataset = toscore[confidence]
            result = comparator.compare_datasets(dataset, groundtruth)
            multi_result.add_result(result)
        if mode == "ROC":
            if groundtruth_parser.data_type == "images":
                plot.print_ROC(multi_result, len(toscore))
            elif groundtruth_parser.data_type == "posneg":
                plot.print_ROC(multi_result, len(toscore))
                #plot.print_ROC_posneg(multi_result)
            else:
                raise NotImplementedError()
        elif mode == "DET":
            if groundtruth_parser.data_type == "images":
                plot.print_DET(multi_result, len(toscore))
            elif groundtruth_parser.data_type == "posneg":
                #plot.print_DET_posneg(multi_result)
                plot.print_DET(multi_result, len(toscore))
            else:
                raise NotImplementedError()
