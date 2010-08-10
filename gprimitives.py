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

class GPrimitive(object):
    def __init__(self):
        super(GPrimitive, self).__init__()

    def draw(self):
        pass

class Rectangle(object):
    def __init__(self, x1, y1, w, h):
        super(Rectangle, self).__init__()
        self.x1 = x1
        self.y1 = y1
        self.w = w
        self.h = h

    def draw(self, context):
        context.rectangle(self.x1, self.y1, self.w, self.h)
        context.stroke()
