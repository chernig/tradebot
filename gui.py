"""
Import main class from all related UI files here
"""
from main_window import Ui_Main
from login_popup import Ui_Login
from acc_info_popup import Ui_Account
from view_open_positions import Ui_Positions
from view_closed_positions import Ui_ClosedPositions
from edit_order_stop_limit import Ui_OrderStopLimit
from open_position import Ui_OpenPos
from open_order import Ui_OpenOrd
from edit_popup import Ui_EditPosition
from edit_position_stop_limit import Ui_EditTradeStopLimit
from view_orders import Ui_Orders
from fxcm_controller import Fxcm
from db_controller import Db_Controller
import sys
import datetime
import pandas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtCore import QAbstractTableModel, Qt
"""
TO DO:
Add db changes for edit
bugfixes (datatypes, default variables)
complete rest of db based on auto trade
"""


class GUI():
    """
    GUI class represents the actual GUI and its functionality
    Functions represent specific windows and popups
    """
    def __init__(self):
        """
        Main window generation method. The UI template can be taken from main_window.py
        """
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
        self.ui.actionViewOrders.triggered.connect(self.view_orders)
        self.controller = Fxcm()
        self.id = str(self.controller.get_default_acc_id())
        self.db = Db_Controller()
    def open_login(self):
        """
        Method to generate login popup window. The UI template can be taken from login_popup.py
        """

        # Window initialization
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Login()
        self.ui.setupUi(self.dialog)

        # Window functionality
        self.ui.label_2.setText(str(self.controller.connection_status))
        self.ui.lineEdit.setText(self.controller.token)
        self.ui.pushButton.clicked.connect(lambda: self.controller.update_token(self.ui.lineEdit.text()))
        self.dialog.show()
    def open_acc_info(self):
        """
        Method to generate account info popup. The UI template can be taken from acc_info_popup.py
        """
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Account()
        self.ui.setupUi(self.dialog)
        self.data = self.controller.get_acc_info()
        print(len(self.data[0]))
        """
        self.ui.tableWidget.setRowCount(len(self.data.iloc[0]))
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setVerticalHeaderLabels(self.data.columns.values.tolist())
        self.ui.tableWidget.setHorizontalHeaderLabels(['values'])
        data = [str(x) for x in list(self.data.iloc[0])]
        for x in range(len(data)):
            self.ui.tableWidget.setItem(x, 0, QTableWidgetItem(data[x]))
        """
        self.ui.tableWidget.setRowCount(len(self.data)) # Creating rows based on data
        # Populating the QTableWidget
        for row, position in enumerate(self.data):
            for column, data in enumerate(position):
                # setItem function cannot accept not QTableWidgetItem objects. QTableWidgetItem accepts only strings
                # Thus, to populate the table, convert all the data to string first, then QTableWidgetItem
                self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(position[data])))
        self.dialog.show()
    def edit_order(self):
        """
        Second popup window to be used from view_open_position for edit position purposes
        """
        # Window initialization
        edit_info = {
            "order_id": 235045369, # random deaful value, not essential
            "amount": 1,
            "rate" : 1,
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
        def update_edit_info():
            """
            A method to capture the required data from UI and update edit_info
            """

            #Update the edit_data dictionary
            edit_info['amount'] = int(self.dialog.ui.lineEdit.text())

            #Update TableWidget at the same time
            self.ui.tableWidget.setItem(self.ui.tableWidget.currentRow(), 15, QTableWidgetItem(str(edit_info['amount'])))

            edit_info['order_id'] = int(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text())
            if self.dialog.ui.lineEdit_2.isEnabled():
                edit_info['rate'] = int(self.dialog.ui.lineEdit_2.text())
            if self.dialog.ui.lineEdit_3.isEnabled():
                edit_info['range'] = int(self.dialog.ui.lineEdit_3.text())
            if self.dialog.ui.lineEdit_4.isEnabled():
                edit_info['trailing_step'] = int(self.dialog.ui.lineEdit_4.text())
        self.dialog.ui.buttonBox.accepted.connect(update_edit_info)
        self.dialog.ui.buttonBox.accepted.connect(lambda: self.controller.edit_order(**edit_info))
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
        def add_position_maker(data):
            """
            Function to add a position maker and transform data 
            to be suitable for database input
            Input: Dictionary with data
            Output: List of dictionary's values + position maker value
            """
            data = list(data.values())
            data.append('maker?')
            return data
        self.ui.pushButton.clicked.connect(self.controller.close_all_positions)
        self.ui.pushButton.clicked.connect(lambda: self.ui.tableWidget.setRowCount(0))
        self.ui.pushButton_2.clicked.connect(lambda: self.controller.close_position(**position_data))
        self.ui.pushButton_2.clicked.connect(lambda: self.db.delete_from_table('Open_Positions', position_data['trade_id']))
        self.ui.pushButton_2.clicked.connect(lambda: self.db.insert_into_table('Closed_Positions', add_position_maker(self.controller.get_closed_positions()[-1])))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow()))
        self.ui.pushButton_3.clicked.connect(self.edit_position_stop_limit)
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
        def add_position_maker(data):
            """
            Function to add a position maker and transform data 
            to be suitable for database input
            Input: Dictionary with data
            Output: List of dictionary's values + position maker value
            """
            data = list(data.values())
            data.append('maker?')
            return data
        self.ui.checkBox.stateChanged.connect(lambda: change_status(self.ui.checkBox, self.ui.lineEdit_2))
        self.ui.checkBox_2.stateChanged.connect(lambda: change_status(self.ui.checkBox_2, self.ui.lineEdit_3))
        self.ui.checkBox_3.stateChanged.connect(lambda: change_status(self.ui.checkBox_3, self.ui.lineEdit_4))
        self.ui.buttonBox.accepted.connect(update_trading_values)
        self.ui.buttonBox.accepted.connect(lambda: self.controller.open_position(**trading_values))
        self.ui.buttonBox.accepted.connect(lambda: self.db.insert_into_table('Open_Positions', add_position_maker(self.controller.get_open_positions()[-1])))
        self.dialog.show()
    def open_order(self):
        
        # Window initialization
        
        # Dictionary to hold order info for editing/closing purposes
        order_data = {
            "account_id": self.id,
            "symbol": "EUR/USD",
            "amount": 1000,
            "is_buy": True,
            "order_type": "Entry",
            "time_in_force": "GTC"
        }
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
        def update_order_data():
            """
            Function to transfer any changes in UI to the order_data dictionary
            """
            order_data['amount'] = int(self.ui.lineEdit.text())
            order_data['rate'] = int(self.ui.lineEdit_2.text())
            order_data['limit'] = int(self.ui.lineEdit_5.text())
            if self.ui.lineEdit_3.isEnabled():
                order_data['stop'] = int(self.ui.lineEdit_3.text())
            if self.ui.lineEdit_4.isEnabled():
                order_data['trailing_step'] = int(self.ui.lineEdit_4.text())
            order_data['is_in_pips'] = bool(self.ui.checkBox_3.isChecked)
        def add_position_maker(data):
            """
            Function to add a position maker and transform data 
            to be suitable for database input
            Input: Dictionary with data
            Output: List of dictionary's values + position maker value
            """
            data = list(data.values())
            data.append('maker?')
            return data
        self.ui.checkBox.stateChanged.connect(lambda: change_status(self.ui.checkBox, self.ui.lineEdit_3))
        self.ui.checkBox_2.stateChanged.connect(lambda: change_status(self.ui.checkBox_2, self.ui.lineEdit_4))
        self.ui.buttonBox.accepted.connect(update_order_data)
        self.ui.buttonBox.accepted.connect(lambda: self.controller.open_order(**order_data)) 
        self.ui.buttonBox.accepted.connect(lambda: self.db.insert_into_table('Orders', add_position_maker(self.controller.get_orders()[-1])))
        self.ui.buttonBox.accepted.connect(self.db.test_print)
        self.dialog.show()
    def view_orders(self):
        # Window initialization
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Orders()
        self.ui.setupUi(self.dialog)
        order_id = [0]
        # Window functionality
        self.data = self.controller.get_orders()
        self.ui.tableWidget.setRowCount(len(self.data))
        print(self.data)
        for row, position in enumerate(self.data):
            for column, data in enumerate(position):
                # setItem function cannot accept not QTableWidgetItem objects. QTableWidgetItem accepts only strings
                # Thus, to populate the table, convert all the data to string first, then QTableWidgetItem
                self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(position[data])))
        def update_id():
            """
            Small ID catcher from the selected row
            """
            order_id[0] = int(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text())
            print(order_id)
        self.ui.tableWidget.clicked.connect(update_id)
        self.ui.pushButton.clicked.connect(lambda: self.controller.close_order(order_id[0]))
        self.ui.pushButton.clicked.connect(lambda: self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow()))
        self.ui.pushButton_2.clicked.connect(self.edit_order)
        self.ui.pushButton_3.clicked.connect(self.edit_order_stop_limit)
        self.dialog.show()
    def edit_order_stop_limit(self):
        edit_order = {
            "order_id": 72513348,
            }
        # Window initialization
        self.dialog.dialog = QtWidgets.QDialog()
        self.dialog.ui = Ui_OrderStopLimit()
        self.dialog.ui.setupUi(self.dialog.dialog)

        # Window functionality
        def update_edit_order():
            """
            A method to capture the required data from UI and update edit_info
            """

            #Update the edit_data dictionary
            #Update TableWidget at the same time
            #self.ui.tableWidget.setItem(self.ui.tableWidget.currentRow(), 15, QTableWidgetItem(str(edit_order['amount'])))
            if self.dialog.ui.lineEdit.text():
                edit_order['limit']=float(self.dialog.ui.lineEdit.text())
            if self.dialog.ui.lineEdit_2.text():
                edit_order['stop']=float(self.dialog.ui.lineEdit.text())
            if self.dialog.ui.checkBox.isChecked():
                edit_order['is_limit_in_pips']=True
            else:
                edit_order['is_limit_in_pips']=False
            if self.dialog.ui.checkBox_2.isChecked():
                edit_order['is_stop_in_pips']=True
            else:
                edit_order['is_stop_in_pips']=False
            edit_order['order_id'] = int(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text())
        self.dialog.ui.buttonBox.accepted.connect(update_edit_order)
        self.dialog.ui.buttonBox.accepted.connect(lambda: self.controller.edit_order_stop_limit(**edit_order))
        self.dialog.dialog.show()
    def edit_position_stop_limit(self):
        edit_position = {
            'trade_id': 0
        }
        self.dialog.dialog = QtWidgets.QDialog()
        self.dialog.ui = Ui_EditTradeStopLimit()
        self.dialog.ui.setupUi(self.dialog.dialog)

        # Window functionality
        def update_edit_position():
            edit_position['trade_id'] = int(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text())
            if str(self.dialog.ui.comboBox.currentText()) == "Stop":
                edit_position['is_stop'] = True
            else:
                edit_position['is_stop'] = False
            if self.dialog.ui.lineEdit.text():
                edit_position['rate'] = float(self.dialog.ui.lineEdit.text())
            if self.dialog.ui.lineEdit_2.text():
                edit_position['trailing_step'] = float(self.dialog.ui.lineEdit_2.text())
            if self.dialog.ui.checkBox.isChecked():
                edit_position['is_in_pips'] = True
            else:
                edit_position['is_in_pips'] = False


        self.dialog.ui.buttonBox.accepted.connect(update_edit_position)
        self.dialog.ui.buttonBox.accepted.connect(lambda: self.controller.edit_position_stop_limit(**edit_position))
        self.dialog.dialog.show()

    def launch(self):
        self.main_window.show()
        sys.exit(self.app.exec_())


# Launch
a = GUI()
a.launch()