from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStatusBar, QAction, QMenuBar, QMenu

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

        self.menubar = QMenuBar(self)
        self.file_menu = QMenu(self.menubar)
        self.draw_menu = QMenu(self.menubar)
        self.select_menu = QMenu(self.menubar)
        self.setMenuBar(self.menubar)

        self.action_close = QAction(self)
        self.action_draw_line = QAction(self)
        self.action_select_item = QAction(self)

        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.draw_menu.menuAction())
        self.menubar.addAction(self.select_menu.menuAction())
        self.file_menu.addAction(self.action_close)
        self.draw_menu.addAction(self.action_draw_line)
        self.select_menu.addAction(self.action_select_item)

        self.file_menu.setTitle('Dosya')
        self.action_close.setText('Kapat')
        self.action_close.setShortcut('Ctrl+Q')

        self.draw_menu.setTitle('Çizim')
        self.action_draw_line.setText('Doğru Çiz')
        self.action_draw_line.setShortcut('Ctrl+L')

        self.select_menu.setTitle('Seçim')
        self.action_select_item.setText('Obje Seç')
        self.action_select_item.setShortcut('Shift+S')
