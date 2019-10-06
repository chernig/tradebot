# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acc_info_popup.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Account(object):
    def setupUi(self, Account):
        Account.setObjectName("Account")
        Account.resize(636, 353)
        self.buttonBox = QtWidgets.QDialogButtonBox(Account)
        self.buttonBox.setGeometry(QtCore.QRect(300, 310, 331, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableView = QtWidgets.QTableView(Account)
        self.tableView.setGeometry(QtCore.QRect(70, 60, 256, 192))
        self.tableView.setObjectName("tableView")

        self.retranslateUi(Account)
        self.buttonBox.accepted.connect(Account.accept)
        self.buttonBox.rejected.connect(Account.reject)
        QtCore.QMetaObject.connectSlotsByName(Account)

    def retranslateUi(self, Account):
        _translate = QtCore.QCoreApplication.translate
        Account.setWindowTitle(_translate("Account", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Account = QtWidgets.QDialog()
    ui = Ui_Account()
    ui.setupUi(Account)
    Account.show()
    sys.exit(app.exec_())
