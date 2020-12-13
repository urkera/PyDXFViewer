from PySide2.QtCore import QPoint, QPointF
from ezdxf.math import Vector

from src.core.base_point import BasePoint


def read_ncn(file_name):
    with open(file_name, 'r') as f:
        content = f.read()
    data = [d.strip().split()[:-7] for d in content.strip().split('\n')]
    return [[p[0], float(p[1]), float(p[2]), float(p[3])] for p in data]


def euclidean_dist(p1, p2):
    delta = p1 - p2.point
    return delta.x() ** 2 + delta.y() ** 2


def get_point(item_or_point):
    if isinstance(item_or_point, (tuple, Vector)):
        return BasePoint(*item_or_point)
    if isinstance(item_or_point, (QPoint, QPointF)):
        return BasePoint(item_or_point.x(), item_or_point.y())
