from main_window import Ui_Main
from login_popup import Ui_Login
from acc_info_popup import Ui_Account
from view_open_positions import Ui_Positions
from view_closed_positions import Ui_ClosedPositions
from open_position import Ui_OpenPos
from open_order import Ui_OpenOrd
from edit_popup import Ui_EditPosition
from fxcm_controller import Fxcm
import sys
import datetime
import pandas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtCore import QAbstractTableModel, Qt
"""
TO DO:
Edit done but for position lol, need for order
Add orders
DB
"""


class GUI():
    """
    GUI class functions represent a specific window
    """
    def __init__(self):
        # Create main window object
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_Main()

        # Initial functionality
        self.ui.setupUi(self.main_window)
        self.ui.actionLogin.triggered.connect(self.open_login)
        self.ui.actionAccInfo.triggered.connect(self.open_acc_info)
        self.ui.actionPositions.triggered.connect(self.view_open_positions)
        self.ui.actionOpenPosition.triggered.connect(self.open_position)
        self.ui.actionOpenOrder.triggered.connect(self.open_order)
        self.ui.actionView_Closed_Positions.triggered.connect(self.view_closed_positions)
        self.controller = Fxcm()
        self.id = str(self.controller.get_default_acc_id())
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
    def edit_order(self):
        """
        Second popup window to be used from view_open_position for edit position purposes
        """
        edit_info = {
            "order_id": 235045369,
            "amount": 1
        }
        self.dialog.dialog = QtWidgets.QDialog()
        self.dialog.ui = Ui_EditPosition()
        self.dialog.ui.setupUi(self.dialog.dialog)
        # Window functionality
        def change_status(checkbox, line_edit):
            """
            Small checkbox controller (toggle on/of corresponing line based on status)
            input: checkbox object, corresponding line_edit
            output: toggle on/off line edit
            """
            if checkbox.isChecked():
                line_edit.setEnabled(1)
            else:
                line_edit.setDisabled(1)
        #edit_info['order_id'] = self.ui.tableWidget.
        self.dialog.ui.buttonBox.accepted.connect(lambda: print(edit_info))
        self.dialog.ui.checkBox.stateChanged.connect(lambda: change_status(self.dialog.ui.checkBox, self.dialog.ui.lineEdit_2))
        self.dialog.ui.checkBox_2.stateChanged.connect(lambda: change_status(self.dialog.ui.checkBox_2, self.dialog.ui.lineEdit_3))
        self.dialog.ui.checkBox_3.stateChanged.connect(lambda: change_status(self.dialog.ui.checkBox_3, self.dialog.ui.lineEdit_4))
        self.dialog.dialog.show()
    def view_open_positions(self):
        # Initial table to store the requred for closing position
        position_data = {
            'trade_id': '',
            'amount': ''
        }
        # Window initialization
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Positions()
        self.ui.setupUi(self.dialog)

        # Window functionality
        def position_info_review():
            """
            Small 'capture' controller. Sends the required data from selected row to the position_data
            """
            # 2 and 15 are corresponding to 'trade_id' and 'amount' columns in QTableWidget
            position_data['trade_id'] = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text()
            position_data['amount'] = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 15).text()
        self.ui.pushButton.clicked.connect(self.controller.close_all_positions)
        self.ui.pushButton.clicked.connect(lambda: self.ui.tableWidget.setRowCount(0))
        self.ui.pushButton_2.clicked.connect(lambda: self.controller.close_position(**position_data))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow()))
        self.data = self.controller.get_open_positions()
        self.ui.tableWidget.setRowCount(len(self.data)) # Creating rows based on data
        self.ui.tableWidget.clicked.connect(position_info_review)
        
        # Populating the QTableWidget
        for row, position in enumerate(self.data):
            for column, data in enumerate(position):
                # setItem function cannot accept not QTableWidgetItem objects. QTableWidgetItem accepts only strings
                # Thus, to populate the table, convert all the data to string first, then QTableWidgetItem
                self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(position[data])))
        
        # Show the window
        self.dialog.show()
    def view_closed_positions(self):
        # Window initialization
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_ClosedPositions()
        self.ui.setupUi(self.dialog)

        # Window functionality
        self.data = self.controller.get_closed_positions()
        self.ui.tableWidget.setRowCount(len(self.data)) # Creating rows based on data
        print(self.data)
        # Populating the QTableWidget
        for row, position in enumerate(self.data):
            for column, data in enumerate(position):
                # setItem function cannot accept not QTableWidgetItem objects. QTableWidgetItem accepts only strings
                # Thus, to populate the table, convert all the data to string first, then QTableWidgetItem
                self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(position[data])))
        self.dialog.show()
    def open_position(self):
        
        # Window itnitialization

        trading_values = {
            "account_id": self.id,
            "symbol": "EUR/USD",
            "is_buy": False,
            "amount": 1,
            "order_type": "AtMarket",
            "time_in_force": "GTC",
            "is_in_pips": ''
            }
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_OpenPos()
        self.ui.setupUi(self.dialog)

        # Window functionality

        def change_status(checkbox, line_edit):
            """
            Small checkbox controller (toggle on/of corresponing line based on status)
            input: checkbox object, corresponding line_edit
            output: toggle on/off line edit
            """
            if checkbox.isChecked():
                line_edit.setEnabled(1)
            else:
                line_edit.setDisabled(1)
        def update_trading_values():
            """
            Function to update trading values for future operations
            """
            trading_values['amount'] = int(self.ui.lineEdit.text())
            trading_values['symbol'] = str(self.ui.comboBox.currentText())
            if self.ui.lineEdit_2.isEnabled():
                trading_values['stop'] = int(self.ui.lineEdit_2.text())
            if self.ui.lineEdit_3.isEnabled():
                trading_values['trailing_step'] = int(self.ui.lineEdit_3.text())
            if self.ui.lineEdit_4.isEnabled():
                trading_values['limit'] = int(self.ui.lineEdit_4.text())
            trading_values['is_in_pips'] = bool(self.ui.checkBox_4.isChecked)
        self.ui.checkBox.stateChanged.connect(lambda: change_status(self.ui.checkBox, self.ui.lineEdit_2))
        self.ui.checkBox_2.stateChanged.connect(lambda: change_status(self.ui.checkBox_2, self.ui.lineEdit_3))
        self.ui.checkBox_3.stateChanged.connect(lambda: change_status(self.ui.checkBox_3, self.ui.lineEdit_4))
        self.ui.buttonBox.accepted.connect(update_trading_values)
        self.ui.buttonBox.accepted.connect(lambda: self.controller.open_position(**trading_values))
        self.dialog.show()
    def open_order(self):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_OpenOrd()
        self.ui.setupUi(self.dialog)
        def change_status(checkbox, line_edit):
            """
            Small checkbox controller (toggle on/of corresponing line based on status)
            input: checkbox object, corresponding line_edit
            output: toggle on/off line edit
            """
            if checkbox.isChecked():
                line_edit.setEnabled(1)
            else:
                line_edit.setDisabled(1)
        self.ui.checkBox.stateChanged.connect(lambda: change_status(self.ui.checkBox, self.ui.lineEdit_3))
        self.ui.checkBox_2.stateChanged.connect(lambda: change_status(self.ui.checkBox_2, self.ui.lineEdit_4))
        self.ui.checkBox_3.stateChanged.connect(lambda: change_status(self.ui.checkBox_3, self.ui.lineEdit_5))
        self.dialog.show()
    def launch(self):
        self.main_window.show()
        sys.exit(self.app.exec_())


# Launch
a = GUI()
a.launch()