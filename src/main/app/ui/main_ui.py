# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1553, 810)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(0, 0, 1551, 681))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.table.setFont(font)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.btn_show_res = QtWidgets.QPushButton(self.centralwidget)
        self.btn_show_res.setGeometry(QtCore.QRect(510, 710, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_show_res.setFont(font)
        self.btn_show_res.setObjectName("btn_show_res")
        self.btn_start_scan = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start_scan.setGeometry(QtCore.QRect(610, 710, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_start_scan.setFont(font)
        self.btn_start_scan.setObjectName("btn_start_scan")
        self.btn_root_dir = QtWidgets.QPushButton(self.centralwidget)
        self.btn_root_dir.setGeometry(QtCore.QRect(730, 710, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_root_dir.setFont(font)
        self.btn_root_dir.setObjectName("btn_root_dir")
        self.btn_trust = QtWidgets.QPushButton(self.centralwidget)
        self.btn_trust.setGeometry(QtCore.QRect(850, 710, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_trust.setFont(font)
        self.btn_trust.setObjectName("btn_trust")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1553, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_show_res.setText(_translate("MainWindow", "Показать"))
        self.btn_start_scan.setText(_translate("MainWindow", "Сканировать"))
        self.btn_root_dir.setText(_translate("MainWindow", "ROOT"))
        self.btn_trust.setText(_translate("MainWindow", "Сохранить отметки"))
