import math

from PySide2.QtCore import QLineF, QRectF
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QWidget, QStyleOptionGraphicsItem

from .base_item import BaseItem, BasePoint


class LineItem(BaseItem):
    def __init__(self, p1, p2, *args, **kwargs):
        super(LineItem, self).__init__(*args, **kwargs)
        self.p1 = BasePoint(*p1)
        self.p2 = BasePoint(*p2)
        self._line = QLineF(self.p1, self.p2)

    def length(self):
        delta = self.p1 - self.p2
        return math.sqrt(delta.x() ** 2 + delta.y() ** 2)

    def __repr__(self):
        return f'Line([{self.p1.x()}, {self.p1.y()}], [{self.p2.x()}, {self.p2.y()}])'

    def boundingRect(self):
        return QRectF(self.p1, self.p2).normalized()

    def paint(self, painter=QPainter, option=QStyleOptionGraphicsItem, widget=QWidget):
        painter.setPen(self.get_pen())
        painter.drawLine(self._line)
