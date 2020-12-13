import sys

from PySide2.QtWidgets import QApplication

from src.core.dxf_handler import DXFHandler
from src.core.utils import read_ncn
from src.gui.main_window import MainWindow


class ApplicationWindow(MainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        # self.test_read_ncn('src/tests/M_ABIDE_APL.ASC')
        self.test_dxf_handler('src/tests/tekirdag.dxf')
        # print(len(self.graphicsView.scene().items()))

        # self.graphicsView.line_drawing = True
        self.graphicsView.mouse_move.connect(self.get_position)

        self.action_close.triggered.connect(self.exit_program)
        self.action_draw_line.triggered.connect(self.draw_line)
        self.action_select_item.triggered.connect(self.select_item_enable)
        # self.graphicsView.snap_point_mode = False

    def select_item_enable(self):
        self.graphicsView.select_items = not self.graphicsView.select_items

    def draw_line(self):
        self.statusBar().showMessage('Line Drawing Mode: On', 1000)
        self.graphicsView.draw_mode = 'Line'

    def exit_program(self):
        # Check if file is saved then close the program
        self.close()

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
        self.graphicsView.show_all()

    def test_dxf_handler(self, file_name):
        dxf_handler = DXFHandler(file_name)

        # print(len(list(dxf_handler.get_layers())))
        print('Getting Layers From File')
        for layer in dxf_handler.get_layers():
            self.graphicsView.create_layer(name=layer['name'], color=layer['color'])

        lines = dxf_handler.get_lines()
        print('Getting Lines From File')
        for line in lines:
            self.graphicsView.create_line_item(line.dxf.start, line.dxf.end, layer=line.dxf.layer)

        # print(self.graphicsView.layer_names)

        p_lines = dxf_handler.get_p_lines()
        print('Getting Polylines From File')
        for p_line in p_lines:
            # if p_line.dxf.layer == 'AIM_BDR_BAZALT_S':
            self.graphicsView.create_polyline_item(points=p_line.points(),
                                                   closed=p_line.is_closed,
                                                   layer=p_line.dxf.layer)

        for layer in self.graphicsView.layers:
            if layer.name != 'AIM_BDR_BAZALT_S':
                layer.set_status(not layer.status)
        print(len(self.graphicsView.scene().items()))

        # self.graphicsView.create_groups()
        # texts = dxf_handler.get_texts()
        # for text in texts:
        #     print(text.dxf.style)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet('QGraphicsView { border-style: none; }')
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
