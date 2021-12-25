import sys

from PyQt5.QtWidgets import QApplication

from package.main_window import MainWindow


if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    window = MainWindow()
    window.resize(int(1920 / 2), int(1200 / 2))
    window.show()

    app.exec_()
