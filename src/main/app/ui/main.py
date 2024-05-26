from PyQt5 import QtWidgets
from main_ui import Ui_MainWindow
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(app.exec())
