import math

from PySide2.QtGui import QPainter, QPolygonF
from PySide2.QtWidgets import QWidget, QStyleOptionGraphicsItem

from .base_item import BaseItem, BasePoint


class PolyLineItem(BaseItem):
    def __init__(self, *args, **kwargs):
        super(PolyLineItem, self).__init__()
        self.points = [BasePoint(*p) for p in args]
        self.closed = kwargs.pop('closed')
        self._polygon = QPolygonF(QPolygonF.fromList(self.points))

    def length(self):
        total_length = 0
        for i in range(len(self.points) - 1):
            delta = self.points[i] - self.points[i + 1]
            total_length += math.sqrt(delta.x() ** 2 + delta.y() ** 2)
        return total_length

    def boundingRect(self):
        return self._polygon.boundingRect()

    def paint(self, painter=QPainter, option=QStyleOptionGraphicsItem, widget=QWidget):
        painter.setPen(self.get_pen())
        if self.closed:
            painter.drawPolygon(self._polygon)
        else:
            painter.drawPolyline(self._polygon)
