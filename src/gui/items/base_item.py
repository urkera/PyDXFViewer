from uuid import uuid4

from PySide2.QtGui import QPen, QColor, QPainterPathStroker, QPainterPath, QPainter
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget


class BaseItem(QGraphicsItem):
    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)
        self._layer = None
        self._color = 'layer'
        self._name = uuid4().hex
        self._pen_width = 0.0
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    # <-- getters setters and properties -->
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    name = property(fget=get_name, fset=set_name)

    def get_layer(self):
        return self._layer

    def set_layer(self, layer):
        self._layer = layer

    layer = property(fget=get_layer, fset=set_layer)

    def get_color(self):
        if self._color == 'layer':
            self._color = self.layer.color
        return self._color

    def set_color(self, value):
        if value == 'layer':
            self._color = self.layer.color
        else:
            self._color = QColor(*value)

    color = property(fget=get_color, fset=set_color)

    def get_pen_width(self):
        return self._pen_width

    def set_pen_width(self, pen_width):
        self._pen_width = pen_width

    pen_width = property(fget=get_pen_width, fset=set_pen_width)

    def get_pen(self):
        pen = QPen()
        pen.setColor(self.color)
        pen.setWidthF(self.pen_width)
        return pen

    def draw_shape(self, painter_path):
        pass

    def shape(self):
        ps = QPainterPathStroker()
        path = QPainterPath()
        self.draw_shape(path)
        ps.setWidth(self.pen_width)
        return ps.createStroke(path)

    def boundingRect(self):
        return self.shape().boundingRect()

    def paint(self, painter=QPainter, option=QStyleOptionGraphicsItem, widget=QWidget):
        painter.setPen(self.get_pen())
        painter.setClipRect(option.exposedRect)
        self.draw_item(painter, option, widget)
