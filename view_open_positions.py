# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view_open_positions.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Positions(object):
    def setupUi(self, Positions):
        Positions.setObjectName("Positions")
        Positions.resize(520, 348)
        self.gridLayout = QtWidgets.QGridLayout(Positions)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(Positions)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(22)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(21, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 6)
        self.pushButton = QtWidgets.QPushButton(Positions)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 3, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Positions)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 5, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(Positions)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Positions)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 2, 1, 1)

        self.retranslateUi(Positions)
        self.buttonBox.accepted.connect(Positions.accept)
        self.buttonBox.rejected.connect(Positions.reject)
        QtCore.QMetaObject.connectSlotsByName(Positions)

    def retranslateUi(self, Positions):
        _translate = QtCore.QCoreApplication.translate
        Positions.setWindowTitle(_translate("Positions", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Positions", "T"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Positions", "Rate Precision"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Positions", "Trade ID"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Positions", "Account Name"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Positions", "Account ID"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Positions", "Roll"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Positions", "Com"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Positions", "Open"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Positions", "Value Date"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Positions", "Gross PL"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("Positions", "Close"))
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText(_translate("Positions", "Visible PL"))
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText(_translate("Positions", "Is Disabled"))
        item = self.tableWidget.horizontalHeaderItem(13)
        item.setText(_translate("Positions", "Currency"))
        item = self.tableWidget.horizontalHeaderItem(14)
        item.setText(_translate("Positions", "Is Buy"))
        item = self.tableWidget.horizontalHeaderItem(15)
        item.setText(_translate("Positions", "Amount K"))
        item = self.tableWidget.horizontalHeaderItem(16)
        item.setText(_translate("Positions", "Currency Point"))
        item = self.tableWidget.horizontalHeaderItem(17)
        item.setText(_translate("Positions", "Time"))
        item = self.tableWidget.horizontalHeaderItem(18)
        item.setText(_translate("Positions", "Used Margin"))
        item = self.tableWidget.horizontalHeaderItem(19)
        item.setText(_translate("Positions", "Stop"))
        item = self.tableWidget.horizontalHeaderItem(20)
        item.setText(_translate("Positions", "Stop Move"))
        item = self.tableWidget.horizontalHeaderItem(21)
        item.setText(_translate("Positions", "Limit"))
        self.pushButton.setText(_translate("Positions", "Close All"))
        self.pushButton_3.setText(_translate("Positions", "Edit Stop/Limit"))
        self.pushButton_2.setText(_translate("Positions", "Close Position"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Positions = QtWidgets.QDialog()
    ui = Ui_Positions()
    ui.setupUi(Positions)
    Positions.show()
    sys.exit(app.exec_())
