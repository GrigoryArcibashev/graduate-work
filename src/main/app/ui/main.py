import sys
from typing import Union

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QFileDialog, QCheckBox

from main_ui import Ui_MainWindow
from src.main.app.model.db_service.result_of_file_analysis import ResultOfFileAnalysis, FileModStatus
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
        self.ui.btn_trust.clicked.connect(self._trust)
        self._set_text_to_label_site_dir(self._main_service.root_dir)

    def _trust(self) -> None:
        filenames = set()
        for row_ind in range(self.ui.table.rowCount()):
            check_box = self.ui.table.cellWidget(row_ind, 0)
            if isinstance(check_box, QCheckBox) and check_box.isChecked():
                filenames.add(self.ui.table.item(row_ind, 1).text())
        self._main_service.mark_files_as_trusted(
            results_of_file_analysis=self._main_service.get_results_from_db(),
            trusted_files=filenames
        )
        self._show_last_result()

    def _set_root_dir(self) -> None:
        root_dir = QFileDialog.getExistingDirectory(self, 'Выбрать директорию', '.')
        root_dir = root_dir if root_dir else ''
        self._set_text_to_label_site_dir(root_dir)
        if root_dir:
            self._main_service.root_dir = root_dir

    def _start_scan(self) -> None:
        self._main_service.run()
        self._show_last_result()

    def _show_last_result(self) -> None:
        results = self._main_service.get_results_from_db()
        statutes = {res.filename: res.status for res in results}
        items = list()
        for result in results:
            items.extend(self._make_items_for_result(result))
        row_count = len(items)
        self._prepare_table(row_count)
        self._fill_table(statutes, items, row_count)

    def _fill_table(
            self,
            statutes: dict[str, FileModStatus],
            items: list[list[Union[QTableWidgetItem, QCheckBox]]],
            row_count: int
    ) -> None:
        for row_ind in range(row_count):
            items_for_row = items[row_ind]
            for item_ind in range(len(items_for_row)):
                item = items_for_row[item_ind]
                if isinstance(item, QCheckBox):
                    self.ui.table.setCellWidget(row_ind, item_ind, item)
                    filename = items_for_row[1].text()
                    if statutes[filename] == FileModStatus.TRUSTED:
                        self.ui.table.cellWidget(row_ind, item_ind).setChecked(True)
                else:
                    self.ui.table.setItem(row_ind, item_ind, self._make_table_item_read_only(item))

    @staticmethod
    def _make_items_for_result(result: ResultOfFileAnalysis) -> list[list[Union[QTableWidgetItem, QCheckBox]]]:
        filename = QTableWidgetItem(result.filename)
        status = QTableWidgetItem(result.status.to_str())
        is_encr = QTableWidgetItem('есть' if result.an_result.encr_res.is_encr else 'нет')
        is_obf = QTableWidgetItem('есть' if result.an_result.obf_res.is_obf else 'нет')
        suspy_results = result.an_result.suspy_res

        items = [
            [
                QCheckBox(),

                filename,
                status,
                is_encr,
                is_obf,

                QTableWidgetItem(suspy_results[0].code_as_str if suspy_results else ''),
                QTableWidgetItem(suspy_results[0].danger_lvl.to_str() if suspy_results else ''),
                QTableWidgetItem(suspy_results[0].type.to_str() if suspy_results else '')
            ]
        ]

        for i in range(max(0, len(suspy_results) - 1)):
            new_item = [
                QTableWidgetItem(''),
                QTableWidgetItem(''),
                QTableWidgetItem(''),
                QTableWidgetItem(''),
                QTableWidgetItem(''),

                QTableWidgetItem(suspy_results[i + 1].code_as_str),
                QTableWidgetItem(suspy_results[i + 1].danger_lvl.to_str()),
                QTableWidgetItem(suspy_results[i + 1].type.to_str()),
            ]
            items.append(new_item)

        return items

    def _prepare_table(self, row_count: int) -> None:
        headers = (
            'Доверенный',
            'Имя',
            'Статус',
            'Преобразование',
            'Обфускация',
            'Подозрительный\nфрагмент',
            'Уровень опасности\nфрагмента',
            'Тип фрагмента',
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

    def _set_text_to_label_site_dir(self, text: str = None) -> None:
        result_text = 'Каталог сайта: ' + text if text is not None else ''
        self.ui.lbl_dir.setText(result_text)


def main():
    settings = Settings(FileReader.read_json('../../settings.json'))
    main_service = MainService(
        settings=settings,
        root_dir='.',
        path_to_db='sqlite:///../../database.db')

    app = QtWidgets.QApplication([])
    application = MainWindow(main_service)
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
