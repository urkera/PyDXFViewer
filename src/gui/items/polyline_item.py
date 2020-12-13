import math

from PySide2.QtGui import QPolygonF

from src.core.utils import get_point
from src.gui.items.base_item import BaseItem


class PolyLineItem(BaseItem):
    def __init__(self, *args, **kwargs):
        super(PolyLineItem, self).__init__()
        self.points = [get_point(p) for p in args]
        self.closed = kwargs.pop('closed')
        self._polygon = QPolygonF(QPolygonF.fromList(self.points))

    def length(self):
        total_length = 0
        for i in range(len(self.points) - 1):
            delta = self.points[i] - self.points[i + 1]
            total_length += math.sqrt(delta.x() ** 2 + delta.y() ** 2)
        return total_length

    def __repr__(self):
        points = ','.join([str(p) for p in self.points])
        text = f'Polyline(points=[{points}], total_length={self.length()}'
        return text

    def draw_shape(self, painter_path):
        painter_path.moveTo(self.points[0])
        for i in range(1, len(self.points)):
            painter_path.lineTo(self.points[i])

    def draw_item(self, painter, option, widget):
        painter.drawPolyline(self._polygon)
