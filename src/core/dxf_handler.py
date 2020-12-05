import ezdxf as ez
from PySide2.QtGui import QColor
from ezdxf.tools.rgb import DXF_DEFAULT_COLORS, int2rgb


class DXFHandler(object):
    def __init__(self, f_name):
        self.doc = ez.readfile(f_name)
        self.model_space = self.doc.modelspace()
        # print(ez.sections.tables.Table)

    def get_layers(self):
        for layer in self.doc.layers:
            yield {'name': layer.dxf.name, 'color': QColor(*int2rgb(DXF_DEFAULT_COLORS[layer.color]))}

    @property
    def layers(self):
        return self.doc.layers

    def get_texts(self):
        for text in self.model_space.query('TEXT'):
            yield text

    def get_lines(self):
        for line in self.model_space.query('LINE'):
            yield line

    def get_p_lines(self):
        for p_line in self.model_space.query('POLYLINE'):
            yield p_line
