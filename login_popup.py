# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_popup.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Login)
        self.buttonBox.setGeometry(QtCore.QRect(30, 230, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Login)
        self.label.setGeometry(QtCore.QRect(40, 40, 101, 16))
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Login)
        self.label_2.setGeometry(QtCore.QRect(156, 40, 71, 20))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Login)
        self.pushButton.setGeometry(QtCore.QRect(30, 230, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(Login)
        self.label_3.setGeometry(QtCore.QRect(40, 70, 51, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Login)
        self.lineEdit.setGeometry(QtCore.QRect(120, 70, 271, 20))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Login)
        self.buttonBox.accepted.connect(Login.accept)
        self.buttonBox.rejected.connect(Login.reject)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Dialog"))
        self.label.setText(_translate("Login", "Connection status"))
        self.pushButton.setText(_translate("Login", "Update token"))
        self.label_3.setText(_translate("Login", "API Token"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login = QtWidgets.QDialog()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())
