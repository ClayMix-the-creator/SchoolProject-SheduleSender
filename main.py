# |-------------------------NON-WORKING VERSION-------------------------|

# Import built-in python packages
import sys

# Import downloaded python packages
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

# Import project files


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('some_ui', self)

    def some_def(self):
        pass


if __name__ == '__main__':
    pass
    # app = QApplication(sys.argv)
    # ex = MyWidget()
    # ex.show()
    # sys.exit(app.exec_())
