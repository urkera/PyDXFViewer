from PySide2.QtCore import QRectF, Qt, QPointF
from PySide2.QtGui import QTransform, QBrush, QColor
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene

from src.gui.items.line_item import LineItem
from src.gui.items.point_item import PointItem
from src.gui.items.polyline_item import PolyLineItem
from src.gui.items.text_item import TextItem
from src.gui.layer import Layer


class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setCursor(Qt.CrossCursor)

        # Transforming view's coordinate system
        #
        # .-------> x                  ^ y
        # |                            |
        # |                            |
        # |            Transform ==>   |
        # |                            |
        # v                            |
        # y                            .-------> x

        self.setTransform(QTransform(1, 0, 0, 0, -1, 0, 0, 0, 1))

        self.setSceneRect(QRectF(-5000000., -5000000., 10000000., 10000000.))

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self.setBackgroundBrush(QBrush(QColor(0, 0, 0)))

        self._layers = []
        self._layer_names = []
        self._active_layer = None
        self.create_layer(name='Default', color='#0f0', set_active=True)

        self.control_pressed = False
        self.middle_pressed = False
        self.right_pressed = False
        self.drag_pos = None

        self.scale_factor = 1.0

    def add_item(self, layer, item):
        layer = self.get_layer_by_name(layer)
        if not layer:
            layer = self.active_layer
        layer.add_item(item)
        self.scene().update()

    def create_point_item(self, name, coordinates, layer='active'):
        layer = self.active_layer if layer == 'active' else self.get_layer_by_name(layer)
        self.add_item(layer=layer, item=PointItem(name=name, point=coordinates))

    def create_line_item(self, point1, point2, layer='active'):
        layer = self.active_layer if layer == 'active' else self.get_layer_by_name(layer)
        self.add_item(layer=layer, item=LineItem(point1, point2))

    def create_polyline_item(self, points, closed, layer='active'):
        layer = self.active_layer if layer == 'active' else self.get_layer_by_name(layer)
        self.add_item(layer=layer, item=PolyLineItem(*points, closed))

    def create_text_item(self, text, position, angle=0, layer='active'):
        layer = self.active_layer if layer == 'active' else self.get_layer_by_name(layer)
        self.add_item(layer=layer, item=TextItem(text=text, position=QPointF(*position), angle=angle))

    # <--- Layer Functions --->

    def add_layer(self, layer, active=False):
        if layer.name not in self.layer_names:
            self.layers.append(layer)
            self.layer_names.append(layer.name)
            layer.scene = self.scene()
            self.active_layer = layer if active else self.active_layer
            return layer
        else:
            return False

    def create_layer(self, name, color, status=1, set_active=False):
        layer = Layer(name, color, status)
        return self.add_layer(layer, set_active)

    def remove_layer(self, l_name):
        try:
            index = self.layer_names.index(l_name)
            self.layer_names.remove(l_name)
            layer = self.layers.pop(index)
            for item in layer.items:
                self.scene().removeItem(item)
            return True
        except ValueError:
            return False

    def get_layer_by_name(self, l_name):
        try:
            return self.layers[self.layer_names.index(l_name)]
        except ValueError:
            return False

    # <--- Properties --->

    @property
    def layers(self):
        return self._layers

    @property
    def active_layer(self):
        return self._active_layer

    @active_layer.setter
    def active_layer(self, layer):
        self._active_layer = layer

    @property
    def layer_names(self):
        return self._layer_names

    # <--- Visibility --->

    def get_visible_items(self):
        return [item for item in self.scene().items() if item.layer.status == 1]

    def show_all(self):
        items = self.get_visible_items()
        rect = QRectF()
        for i in items:
            rect = rect.united(i.boundingRect())
        # it is not working properly without updating the rect
        # need to set new position and edit rect's size
        rect.setX(rect.x() - 1)
        rect.setY(rect.y() - 1)
        rect.setWidth(rect.width() + 1)
        rect.setHeight(rect.height() + 1)
        self.fitInView(rect, Qt.KeepAspectRatio)

    # <--- Mouse And Key Events --->

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.control_pressed = True
        super(GraphicsView, self).keyReleaseEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.control_pressed = False
        super(GraphicsView, self).keyPressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self.control_pressed:
            self.show_all()
        # if event.button() == Qt.RightButton and self.control_pressed:
        #     self.remove_layer('Default')
        return super(GraphicsView, self).mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        self.drag_pos = event.pos()
        if event.button() == Qt.MidButton:
            self.middle_pressed = True
        if event.button() == Qt.RightButton:
            self.right_pressed = True
        super(GraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CrossCursor)
        if event.button() == Qt.MidButton:
            self.middle_pressed = False
        if event.button() == Qt.RightButton:
            self.right_pressed = False
        super(GraphicsView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        new_pos = event.pos()
        if self.middle_pressed:
            diff = new_pos - self.drag_pos
            self.drag_pos = new_pos
            self.setCursor(Qt.ClosedHandCursor)
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
            event.accept()
        super(GraphicsView, self).mouseMoveEvent(event)

    def wheelEvent(self, event):
        # https://stackoverflow.com/a/29026916
        in_factor = 1.25
        out_factor = 1 / in_factor

        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        old_pos = self.mapToScene(event.pos())

        if event.delta() > 0:
            zoom_factor = in_factor
        else:
            zoom_factor = out_factor
        self.scale(zoom_factor, zoom_factor)

        delta = self.mapToScene(event.pos()) - old_pos
        self.translate(delta.x(), delta.y())
