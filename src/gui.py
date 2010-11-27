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
import core
import Queue
import os
import os.path
import modules

class MainGUI(object):
    def __init__(self):
        self.main_path = os.path.join(os.getcwd(), os.path.dirname(sys.argv[0]))
        self.parser_dir = None
        self.parsers = None
        self.set_parser_dir("parsers")
        self.comparator_dir = None
        self.comparators = None
        self.set_comparator_dir("comparators")

        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_window.connect("destroy", self.on_destroy)
        
        self.vbox1 = gtk.VBox(2)
        self.main_window.add(self.vbox1)
        self.vbox1.set_homogeneous(False)

        self.mode_hbox = gtk.HBox(2)
        self.vbox1.pack_start(self.mode_hbox)
        self.mode_hbox.pack_start(gtk.Label("Mode : "))
        self.mode_combobox = gtk.combo_box_new_text()
        self.mode_hbox.pack_start(self.mode_combobox)
        self.mode_combobox.append_text("DET")
        self.mode_combobox.append_text("ROC")
        self.mode_combobox.append_text("Display")
        self.mode_combobox.append_text("Single file")
        self.mode_combobox.set_active(0)
        self.mode_combobox.connect("changed", self.on_mode_changed)

        self.main_viewport = gtk.Viewport()
        self.vbox1.pack_start(self.main_viewport)

        self.main_window.show_all()

    def on_destroy(self, *args):
        gtk.main_quit()

    def on_mode_changed(self, *args):
        mode = self.mode_combobox.get_active()
        if mode == 2:
            self.build_mode_display()

    def set_parser_dir(self, parser_dir):
        if self.parser_dir != parser_dir:
            self.parser_dir = parser_dir
            self.parsers = modules.ModuleHandler(self.main_path, parser_dir)

    def set_comparator_dir(self, comparator_dir):
        if self.comparator_dir != comparator_dir:
            self.comparator_dir = comparator_dir
            self.comparators = modules.ModuleHandler(self.main_path,
                                                     comparator_dir)

    def get_parser_list(self):
        return self.parsers.get_modules_names()

    def get_parser(self, name):
        return self.parsers.get_module(name)

    def get_parser_by_index(self, i):
        return self.get_parser(self.get_parser_list()[i])

    def params_prompt(self, widget, on_ok, gt, ts, comp):
        possible_params = [("gt", 2), ("ts", 2), ("comp", 2)]
        n_params = sum([p[1] for p in possible_params if locals()[p[0]] ==True])
        table = gtk.Table(n_params+1, 2)
        widget.add(table)
        i_row = 0
        fields = {}
        
        def add_parser(label_parser, label_file, chooser_title,
                       field_label_parser, field_label_file,
                       i_row, self = self):
            table.attach(gtk.Label(label_parser), 0, 1, i_row, i_row+1)
            parser_combo = gtk.combo_box_new_text()
            table.attach(parser_combo, 1, 2, i_row, i_row+1)
            for parser in self.get_parser_list():
                parser_combo.append_text(parser)
            parser_combo.set_active(0)
            fields[field_label_parser] = parser_combo

            table.attach(gtk.Label(label_file), 0, 1, i_row+1, i_row+2)
            filename_chooser = gtk.FileChooserButton(chooser_title)
            table.attach(filename_chooser, 1, 2, i_row+1, i_row+2)
            fields[field_label_file] = filename_chooser

            def on_combo_changed(widget, chooser = filename_chooser,
                                 self = self):
                if self.get_parser_by_index(widget.get_active()).path_is_folder:
                    chooser.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
                else:
                    chooser.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
            parser_combo.connect("changed", on_combo_changed)

        if gt:
            add_parser("groundtruth parser", "groundtruth file",
                       "choose groundtruth",
                       "gt_parser_combo", "gt_filename_chooser", i_row)
            i_row += 2
        if ts:
            add_parser("input parser", "input file", "choose input",
                       "ts_parser_combo", "ts_filename_chooser", i_row)
            i_row += 2
        if comp:
            table.attach(gtk.Label("comparator : "), 0, 1, i_row, i_row+1)
            comp_combo = gtk.combo_box_new_text()
            table.attach(comp_entry, 1, 2, i_row, i_row+1)
            table.attach(gtk.Label("comparator directory : "), 0, 1, i_row+1,
                         i_row+2)
            comp_dir_entry = gtk.Entry()
            table.attach(comp_dir_entry, 1, 2, i_row+1, i_row+2)
            i_row += 2

        ok_button = gtk.Button("Ok")
        table.attach(ok_button, 1, 2, i_row, i_row+1)
        ok_button.connect("clicked", on_ok, fields)
        
        table.show_all()
    
    def build_mode_display(self):
        self.params_prompt(self.main_viewport, self.on_ok_display_params,
                           True, True, False)

    def on_ok_display_params(self, widget, fields):
        def set_legend(text):
            pass
        core.display(fields["ts_filename_chooser"].get_filenames()[0],
                     self.get_parser_by_index(fields["ts_parser_combo"]
                                              .get_active()),
                     fields["gt_filename_chooser"].get_filenames()[0],
                     self.get_parser_by_index(fields["gt_parser_combo"]
                                              .get_active()),
                     None, self.main_viewport, set_legend)
                     
        

if __name__=="__main__":
    gui = MainGUI()
    gtk.main()
