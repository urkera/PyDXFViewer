import sys

from PySide2.QtWidgets import QApplication

from src.core.dxf_handler import DXFHandler
from src.core.utils import read_ncn
from src.gui.layer import Layer
from src.gui.main_window import MainWindow


class ApplicationWindow(MainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.test_read_ncn('src/tests/M_ABIDE_APL.ASC')
        # self.test_dxf_handler('src/tests/test.dxf')
        # self.graphicsView.create_line_item((0, 0), (0, 100))
        # self.graphicsView.create_line_item((0, 0), (100, 0))
        # for i in self.graphicsView.items():
        #     print('')

        self.graphicsView.line_drawing = True
        self.graphicsView.mouse_move.connect(self.get_position)

    def get_position(self, position):
        self.statusBar().showMessage('x: {x:.3f} y: {y:.3f}'.format(x=position[0], y=position[1]))

    def test_read_ncn(self, file_name):
        points = read_ncn(file_name)
        layer_name = file_name.split('/')[-1].split('.')[0]
        self.graphicsView.create_layer(layer_name, '#0f0')
        for point in points:
            self.graphicsView.create_point_item(name=point[0], coordinates=point[1:])
            if point[0].startswith('ASF'):
                self.graphicsView.create_text_item(text=point[0], position=point[1:3], attachment_point='TOP_CENTER')
        # self.graphicsView.create_text_item(text=points[0][0], position=(0, 0), attachment_point='MIDDLE_CENTER')
        # print(self.graphicsView.layers)
        self.graphicsView.show_all()

    def test_dxf_handler(self, file_name):
        dxf_handler = DXFHandler(file_name)

        for layer in dxf_handler.get_layers():
            self.graphicsView.add_layer(Layer(name=layer['name'], color=layer['color']))

        lines = dxf_handler.get_lines()
        for line in lines:
            # line_item = LineItem(line.dxf.start, line.dxf.end)
            # self.graphicsView.get_layer_by_name(line.dxf.layer).add_item(line_item)
            self.graphicsView.create_line_item(line.dxf.start, line.dxf.end, layer=line.dxf.layer)

        p_lines = dxf_handler.get_p_lines()
        for p_line in p_lines:
            # p_line_item = PolyLineItem(*p_line.points(), closed=p_line.is_closed)
            # self.graphicsView.get_layer_by_name(p_line.dxf.layer).add_item(p_line_item)
            self.graphicsView.create_polyline_item(p_line.points, p_line.is_closed, layer=p_line.dxf.layer)

        texts = dxf_handler.get_texts()
        for text in texts:
            print(text.dxf.style)


def main():
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
