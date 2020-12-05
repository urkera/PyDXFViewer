from PySide2.QtCore import QRectF, QSize, QPointF
from PySide2.QtGui import QFont, QFontMetrics, QTransform
from PySide2.QtWidgets import QGraphicsItem

from .base_item import BaseItem


# ATTACHMENT_POINT = {
#     'MTEXT_TOP_LEFT': 1, 'MTEXT_TOP_CENTER': 2, 'MTEXT_TOP_RIGHT': 3,
#     'MTEXT_MIDDLE_LEFT': 4, 'MTEXT_MIDDLE_CENTER': 5, 'MTEXT_MIDDLE_RIGHT': 6,
#     'MTEXT_BOTTOM_LEFT': 7, 'MTEXT_BOTTOM_CENTER': 8, 'MTEXT_BOTTOM_RIGHT': 9,
# }
#
# TEXT_STYLE = {
#     'STANDARD': QFont('Arial', ),
#     'ARIAL': 0,
#     'ARIAL_BOLD': 0,
#     'ARIAL_ITALIC': 0,
#     'ARIAL_BOLD_ITALIC': 0,
#     'ARIAL_BLACK': 0,
#     'ISOCPEUR': 0,
#     'ISOCPEUR_ITALIC': 0,
#     'TIMES': 0,
#     'TIMES_BOLD': 0,
#     'TIMES_ITALIC': 0,
#     'TIMES_BOLD_ITALIC': 0,
# }


class TextItem(BaseItem):
    def __init__(self, text, position, *args, **kwargs):
        super(TextItem, self).__init__(*args, **kwargs)
        self.text = text
        self.angle = kwargs.pop('angle')
        self.position = position  # QPointF(position.x(), -1 * position.y())
        self.font = QFont('Arial', 12)
        self.font_metrics = QFontMetrics(self.font)

        self.width = self.font_metrics.width(self.text)
        self.height = self.font_metrics.height()

    def __repr__(self):
        return f'Text({self.text})'

    def boundingRect(self):
        return QRectF(self.position, QSize(self.width, self.height)).normalized()

    def paint(self, painter, option, widget):
        painter.save()
        painter.translate(self.position + QPointF(self.width / 2, self.height / 2))
        painter.scale(1, -1)
        painter.setPen(self.get_pen())
        painter.drawText(QRectF(-self.width, self.height/2, self.width, self.height), self.text)
        painter.restore()
