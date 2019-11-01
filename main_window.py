# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(1124, 724)
        self.centralwidget = QtWidgets.QWidget(Main)
        self.centralwidget.setObjectName("centralwidget")
        Main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1124, 21))
        self.menubar.setObjectName("menubar")
        self.menuTrading = QtWidgets.QMenu(self.menubar)
        self.menuTrading.setObjectName("menuTrading")
        self.menuAutotrading = QtWidgets.QMenu(self.menubar)
        self.menuAutotrading.setObjectName("menuAutotrading")
        self.menuTest_Streaming = QtWidgets.QMenu(self.menubar)
        self.menuTest_Streaming.setObjectName("menuTest_Streaming")
        Main.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Main)
        self.statusbar.setObjectName("statusbar")
        Main.setStatusBar(self.statusbar)
        self.actionLogin = QtWidgets.QAction(Main)
        self.actionLogin.setCheckable(False)
        self.actionLogin.setObjectName("actionLogin")
        self.actionAccInfo = QtWidgets.QAction(Main)
        self.actionAccInfo.setObjectName("actionAccInfo")
        self.actionPositions = QtWidgets.QAction(Main)
        self.actionPositions.setObjectName("actionPositions")
        self.actionOpenPosition = QtWidgets.QAction(Main)
        self.actionOpenPosition.setObjectName("actionOpenPosition")
        self.actionOpenOrder = QtWidgets.QAction(Main)
        self.actionOpenOrder.setObjectName("actionOpenOrder")
        self.actionViewOrders = QtWidgets.QAction(Main)
        self.actionViewOrders.setObjectName("actionViewOrders")
        self.actionView_Closed_Positions = QtWidgets.QAction(Main)
        self.actionView_Closed_Positions.setObjectName("actionView_Closed_Positions")
        self.actionConnect = QtWidgets.QAction(Main)
        self.actionConnect.setObjectName("actionConnect")
        self.actionGet_Data = QtWidgets.QAction(Main)
        self.actionGet_Data.setObjectName("actionGet_Data")
        self.actionDisconnect = QtWidgets.QAction(Main)
        self.actionDisconnect.setObjectName("actionDisconnect")
        self.menuTrading.addSeparator()
        self.menuTrading.addAction(self.actionLogin)
        self.menuTrading.addAction(self.actionAccInfo)
        self.menuTrading.addAction(self.actionPositions)
        self.menuTrading.addAction(self.actionView_Closed_Positions)
        self.menuTrading.addAction(self.actionOpenPosition)
        self.menuTrading.addAction(self.actionOpenOrder)
        self.menuTrading.addAction(self.actionViewOrders)
        self.menuTest_Streaming.addAction(self.actionConnect)
        self.menuTest_Streaming.addAction(self.actionGet_Data)
        self.menuTest_Streaming.addAction(self.actionDisconnect)
        self.menubar.addAction(self.menuTrading.menuAction())
        self.menubar.addAction(self.menuAutotrading.menuAction())
        self.menubar.addAction(self.menuTest_Streaming.menuAction())

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "MainWindow"))
        self.menuTrading.setTitle(_translate("Main", "Trading"))
        self.menuAutotrading.setTitle(_translate("Main", "Autotrading"))
        self.menuTest_Streaming.setTitle(_translate("Main", "Test Streaming"))
        self.actionLogin.setText(_translate("Main", "Login"))
        self.actionAccInfo.setText(_translate("Main", "Acc Info"))
        self.actionPositions.setText(_translate("Main", "View Open Positions"))
        self.actionOpenPosition.setText(_translate("Main", "Open Position"))
        self.actionOpenOrder.setText(_translate("Main", "Open Order"))
        self.actionViewOrders.setText(_translate("Main", "View Orders"))
        self.actionView_Closed_Positions.setText(_translate("Main", "View Closed Positions"))
        self.actionConnect.setText(_translate("Main", "Connect"))
        self.actionGet_Data.setText(_translate("Main", "Get Data"))
        self.actionDisconnect.setText(_translate("Main", "Disconnect"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Main = QtWidgets.QMainWindow()
    ui = Ui_Main()
    ui.setupUi(Main)
    Main.show()
    sys.exit(app.exec_())
