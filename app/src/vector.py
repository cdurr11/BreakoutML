class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def reflect_x(self):
        return Vector(-1*self.x, self.y)

    def reflect_y(self):
        return Vector(self.x, -1*self.y)

    def __eq__(self, other):
        return isinstance(other, Vector) and other.get_x() == self.get_x() \
                                         and other.get_y() == self.get_y()

    def __repr__(self):
        return "(x: {}, y: {})".format(self.get_x(), self.get_y())
