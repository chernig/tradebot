from main_window import Ui_Main
from login_popup import Ui_Login
from acc_info_popup import Ui_Account
from fxcm_controller import Fxcm
import sys
import pandas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtCore import QAbstractTableModel, Qt



class GUI():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_Main()
        self.ui.setupUi(self.main_window)
        self.ui.actionLogin.triggered.connect(self.open_login)
        self.ui.actionAccInfo.triggered.connect(self.open_acc_info)
        self.controller = Fxcm()
    def open_login(self):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Login()
        self.ui.setupUi(self.dialog)
        self.ui.label_2.setText(str(self.controller.connection_status))
        self.ui.lineEdit.setText(self.controller.token)
        self.ui.pushButton.clicked.connect(lambda: self.controller.update_token(self.ui.lineEdit.text()))
        self.dialog.show()
    def open_acc_info(self):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Account()
        self.ui.setupUi(self.dialog)
        self.data = self.controller.get_acc_info()
        self.ui.tableWidget.setRowCount(len(self.data.iloc[0]))
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setVerticalHeaderLabels(self.data.columns.values.tolist())
        self.ui.tableWidget.setHorizontalHeaderLabels(['values'])
        data = [str(x) for x in list(self.data.iloc[0])]
        for x in range(len(data)):
            self.ui.tableWidget.setItem(x, 0, QTableWidgetItem(data[x]))
        self.dialog.show()
    def launch(self):
        self.main_window.show()
        sys.exit(self.app.exec_())


# Launch
a = GUI()
a.launch()