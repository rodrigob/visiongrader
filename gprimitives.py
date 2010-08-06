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
