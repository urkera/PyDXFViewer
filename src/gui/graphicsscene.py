from PySide2.QtCore import QRectF
from PySide2.QtGui import QBrush, QColor
from PySide2.QtWidgets import QGraphicsScene


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self.setSceneRect(QRectF(-50000000., -50000000., 100000000., 100000000.))

        self.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
