# Import built-in python packages
import sys

# Import downloaded python packages
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

# Import project files(soon)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface/start.ui', self)

        self.start_but.clicked.connect(self.control_panel)

    def start_page(self):
        uic.loadUi('interface/start.ui', self)
        self.start_but.clicked.connect(self.control_panel)

    def control_panel(self):
        uic.loadUi('interface/control_panel.ui', self)
        self.close_but.clicked.connect(self.start_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
