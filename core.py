import viewer
import result

def single_scoring(ts_filename, ts_parser, gt_filename, gt_parser, comparator):
    ts = ts_parser.parse(ts_filename)
    gt = gt_parser.parse(gt_filename)
    return comparator.compare_datasets(ts, gt)

def display(ts_filename, ts_parser, gt_filename, gt_parser, img_path):
    ts = ts_parser.parse(ts_filename)
    gt = gt_parser.parse(gt_filename)
    v = viewer.Viewer()
    global i #TODO : dirty
    i = 0
    def on_click(ts = ts, v = v):
        global i
        img_name = ts.keys()[i]
        filename = gt_parser.get_img_from_name(img_name, gt_filename, img_path)
        #img = ts[img_name]
        #gt_img = gt[img_name]
        print i
        i = (i + 1) % len(ts)
        v.display(filename, gt.get_gprims(img_name), ts.get_gprims(img_name))
    v.start(on_click, on_click)

def multi_scoring(ts_filename, ts_parser, gt_filename, gt_parser, comparator,
                  crawl, sampling, confidence_min, confidence_max):
    ts = ts_parser.parse_multi(ts_filename, crawl)
    gt = gt_parser.parse(gt_filename)
    multi_result = result.MultiResult()
    if sampling == None:
        n = 200
    else:
        n = int(ts.n_confidence() / sampling)
    for i in xrange(0, n):
        confidence = ts.keys()[ts.n_confidences() / n * i]
        if confidence_min != None:
            if confidence < confidence_min:
                continue
        if confidence_max != None:
            if confidence > confidence_max:
                continue
        print i
        dataset = ts[confidence]
        multi_result.add_result(comparator.compare_datasets(dataset, gt))
    return (multi_result, ts)
