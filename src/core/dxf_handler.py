import ezdxf as ez
from PySide2.QtGui import QColor
from ezdxf.tools.rgb import DXF_DEFAULT_COLORS, int2rgb


class DXFHandler(object):
    def __init__(self, f_name):
        self.doc = ez.readfile(f_name)
        self.model_space = self.doc.modelspace()

    def get_layers(self):
        for layer in self.doc.layers:
            yield {'name': layer.dxf.name, 'color': QColor(*int2rgb(DXF_DEFAULT_COLORS[layer.color]))}

    @property
    def layers(self):
        return self.doc.layers

    def get_texts(self):
        return self.model_space.query('TEXT')

    def get_lines(self):
        return self.model_space.query('LINE')

    def get_p_lines(self):
        return self.model_space.query('POLYLINE')
