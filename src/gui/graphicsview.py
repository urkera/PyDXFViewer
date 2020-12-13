from PySide2.QtCore import QRectF, Qt, QPointF, Signal, QPoint
from PySide2.QtGui import QTransform
from PySide2.QtWidgets import QGraphicsView

from src.core.utils import euclidean_dist
from src.gui.graphicsscene import GraphicsScene
from src.gui.items import (LineItem, PointItem, PolyLineItem, TextItem, TEXT_ATTACHMENT_POINT)
from src.gui.layer import Layer


class GraphicsView(QGraphicsView):
    mouse_move = Signal(tuple)  # Signal(QPointF) is not working

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setCursor(Qt.CrossCursor)

        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

        self.setTransform(QTransform(1, 0, 0, 0, -1, 0, 0, 0, 1))

        self._scene = GraphicsScene(self)
        self.setScene(self._scene)

        self._layers = []
        self._layer_names = []
        self._active_layer = None
        self.create_layer(name='Default', color='#0f0', set_active=True)

        self.control_pressed = False
        self.middle_pressed = False
        self.right_pressed = False
        self.drag_pos = None

        self.snap_point_mode = False

        self.draw_mode = 'None'
        self.drawn_line = None

        self.select_items = False

        self.initial_matrix = self.matrix()

        self.setMouseTracking(True)

        self.scale_factor = 1.0

    def create_groups(self):
        for layer in self.layers:
            self.scene().createItemGroup(layer.items)

    def get_closest_point_item(self, event):
        point = None
        top_left = event.pos() - QPoint(50, 50)
        bottom_right = event.pos() + QPoint(50, 50)
        items = self.items(QRectF(top_left, bottom_right).toRect())
        points = list(filter(lambda x: x if isinstance(x, PointItem) else None, items))
        if len(points) > 0:
            scene_pos = self.mapToScene(event.pos())
            dists = [euclidean_dist(scene_pos, p) for p in points]
            point = points[dists.index(min(dists))]
        return point

    def add_item(self, layer, item):
        layer = self.get_layer_by_name(layer)
        if not layer:
            layer = self.active_layer
        layer.add_item(item)
        self.scene().update()
        self.update()
        return item

    def create_point_item(self, name, coordinates, layer='active'):
        # layer = self.active_layer if layer == 'active' else self.get_layer_by_name(layer)
        point_item = PointItem(name=name, point=coordinates)
        return self.add_item(layer=layer, item=point_item)

    def create_line_item(self, point1, point2, layer='active'):
        # layer = self.active_layer if layer == 'active' else self.get_layer_by_name(layer)
        line_item = LineItem(point1, point2)
        return self.add_item(layer=layer, item=line_item)

    def create_polyline_item(self, points, closed, layer='active'):
        # layer = self.active_layer if layer == 'active' else self.get_layer_by_name(layer)
        polyline_item = PolyLineItem(*points, closed=closed)
        return self.add_item(layer=layer, item=polyline_item)

    def create_text_item(self, text, position, angle=0, layer='active', attachment_point=1):
        # layer = self.active_layer if layer == 'active' else self.get_layer_by_name(layer)
        text_item = TextItem(text=text, position=QPointF(*position), angle=angle,
                             attachment_point=TEXT_ATTACHMENT_POINT[attachment_point])
        return self.add_item(layer=layer, item=text_item)

    def remove_item(self, item):
        layer = item.layer
        layer.remove_item(item)

    # <--- Layer Functions --->
    def update_scene(self, arg):
        for layer in self.layers:
            if layer.status == 0:
                for item in layer.items:
                    item.hide()

    def add_layer(self, layer, active=False):
        if layer.name not in self.layer_names:
            self.layers.append(layer)
            self.layer_names.append(layer.name)
            layer.scene = self.scene()
            self.active_layer = layer if active else self.active_layer
            layer.status_changed.connect(self.update_scene)
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
        # trick:
        # if user zoom in or zoom out too much view exceeds matrix limit
        # so need to set view's matrix to initial matrix
        self.setMatrix(self.initial_matrix)
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
        if self.select_items:
            print(self.scene().selectedItems())
        scene_pos = self.mapToScene(event.pos())
        self.setCursor(Qt.CrossCursor)
        if event.button() == Qt.MidButton:
            self.middle_pressed = False
        if event.button() == Qt.RightButton:
            self.right_pressed = False

        if self.draw_mode == 'Line' and event.button() == Qt.RightButton:
            self.draw_mode = 'None'
            self.remove_item(self.drawn_line)

        if self.draw_mode == 'Line' and event.button() == Qt.LeftButton:
            point = scene_pos
            if self.snap_point_mode:
                point = self.get_closest_point_item(event)
                if not point:
                    return super(GraphicsView, self).mouseReleaseEvent(event)
            if self.drawn_line:
                self.drawn_line.point2 = point
                self.drawn_line.update()
                self.drawn_line = self.create_line_item(point, point)
            else:
                self.drawn_line = self.create_line_item(point, point)
        super(GraphicsView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        new_pos = event.pos()
        scene_pos = self.mapToScene(new_pos)
        # noinspection PyUnresolvedReferences
        self.mouse_move.emit((scene_pos.x(), scene_pos.y()))
        if self.draw_mode == 'Line' and self.drawn_line:
            self.drawn_line.point2 = scene_pos
            self.drawn_line.update()

        if self.draw_mode == 'Line' and event.button() == Qt.RightButton:
            self.draw_mode = 'None'
            self.remove_item(self.drawn_line)

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

        if event.delta() > 0:
            zoom_factor = in_factor
        else:
            zoom_factor = out_factor
        # a = self.matrix().scale(zoom_factor, zoom_factor).mapRect(QRectF(0, 0, 1, 1)).width()
        # print(self.matrix())
        # if a > 750 or a < 0.001:
        #     return

        old_pos = self.mapToScene(event.pos())
        self.scale(zoom_factor, zoom_factor)

        delta = self.mapToScene(event.pos()) - old_pos
        self.translate(delta.x(), delta.y())
        # self.scene().update()
