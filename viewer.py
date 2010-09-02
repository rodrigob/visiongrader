# Copyright (C) 2010 Michael Mathieu <michael.mathieu@ens.fr>
# 
# This file is part of visiongrader.
# 
# visiongrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# visiongrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with visiongrader.  If not, see <http://www.gnu.org/licenses/>.
# 
# Authors :
#  Michael Mathieu <michael.mathieu@ens.fr>

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
        self.main_window.set_geometry_hints(self, w, h, w, h)
        self.set_size_request(w, h)
        #self.set_geometry_hints(None, w, h, w, h)
        pass

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
    def __init__(self, parent = None):
        super(GUI, self).__init__()
        if parent != None:
            self.main_window = parent
        else:
            self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.main_window.connect("destroy", self.on_destroy)

        self.vbox1 = gtk.VBox(3)
        self.vbox1.set_homogeneous(False)
        self.main_window.add(self.vbox1)

        self.input = gtk.Entry()
        self.input.connect("activate", self._on_activate)
        self.next_button = gtk.Button(label = "next")
        self.next_button.connect("clicked", self._on_next)
        self.prev_button = gtk.Button(label = "prev")
        self.prev_button.connect("clicked", self._on_prev)
        self.hbox1 = gtk.HBox(2)
        self.hbox1.pack_start(self.input, False, True)
        self.hbox1.pack_start(self.prev_button, False, True)
        self.hbox1.pack_start(self.next_button, False, True)
        self.vbox1.pack_start(self.hbox1, False, False)

        self.hbox2 = gtk.HBox(2)
        self.hbox2.set_homogeneous(False)
        self.vbox1.pack_start(self.hbox2, False, False)
        self.label_slider = gtk.Label("Confidence : ")
        self.hbox2.pack_start(self.label_slider, False, False)
        self.hscale1 = gtk.HScale()
        self.hscale1.set_range(0, 1)
        self.hscale1.connect("value-changed", self._on_slider_moved)
        self.hbox2.pack_start(self.hscale1, True, True)

        self.displayer = Displayer(self.main_window)
        self.vbox1.pack_start(self.displayer, False, False)

        self.main_window.show_all()

    def on_destroy(self, *args):
        gtk.main_quit()

    def set_title(self, title):
        self.main_window.set_title(title)

    def set_slider_params(self, xmin, xmax, digits):
        self.hscale1.set_range(xmin, xmax)
        self.hscale1.set_digits(digits)

    def get_slider_position(self):
        return self.hscale1.get_value()

    def display(self, img_filename, gts, positives):
        self.displayer.set_image(img_filename)
        self.displayer.clear_gprims()
        for gt in gts:
            self.displayer.add_gprim(gt, 1, 0, 0)
        for pos in positives:
            self.displayer.add_gprim(pos, 0, 1, 0)
        self.displayer.draw()

    def _on_activate(self, entry):
        self.on_activate(entry.get_text())
        return False

    def on_activate(self, text):
        pass

    def _on_next(self, *args):
        self.on_next()
        return False

    def on_next(self, *args):
        pass

    def _on_prev(self, *args):
        self.on_prev()
        return False

    def on_prev(self):
        pass

    def _on_slider_moved(self, *args):
        self.on_slider_moved()
        return False

    def on_slider_moved(self):
        pass

    def start(self):
        gtk.main()

if __name__ == "__main__":
    def c():
        pass
    gui = GUI(c)
    gtk.main()
