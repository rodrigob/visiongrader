import viewer
import result

def single_scoring(ts_filename, ts_parser, gt_filename, gt_parser, comparator):
    ts = ts_parser.parse(ts_filename)
    gt = gt_parser.parse(gt_filename)
    return comparator.compare_datasets(ts, gt)

def display(ts_filename, ts_parser, gt_filename, gt_parser, img_path):
    ts = ts_parser.parse_multi(ts_filename)
    gt = gt_parser.parse(gt_filename)
    v = viewer.GUI()
    keys = ts.images_keys()
    global i
    i = 0
    def on_refresh(ts = ts, v = v):
        global i
        img_name = keys[i]
        filename = gt_parser.get_img_from_name(img_name, gt_filename, img_path)
        v.set_title(img_name)
        confidence = v.get_slider_position()
        ts2 = ts[confidence]
        v.display(filename, gt.get_gprims(img_name), ts2.get_gprims(img_name))
    def on_next():
        global i
        i = (i + 1) % len(keys)
        on_refresh()
    def on_prev():
        global i
        i = (i - 1) % len(keys)
        on_refresh()
    v.on_next = on_next
    v.on_prev = on_prev
    v.on_slider_moved = on_refresh
    v.set_slider_params(ts.confidence_min(), ts.confidence_max(), 2)
    on_refresh()
    v.start()

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
