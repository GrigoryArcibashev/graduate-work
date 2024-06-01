import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

from main_ui import Ui_MainWindow
from src.main.app.model.db_service.result_of_file_analysis import ResultOfFileAnalysis
from src.main.app.model.file_service.file_reader import FileReader
from src.main.app.model.main.mainservice import MainService
from src.main.app.model.settings.settings import Settings


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, main_service: MainService):
        super().__init__()
        self._main_service = main_service
        self._setup_ui()

    def _setup_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_show_res.clicked.connect(self._show_last_result)
        self.ui.btn_start_scan.clicked.connect(self._start_scan)
        self.ui.btn_root_dir.clicked.connect(self._set_root_dir)

    def _start_scan(self) -> None:
        self._main_service.run()
        self._show_last_result()

    def _show_last_result(self) -> None:
        results = self._main_service.get_results_from_db()
        items = list()
        for result in results:
            items.extend(self._make_items_for_result(result))
        row_count = len(items)
        self._prepare_table(row_count)
        for row_ind in range(row_count):
            items_for_row = items[row_ind]
            for item_ind in range(len(items_for_row)):
                self.ui.table.setItem(row_ind, item_ind, self._make_table_item_read_only(items_for_row[item_ind]))

        print('OK')

    def _set_root_dir(self, root_dir: str) -> None:
        self._main_service.root_dir = '../../source/encr/base122'  # root_dir
        print('OK')

    @staticmethod
    def _make_items_for_result(result: ResultOfFileAnalysis) -> list[list[QTableWidgetItem]]:
        filename = QTableWidgetItem(result.filename)
        status = QTableWidgetItem(str(result.status))
        is_encr = QTableWidgetItem('есть' if result.an_result.encr_res.is_encr else 'нет')
        is_obf = QTableWidgetItem('есть' if result.an_result.obf_res.is_obf else 'нет')
        suspy_results = result.an_result.suspy_res
        items = [[filename, status, is_encr, is_obf]] \
                + [[QTableWidgetItem('')] * 4] * max(0, len(suspy_results) - 1)
        for suspy_ind in range(len(suspy_results)):
            suspy = suspy_results[suspy_ind]
            items[suspy_ind].extend(
                [
                    QTableWidgetItem(suspy.code_as_str),
                    QTableWidgetItem(str(suspy.danger_lvl)),
                    QTableWidgetItem(str(suspy.type))]
            )
        return items

    def _prepare_table(self, row_count: int) -> None:
        headers = (
            'Имя',
            'Статус',
            'Преобразование',
            'Обфускация',
            'Подозрительный\nфрагмент',
            'Уровень опасности\nфрагмента',
            'Тип фрагмента'
        )
        column_count = len(headers)
        self.ui.table.setRowCount(row_count)
        self.ui.table.setColumnCount(column_count)
        self.ui.table.setHorizontalHeaderLabels(headers)
        header = self.ui.table.horizontalHeader()
        for col_ind in range(column_count):
            header.setSectionResizeMode(col_ind, QHeaderView.ResizeMode.ResizeToContents)
            self.ui.table.horizontalHeaderItem(col_ind).setTextAlignment(Qt.AlignLeft)

    @staticmethod
    def _make_table_item_read_only(table_item: QTableWidgetItem) -> QTableWidgetItem:
        table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        return table_item


def main():
    settings = Settings(FileReader.read_json('../../settings.json'))
    main_service = MainService(
        settings=settings,
        root_dir='../../source/encr/base85',
        path_to_db='sqlite:///../../database.db')

    app = QtWidgets.QApplication([])
    application = MainWindow(main_service)
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
