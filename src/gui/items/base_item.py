from uuid import uuid4

from PySide2.QtCore import QPointF
from PySide2.QtGui import QPen
from PySide2.QtWidgets import QGraphicsItem


class BasePoint(QPointF):
    def __init__(self, x, y, z=0):
        super(BasePoint, self).__init__(x, y)
        self._z = z

    def z(self):
        return self._z

    def set_z(self, z):
        self._z = z


class BaseItem(QGraphicsItem):
    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)
        self._layer = None
        self._color = 'layer'
        self._name = uuid4().hex
        self._pen_width = 0.0

    def boundingRect(self):
        """this function must be overridden"""
        return super(BaseItem, self).boundingRect()

    def paint(self, painter, option, widget):
        """this function must be overridden"""
        painter.setPen(self.get_pen())
        painter.drawLine(self._line)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, layer):
        self._layer = layer

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def pen_width(self):
        return self._pen_width

    @pen_width.setter
    def pen_width(self, pen_width):
        self._pen_width = pen_width

    def get_pen(self):
        pen = QPen()
        pen.setColor(self.layer.color if self.color == 'layer' else self._color)
        pen.setWidthF(self._pen_width)
        return pen
