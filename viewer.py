import gtk
import sys
import cairo

class Displayer(gtk.DrawingArea):
    def __init__(self, main_window):
        super(Displayer, self).__init__()
        self.main_window = main_window
        self.w_surface = None
        self.h_surface = None
        self.surface = None
        self.img_surface = None
        self.gprims = []
        self.connect("size-allocate", self.size_allocate)
        self.connect("expose-event", self.expose_event)
        
    def size_allocate(self, widget, allocation):
        self.w_surface = allocation.width
        self.h_surface = allocation.height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                          self.w_surface, self.h_surface)
        context = cairo.Context(self.surface)
        self.draw()

    def expose_event(self, widget, event):
        if not self.surface:
            return True
        wcontext = event.window.cairo_create()
        wcontext.set_operator(cairo.OPERATOR_SOURCE)
        wcontext.set_source_surface(self.surface)
        wcontext.rectangle(event.area.x, event.area.y,
                           event.area.width, event.area.height)
        wcontext.fill()
        return False

    def set_window_size(self, w, h):
        self.main_window.set_geometry_hints(None, w, h, w, h)

    def set_image(self, filename):
        pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
        self.img_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                              pixbuf.get_width(), pixbuf.get_height())
        img_context = gtk.gdk.CairoContext(cairo.Context(self.img_surface))
        img_context.set_operator(cairo.OPERATOR_SOURCE)
        img_context.set_source_rgb(1, 1, 1)
        img_context.paint()
        img_context.set_source_pixbuf(pixbuf, 0, 0)
        img_context.paint()
        #self.set_size_request(pixbuf.get_width(), pixbuf.get_height())
        self.set_window_size(pixbuf.get_width(), pixbuf.get_height())
        self.draw()

    def add_gprim(self, gprim, r, g, b):
        self.gprims.append((gprim, (r, g, b)))

    def clear_gprims(self):
        self.gprims = []

    def draw(self):
        if not self.img_surface:
            context = cairo.Context(self.surface)
            context.set_source_rgb(1, 1, 1)
            context.set_operator(cairo.OPERATOR_SOURCE)
            context.paint()
        else:
            context = cairo.Context(self.surface)
            pattern = cairo.SurfacePattern(self.img_surface)
            pattern.set_filter(cairo.FILTER_GOOD)
            xscale = float(self.img_surface.get_width()) \
                / float(self.surface.get_width())
            yscale = float(self.img_surface.get_height()) \
                / float(self.surface.get_height())
            pattern.set_matrix(cairo.Matrix(xx = xscale, yy = yscale))
            context.set_source(pattern)
            context.set_operator(cairo.OPERATOR_SOURCE)
            context.paint()
            context.set_operator(cairo.OPERATOR_OVER)
            for (gprim, color) in self.gprims:
                context.set_source_rgb(*color)
                gprim.draw(context)
        self.queue_draw()

class GUI(object):
    def __init__(self, on_click_ext):
        super(GUI, self).__init__()
        self.on_click_ext = on_click_ext
        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_window.connect("destroy", self.on_destroy)
        self.displayer = Displayer(self.main_window)
        self.main_window.add(self.displayer)
        self.main_window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.main_window.connect("button-press-event", self.on_click)
        self.main_window.show_all()

    def on_destroy(self, *args):
        gtk.main_quit()

    def display(self, img_filename, gts, positives):
        self.displayer.set_image(img_filename)
        self.displayer.clear_gprims()
        for gt in gts:
            self.displayer.add_gprim(gt, 1, 0, 0)
        for pos in positives:
            self.displayer.add_gprim(pos, 0, 1, 0)
        self.displayer.draw()

    def on_click(self, *args):
        self.on_click_ext()
        return False

class Viewer(object):
    def __init__(self):
        super(Viewer, self).__init__()
        self.gui = None

    def start(self, on_init, on_click):
        self.gui = GUI(on_click)
        on_init()
        gtk.main()

    def display(self, img_filename, gts, positives):
        self.gui.display(img_filename, gts, positives)

if __name__ == "__main__":
    def c():
        pass
    gui = GUI(c)
    gtk.main()
