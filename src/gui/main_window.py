from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar

from src.gui.graphicsview import GraphicsView


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.graphicsView = GraphicsView(self.widget)
        self.verticalLayout.addWidget(self.graphicsView)
        self.setCentralWidget(self.widget)
        self.setStatusBar(QStatusBar())
