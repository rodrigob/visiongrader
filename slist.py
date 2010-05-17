class slist(object):
    '''Sorted list'''
    def __init__(self, init = []):
        self.contents = sorted(init)

    def insert(self, elem):
        '''Inserts an element keeping the list sorted'''
        if self.contents == []:
            self.contents = [elem]
        elif elem < self.contents[0]:
            self.contents.insert(0, elem)
        elif self.contents[-1] < elem:
            self.contents.append(elem)
        else:
            i1 = 0
            i2 = len(self.contents) - 1
            while (i1 != i2 - 1):
                i3 = (i1 + i2) / 2
                if self.contents[i3] < elem:
                    i1 = i3
                else:
                    i2 = i3
            self.contents.insert(i1 + 1, elem)

    def __len__(self):
        '''Returns the length of the list'''
        return len(self.contents)

    def __getitem__(self, i):
        '''Returns the i-th element of the list'''
        return self.contents[i]

    def __str__(self):
        return str(self.contents)
