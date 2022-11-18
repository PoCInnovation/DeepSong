from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import pyqtSlot
from color_updater import ColorUpdater


class ColorDisplayer(QWidget):
    def __init__(self):
        super().__init__()

        self.updater = ColorUpdater(self)

        self.start_button = QPushButton('Colorize')
        self.start_button.clicked.connect(self.start_updating)

        self.close_button = QPushButton('Close app')
        self.close_button.clicked.connect(self.close)

        self.text = QLabel('Background color reacting to music')
        self.text.setStyleSheet('color: white')

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.close_button)

        self.resize(250, 250)
        self.setWindowTitle('Sound analysis app')

    def set_background_color(self, color):
        self.setStyleSheet('background-color: %s' % color)

    def start_updating(self):
        self.updater.start()

    @pyqtSlot()
    def close(self):
        exit(0)
