from PySide2.QtGui import QColor

ON = 1
OFF = 0


class Layer(object):
    def __init__(self, name, color=QColor(r=0, g=0, b=0), status=ON):
        self.name = name
        self._color = QColor(color)

        self.status = status

        self._items = []

        self.scene = None

    def __repr__(self):
        return f'Layer(\'name\': \'{self.name}\', \'color\': \'{self.color.name()}\', \'status\': \'{self.status}\')'

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = QColor(*value)

    @property
    def items(self):
        return self._items

    def add_item(self, item):
        item.layer = self
        self.items.append(item)
        self.scene.addItem(item)
        self.scene.update()

    def remove_item(self, item):
        self.items.remove(item)
        self.scene.removeItem(item)
        self.scene.update()
