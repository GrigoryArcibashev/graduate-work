import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.uic.properties import QtGui

# from main_ui import Ui_MainWindow
from src.main.app.model.file_service.file_reader import FileReader
from src.main.app.model.main.mainservice import MainService
from src.main.app.model.settings.settings import Settings


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, main_service: MainService):
        super().__init__()
        self._main_service = main_service
        # self._setup_ui()
        self.show()

    # def _setup_ui(self):
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)

        # self.ui.show_last_res.triggered.connect(self._show_last_result)
        # self.ui.menu.addAction(self.ui.show_last_res)
        # self.ui.menubar.addAction(self.ui.menu.menuAction())

    def _show_last_result(self):
        # results = self._main_service.get_results_from_db()
        # row_count = sum([max(1, len(res.an_result.suspy_res)) for res in results])
        # self.ui.show_last_res.setRowCount(row_count)
        all_data = [[1, 2, 3, 4], [5, 6, 7, 8]]
        tbl = QtGui.QTableWidget(len(all_data), 4)
        header_labels = ['Column 1', 'Column 2', 'Column 3', 'Column 4']
        tbl.setHorizontalHeaderLabels(header_labels)
        for row in all_data:
            inx = all_data.index(row)
            tbl.insertRow(inx)
            tbl.setItem(inx, 0, QTableWidgetItem(str(row[0])))
            tbl.setItem(inx, 0, QTableWidgetItem(str(row[0])))
            tbl.setItem(inx, 0, QTableWidgetItem(str(row[0])))
        print('OK')


def main():
    settings = Settings(FileReader.read_json('../../settings.json'))
    main_service = MainService(
        settings=settings,
        root_dir='../../source/encr_non',
        path_to_db='sqlite:///../../database.db')

    app = QtWidgets.QApplication([])
    application = MainWindow(main_service)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
