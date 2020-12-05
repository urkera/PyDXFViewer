from PySide2.QtCore import QRectF, QSize, QPointF
from PySide2.QtGui import QFont, QFontMetrics

from .base_item import BaseItem

TEXT_ATTACHMENT_POINT = {
    'TOP_LEFT': 1, 'TOP_CENTER': 2, 'TOP_RIGHT': 3,
    'MIDDLE_LEFT': 4, 'MIDDLE_CENTER': 5, 'MIDDLE_RIGHT': 6,
    'BOTTOM_LEFT': 7, 'BOTTOM_CENTER': 8, 'BOTTOM_RIGHT': 9,
}


class TextItem(BaseItem):
    def __init__(self, text, position, attachment_point, *args, **kwargs):
        super(TextItem, self).__init__(*args, **kwargs)
        self.text = text
        self.angle = kwargs.pop('angle')
        self.position = position
        self.font = QFont('Arial', 5)
        metrics = QFontMetrics(self.font)
        self.w = metrics.width(self.text)
        self.h = metrics.height()
        self.attachment_point = attachment_point

    def get_start_point(self):
        point = QPointF(0, 0)
        if self.attachment_point == 1:  # TOP_LEFT
            point += QPointF(0, 0)
        if self.attachment_point == 2:  # TOP_CENTER
            point += QPointF(-self.w / 2, 0)
        if self.attachment_point == 3:  # TOP_RIGHT
            point += QPointF(-self.w, 0)
        if self.attachment_point == 4:  # MIDDLE_LEFT
            point += QPointF(0, -self.h / 2)
        if self.attachment_point == 5:  # MIDDLE_CENTER
            point += QPointF(-self.w / 2, -self.h / 2)
        if self.attachment_point == 6:  # MIDDLE_RIGHT
            point += QPointF(-self.w, -self.h / 2)
        if self.attachment_point == 7:  # BOTTOM_LEFT
            point += QPointF(0, -self.h)
        if self.attachment_point == 8:  # BOTTOM_CENTER
            point += QPointF(-self.w / 2, -self.h)
        if self.attachment_point == 9:  # BOTTOM_RIGHT
            point += QPointF(-self.w, -self.h)
        return point

    def __repr__(self):
        return f'Text({self.text})'

    def boundingRect(self):
        return QRectF(self.position + self.get_start_point(), QSize(self.w, self.h)).normalized()

    def paint(self, painter, option, widget):
        """ because of the y axis flipped painter needs to be flipped too"""
        painter.setPen(self.get_pen())
        painter.save()
        painter.setFont(self.font)
        painter.translate(self.position)
        painter.scale(1, -1)
        painter.drawText(self.get_start_point(), self.text)
        painter.restore()
