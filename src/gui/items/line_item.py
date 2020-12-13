import math

from src.core.utils import get_point
from src.gui.items.base_item import BaseItem


class LineItem(BaseItem):
    def __init__(self, p1, p2, *args, **kwargs):
        super(LineItem, self).__init__(*args, **kwargs)
        self.p1 = get_point(p1)
        self.p2 = get_point(p2)

    def get_p1(self):
        return self.p1

    def set_p1(self, p):
        self.prepareGeometryChange()
        self.p1 = get_point(p)

    point1 = property(fget=get_p1, fset=set_p1)

    def get_p2(self):
        return self.p2

    def set_p2(self, p):
        self.prepareGeometryChange()
        self.p2 = get_point(p)

    point2 = property(fget=get_p2, fset=set_p2)

    def length(self):
        delta = self.p1 - self.p2
        return math.sqrt(delta.x() ** 2 + delta.y() ** 2)

    def __repr__(self):
        return f'Line([{self.point1.x():.3f}, {self.point1.y():.3f}], ' + \
               f'[{self.point2.x():.3f}, {self.point2.y():.3f}], ' + \
               f'length={self.length():.3f})'

    def draw_shape(self, painter_path):
        painter_path.moveTo(self.point1)
        painter_path.lineTo(self.point2)

    def draw_item(self, painter, option, widget):
        painter.drawLine(self.point1, self.point2)
