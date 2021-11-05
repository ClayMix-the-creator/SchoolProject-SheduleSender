# Import built-in python packages
import sys
import os

# Import downloaded python packages
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

# Import project files(soon)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface/start.ui', self)

        self.start_but.clicked.connect(self.control_panel)
        self.start_but.clicked.connect(self.bot_change_status)

        self.bot_status = False

    def start_page(self):
        uic.loadUi('interface/start.ui', self)
        self.start_but.clicked.connect(self.control_panel)
        self.start_but.clicked.connect(self.bot_change_status)

    def control_panel(self):
        uic.loadUi('interface/control_panel.ui', self)
        self.close_but.clicked.connect(self.start_page)
        self.close_but.clicked.connect(self.bot_change_status)

    def bot_change_status(self):
        var_text = self.sender().text()

        if var_text == 'Начать работу':
            self.bot_status = True
            os.startfile(f'{os.getcwd()}/data/vk_bot.py')

        elif var_text == 'Выключить':
            self.bot_status = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
