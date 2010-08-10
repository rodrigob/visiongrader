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

import os
import os.path
import sys

class ModuleHandler(object):
    def __init__(self, module_dir, module_name):
        self.modules = {}
        self.module_name = module_name
        modules_names = os.listdir(os.path.join(module_dir, module_name))
        if module_dir not in sys.path:
            sys.path.append(os.path.abspath(module_dir))
            #sys.path.append(os.path.abspath(os.path.join(module_dir, module_name)))
            remove_from_path = True
        else:
            remove_from_path = False
        #for name in modules_names:
        #    if self.is_a_module_name(name):
        #        #name = "%s.%s"%(module_name, name[:-3])
        #        name = name[:-3]
        #        __import__(name)
        #        self.modules[name] = sys.modules[name]
        __import__(module_name)
        for name in modules_names:
            if self.is_a_module_name(name):
                name = name[:-3]
                modname = "%s.%s"%(module_name, name)
                __import__(modname)
                self.modules[name] = sys.modules[modname]
        if remove_from_path:
            sys.path.remove(os.path.abspath(module_dir))
            #sys.path.remove(os.path.abspath(os.path.join(module_dir, module_name)))

    def is_a_module_name(self, name):
        return name[-3:] == ".py" and name != "__init__.py"

    def get_modules_names(self):
        return self.modules.keys()

    def get_module(self, name):
        return self.modules[name]
