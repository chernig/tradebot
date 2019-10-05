from main_window import Ui_MainWindow
from login_window import Ui_Dialog
from fxcm_controller import Fxcm
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication



class GUI():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.ui.actionLogin.triggered.connect(self.click_some)
        self.ui.actionLogout.triggered.connect(self.open_login)
        self.controller = Fxcm()
    def click_some(self):
        print('TADAM')
    def open_login(self):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.dialog)
        self.ui.label_2.setText(str(self.controller.connection_status))
        self.dialog.show()
    def launch(self):
        self.main_window.show()
        sys.exit(self.app.exec_())


# Launch
a = GUI()
a.launch()