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

class slist(object):
    '''Sorted list with unique values'''
    def __init__(self, init = []):
        self.contents = sorted(init)

    def insert(self, elem):
        '''Inserts an element keeping the list sorted. Does nothing if the element already exists.'''
        index = self.find_index(elem)
        if index != -1:
            if self.contents[index] == elem:
                return
        self.contents.insert(index + 1, elem)

    def find_index(self, elem):
        '''Returns the index of elem. If it does not belong to the list, it returns max{i | self[i] < elem}.
        It returns -1 if that set is empty.'''
        if self.contents == []:
            return -1
        elif elem < self.contents[0]:
            return -1
        elif self.contents[-1] <= elem:
            return len(self.contents) - 1
        else:
            i1 = 0
            i2 = len(self.contents) - 1
            while (i1 != i2 - 1):
                i3 = (i1 + i2) / 2
                if self.contents[i3] <= elem:
                    i1 = i3
                else:
                    i2 = i3
            return i1

    def __len__(self):
        '''Returns the length of the list.'''
        return len(self.contents)

    def __getitem__(self, i):
        '''Returns the i-th element of the list.'''
        return self.contents[i]

    def __str__(self):
        return str(self.contents)
