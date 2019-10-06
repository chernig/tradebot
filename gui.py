from main_window import Ui_Main
from login_popup import Ui_Login
from acc_info_popup import Ui_Account
from fxcm_controller import Fxcm
import sys
import pandas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
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
        self.ui.tableView.setModel(Pandas_Model(self.controller.get_acc_info()))
        self.dialog.show()
    def launch(self):
        self.main_window.show()
        sys.exit(self.app.exec_())


class Pandas_Model(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


# Launch
a = GUI()
a.launch()