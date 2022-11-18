import sys
from PyQt6.QtWidgets import QApplication
from color_displayer import ColorDisplayer
from color_updater import ColorUpdater
from threading import Thread


class Application(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)
        self.widget = ColorDisplayer()

        self.widget.set_background_color('#c02e63')
        self.widget.show()


def show_application():
    app = Application(sys.argv)

    app.exec()


if __name__ == '__main__':
    show_application()
