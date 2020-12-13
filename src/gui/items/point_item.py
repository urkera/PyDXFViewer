from src.core.utils import get_point
from src.gui.items.base_item import BaseItem


class PointItem(BaseItem):
    def __init__(self, point, *args, **kwargs):
        super(PointItem, self).__init__(*args, **kwargs)
        self._name = kwargs.pop('name')
        self.point = get_point(point)

    def __repr__(self):
        return f'Point(\'{self.name}\',[{self.point.x()}, {self.point.y()}, {self.point.z()}])'

    def draw_shape(self, painter_path):
        painter_path.addRect(self.point.x() - 2, self.point.y() - 2, 4, 4)

    def draw_item(self, painter, option, widget):
        painter.drawPoint(self.point)
