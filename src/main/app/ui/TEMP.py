import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget,
                             QTableWidgetItem, QHeaderView)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(["A", "B", "C"])

        # Скрываем заголовок строки 2
        header = self.table.verticalHeader()
        header.setSectionHidden(2, True)

        # Устанавливаем текст для объединенной строки 1 и 2
        item = QTableWidgetItem("Объединенные строки")
        self.table.setItem(1, 0, item)

        # Заполняем остальные строки данными
        self.table.setItem(0, 0, QTableWidgetItem("Строка 1"))
        self.table.setItem(3, 0, QTableWidgetItem("Строка 3"))
        self.table.setItem(4, 0, QTableWidgetItem("Строка 4"))

        # ...  заполнение остальных столбцов

        self.setLayout(self.table)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())