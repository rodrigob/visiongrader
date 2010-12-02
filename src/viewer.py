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
from gprimitives import Rectangle
from objects import BoundingBox

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
                                              pixbuf.get_width(),
                                              pixbuf.get_height())
        img_context = gtk.gdk.CairoContext(cairo.Context(self.img_surface))
        img_context.set_operator(cairo.OPERATOR_SOURCE)
        img_context.set_source_rgb(1, 1, 1)
        img_context.paint()
        img_context.set_source_pixbuf(pixbuf, 0, 0)
        img_context.paint()
        #self.set_size_request(pixbuf.get_width(), pixbuf.get_height())
        self.set_window_size(pixbuf.get_width(), pixbuf.get_height())
        self.draw()

    def add_gprim(self, gprim, color):
        self.gprims.append((gprim, color))

    def clear_gprims(self):
        self.gprims = []

    def draw(self, boxes = None):
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
                context.set_source_rgb(color.red / float(65535),
                                       color.green / float(65535),
                                       color.blue / float(65535))
                gprim.draw(context)
            if boxes:
                context.set_source_rgb(.5, 0, .5)
                for box in boxes:
                    box.draw(context)
                    print 'drawing ' + str(box)
        self.queue_draw()

class GUI(object):
    def __init__(self, parent = None):
        super(GUI, self).__init__()
        if parent != None:
            self.main_window = parent
        else:
            self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.main_window.connect("destroy", self.on_destroy)
            self.main_window.connect("key_press_event", self.on_key_press)
            self.main_window.connect("key_release_event", self.on_key_release)

        self.vbox1 = gtk.VBox(3)
        self.vbox1.set_homogeneous(False)
        self.main_window.add(self.vbox1)

        # image bar
        self.label_image = gtk.Label("Image: ")
        self.input = gtk.Entry()
        self.input.connect("activate", self._on_activate)
        self.next_button = gtk.Button(label = "next")
        self.next_button.connect("clicked", self._on_next)
        self.prev_button = gtk.Button(label = "prev")
        self.prev_button.connect("clicked", self._on_prev)
        self.hbox1 = gtk.HBox(False)
        self.hbox1.pack_start(self.label_image, False, False)
        self.hbox1.pack_start(self.input, False, True)
        self.hbox1.pack_start(self.prev_button, True, True)
        self.hbox1.pack_start(self.next_button, True, True)
        self.vbox1.pack_start(self.hbox1, False, False)

        # confidence bar
        self.hbox2 = gtk.HBox(True)
        self.hbox2.set_homogeneous(False)
        self.vbox1.pack_start(self.hbox2, False, False)
        self.label_slider = gtk.Label("Confidence: ")
        self.hbox2.pack_start(self.label_slider, False, False)
        self.confidence_input = gtk.Entry()
        self.confidence_input.connect("activate", self._on_conf_activate)
        self.hbox2.pack_start(self.confidence_input, False, True)
        self.hscale1 = gtk.HScale()
        self.hscale1.set_range(0, 1)
        self.hscale1.connect("value-changed", self._on_slider_moved)
        self.hbox2.pack_start(self.hscale1, True, True)

        # bbox save bar
        self.hbox3 = gtk.HBox(False)
        self.vbox1.pack_start(self.hbox3, False, False)
        self.label_bbox = gtk.Label("Bbox saving directory: ")
        self.input_save = gtk.Entry()
        self.hbox3.pack_start(self.label_bbox, False, False)
        self.hbox3.pack_start(self.input_save, True, True)

        self.displayer = Displayer(self.main_window)
        self.displayer.connect("button_press_event", self.on_button_press)
        self.displayer.connect("button_release_event", self.on_button_release)
        self.displayer.connect("motion_notify_event", self.on_motion_notify)
        self.displayer.set_events(gtk.gdk.EXPOSURE_MASK
                                  | gtk.gdk.LEAVE_NOTIFY_MASK
                                  | gtk.gdk.BUTTON_PRESS_MASK
                                  | gtk.gdk.BUTTON_RELEASE_MASK
                                  | gtk.gdk.POINTER_MOTION_MASK
                                  | gtk.gdk.POINTER_MOTION_HINT_MASK)
        # right hand buttons
        self.vbox4 = gtk.VButtonBox()
        self.ignore_button = gtk.Button(label = 'ignore')
        self.save_button = gtk.Button(label = 'save')
        self.save_button.connect("clicked", self._on_save)
        self.clear_button = gtk.Button(label = 'clear')
        self.clear_button.connect("clicked", self.on_clear)
        self.gt_button = gtk.CheckButton("Groundtruth")
        self.fp_button = gtk.CheckButton("False positives")
        self.gti_button = gtk.CheckButton("Ignored groundtruth")
        self.matchedgti_button = gtk.CheckButton("Matched ignored groundtruth")
        self.matchedtsi_button = gtk.CheckButton("Matched ignored input")
        self.matchedgt_button = gtk.CheckButton("Matched groundtruth")
        self.matchedts_button = gtk.CheckButton("Matched input")
        self.gt_button.connect("clicked", self.on_gt)
        self.fp_button.connect("clicked", self.on_fp)
        self.gti_button.connect("clicked", self.on_gti)
        self.matchedgti_button.connect("clicked", self.on_matchedgti)
        self.matchedtsi_button.connect("clicked", self.on_matchedtsi)
        self.matchedgt_button.connect("clicked", self.on_matchedgt)
        self.matchedts_button.connect("clicked", self.on_matchedts)
        # buttons colors
        self.vbox4.add(self.clear_button)
        self.vbox4.add(self.save_button)
        self.vbox4.add(self.gt_button)
        self.vbox4.add(self.fp_button)
        self.vbox4.add(self.gti_button)
        self.vbox4.add(self.matchedgti_button)
        self.vbox4.add(self.matchedtsi_button)
        self.vbox4.add(self.matchedgt_button)
        self.vbox4.add(self.matchedts_button)
        self.vbox4.set_layout(gtk.BUTTONBOX_START)
        # separate display and right hand buttons
        self.hbox3 = gtk.HBox(False)
        self.hbox3.pack_start(self.displayer, False, False)
        self.hbox3.pack_start(self.vbox4, False, False)    

        self.vbox1.pack_start(self.hbox3, False, False)
        self.main_window.show_all()

        # colors
        self.color_gt = gtk.gdk.Color(65535,0,0)
        self.color_fp = gtk.gdk.Color(0,65535,0)
        self.color_gti = gtk.gdk.Color(0,32765,32765)
        self.color_matchedgti = gtk.gdk.Color(32765,0,32765)
        self.color_matchedtsi = gtk.gdk.Color(32765,32765,0)
        self.color_matchedgt = gtk.gdk.Color(0, 0, 65535)
        self.color_matchedts = gtk.gdk.Color(0, 65535, 65535)

        # text colors
        self.set_check_color(self.gt_button, self.color_gt)
        self.set_check_color(self.fp_button, self.color_fp)
        self.set_check_color(self.gti_button, self.color_gti)
        self.set_check_color(self.matchedgti_button, self.color_matchedgti)
        self.set_check_color(self.matchedgt_button, self.color_matchedgt)
        self.set_check_color(self.matchedtsi_button, self.color_matchedtsi)
        self.set_check_color(self.matchedts_button, self.color_matchedts)
        
        # initializations
        self.button1 = False # button 1 is pressed or not
        self.button1_origin = []
        self.boxes = []
        self.control_key = False
        # display initializations
        self.display_gt = True
        self.display_fp = True
        self.display_gti = True
        self.display_matchedgti = True
        self.display_matchedtsi = True
        self.display_matchedgt = True
        self.display_matchedts = True
        self.gt_button.set_active(self.display_gt)
        self.fp_button.set_active(self.display_fp)
        self.gti_button.set_active(self.display_gti)
        self.matchedgti_button.set_active(self.display_matchedgti)
        self.matchedtsi_button.set_active(self.display_matchedtsi)
        self.matchedgt_button.set_active(self.display_matchedgt)
        self.matchedts_button.set_active(self.display_matchedts)

    def on_destroy(self, *args):
        gtk.main_quit()

    def set_check_color(self, but, color):
        # but.modify_base(gtk.STATE_NORMAL, color)
        # but.modify_base(gtk.STATE_SELECTED, color)
        # but.modify_base(gtk.STATE_ACTIVE, color)
        # but.modify_base(gtk.STATE_PRELIGHT, color)
        # but.modify_base(gtk.STATE_INSENSITIVE, color)
        # but.child.modify_base(gtk.STATE_NORMAL, color)
        # but.modify_fg(gtk.STATE_NORMAL, color)
        but.child.modify_fg(gtk.STATE_NORMAL, color)
        but.child.modify_fg(gtk.STATE_SELECTED, color)
        but.child.modify_fg(gtk.STATE_ACTIVE, color)
        but.child.modify_fg(gtk.STATE_PRELIGHT, color)

        
    def set_title(self, title):
        self.main_window.set_title(title)

    def set_slider_params(self, xmin, xmax, digits):
        self.hscale1.set_range(xmin, xmax)
        self.hscale1.set_digits(digits)

    def get_slider_position(self):
        return self.hscale1.get_value()

    def display(self, img_filename, gts, positives,
                matched_gt = None, matched_ts = None, gti_prims = None,
                matched_gti = None, matched_tsi = None):
        self.displayer.set_image(img_filename)
        self.displayer.clear_gprims()
        # display groundtruth
        if self.display_gt:
            for gt in gts: 
                self.displayer.add_gprim(gt, self.color_gt)
        # display false positives
        if self.display_fp:
            for pos in positives:
                self.displayer.add_gprim(pos, self.color_fp)
        # display ignored groundtruth
        if self.display_gti:
            if gti_prims:
                for prim in gti_prims:
                    self.displayer.add_gprim(prim, self.color_gti)
        # display matched ignored groundtruth
        if self.display_matchedgti and matched_gti:
            for mgt in matched_gti:
                self.displayer.add_gprim(mgt, self.color_matchedgti)
        # display matched ignored input
        if self.display_matchedtsi and matched_tsi:
            for mgt in matched_tsi:
                self.displayer.add_gprim(mgt, self.color_matchedtsi)
        # display matched groundtruth        
        if self.display_matchedgt and matched_gt:
            for mgt in matched_gt:
                self.displayer.add_gprim(mgt, self.color_matchedgt)
        # display matched input
        if self.display_matchedts and matched_ts:
            for mts in matched_ts:
                self.displayer.add_gprim(mts, self.color_matchedts)
        self.displayer.draw()

    def on_key_press(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname == 'Right':
            self._on_next()
        if keyname == 'Left':
            self._on_prev()
        if keyname[:7] == 'Control':
            self.control_key = True
        if keyname == 's' and self.control_key == True:
            self._on_save()
        
    def on_key_release(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if keyname[:7] == 'Control':
            self.control_key = False
        
    def _on_activate(self, entry):
        self.on_activate(entry.get_text())
        return False

    def _on_conf_activate(self, entry):
        self.hscale1.set_value(float(entry.get_text()))
        self.on_slider_moved()
        return False

    def on_activate(self, text):
        pass

    def _on_save(self, *args):
        self.on_save(self.input_save.get_text())

    def on_save(self):
        pass

    def _on_next(self, *args):
        self.on_next()
        return False

    def on_next(self, *args):
        pass

    def on_clear(self, *args):
        self.boxes = []
        self.displayer.draw(self.boxes)

    def on_refresh():
        pass

    ############################################################################
    # check box actions
    
    def on_gt(self, *args):
        self.display_gt = self.gt_button.get_active()
        self.on_refresh()

    def on_fp(self, *args):
        self.display_fp = self.fp_button.get_active()
        self.on_refresh()

    def on_gti(self, *args):
        self.display_gti = self.gti_button.get_active()
        self.on_refresh()

    def on_matchedgti(self, *args):
        self.display_matchedgti = self.matchedgti_button.get_active()
        self.on_refresh()

    def on_matchedtsi(self, *args):
        self.display_matchedtsi = self.matchedtsi_button.get_active()
        self.on_refresh()

    def on_matchedgt(self, *args):
        self.display_matchedgt = self.matchedgt_button.get_active()
        self.on_refresh()

    def on_matchedts(self, *args):
        self.display_matchedts = self.matchedts_button.get_active()
        self.on_refresh()

    ############################################################################
    # keyboard actions
    
    def on_button_press(self, widget, event):
        if event.button == 1:
            self.button1 = True
            self.button1_origin = (max(0, event.y), max(0, event.x))

    def on_button_release(self, widget, event):
        if event.button == 1:
            self.button1 = False
            o = self.button1_origin
            w0 = max(0, min(o[1], event.x))
            h0 = max(0, min(o[0], event.y))
            w1 = max(w0, max(o[1], event.x))
            h1 = max(h0, max(o[0], event.y))
            self.boxes.append(BoundingBox(w0, h0, w1, h1))
            self.displayer.draw(self.boxes)

    def on_motion_notify(self, widget, event):
        if self.button1:
            o = self.button1_origin
            w0 = max(0, min(o[1], event.x))
            h0 = max(0, min(o[0], event.y))
            w = max(o[1], event.x) - w0
            h = max(o[0], event.y) - h0
            r = Rectangle(w0, h0, w, h)
            context = cairo.Context(self.displayer.surface)
            self.displayer.draw()
            context.set_source_rgb(.5, 0, .5)
            r.draw(context)

    def _on_prev(self, *args):
        self.on_prev()
        return False

    def on_prev(self):
        pass

    def _on_slider_moved(self, *args):
        self.confidence_input.set_text(str(self.get_slider_position()))
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
