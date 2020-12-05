from PySide2.QtCore import QRectF

from src.gui.items.base_item import BaseItem, BasePoint


class PointItem(BaseItem):
    def __init__(self, point, *args, **kwargs):
        super(PointItem, self).__init__(*args, **kwargs)
        self._name = kwargs.pop('name')
        self.point = BasePoint(*point)

    def __repr__(self):
        return f'Point(\'{self.name}\',[{self.point.x()}, {self.point.y()}, {self.point.z()}])'

    def boundingRect(self):
        rect = QRectF(self.point, self.point)
        rect.setWidth(1)
        rect.setHeight(1)
        return rect

    def paint(self, painter, option, widget):
        painter.setPen(self.get_pen())
        painter.drawPoint(self.point)
