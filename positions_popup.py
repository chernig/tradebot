# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'positions_popup.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Positions(object):
    def setupUi(self, Positions):
        Positions.setObjectName("Positions")
        Positions.resize(566, 355)
        self.buttonBox = QtWidgets.QDialogButtonBox(Positions)
        self.buttonBox.setGeometry(QtCore.QRect(200, 310, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableWidget = QtWidgets.QTableWidget(Positions)
        self.tableWidget.setGeometry(QtCore.QRect(0, 30, 181, 271))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(Positions)
        self.label.setGeometry(QtCore.QRect(30, 10, 131, 16))
        self.label.setObjectName("label")
        self.tableWidget_2 = QtWidgets.QTableWidget(Positions)
        self.tableWidget_2.setGeometry(QtCore.QRect(200, 30, 191, 271))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.label_2 = QtWidgets.QLabel(Positions)
        self.label_2.setGeometry(QtCore.QRect(210, 10, 131, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Positions)
        self.buttonBox.accepted.connect(Positions.accept)
        self.buttonBox.rejected.connect(Positions.reject)
        QtCore.QMetaObject.connectSlotsByName(Positions)

    def retranslateUi(self, Positions):
        _translate = QtCore.QCoreApplication.translate
        Positions.setWindowTitle(_translate("Positions", "Dialog"))
        self.label.setText(_translate("Positions", "Open positions summary"))
        self.label_2.setText(_translate("Positions", "Closed positions summary"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Positions = QtWidgets.QDialog()
    ui = Ui_Positions()
    ui.setupUi(Positions)
    Positions.show()
    sys.exit(app.exec_())
