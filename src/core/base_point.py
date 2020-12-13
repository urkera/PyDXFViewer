from PySide2.QtCore import QPointF


class BasePoint(QPointF):
    def __init__(self, x, y, z=0):
        super(BasePoint, self).__init__(x, y)
        self._z = z
        __str__ = self.__repr__

    def __repr__(self):
        return f'Point({self.x()}, {self.y()}, {self.z()})'

    def z(self):
        return self._z

    def set_z(self, z):
        self._z = z
