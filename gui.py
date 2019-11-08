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
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, qApp, QAction, QMessageBox
from PyQt5.QtCore import QAbstractTableModel, Qt, QThread, QObject, pyqtSignal, pyqtSlot
import os
import pickle
import configuration
import multiprocessing
import queue
import threading
from auto_trading_page import Ui_autotrading_page
from auto_trading_add_strategy import Ui_autotrading_add_strategy_page
from auto_trading_edit_strategy import Ui_autotrading_edit_strategy_page
from auto_trading_backtest_strategy import Ui_Ui_autotrading_backtest_strategy_page
from strategy import strategy_controller
import time
"""
TO DO:
A lot of bugfixes
If you add a strategy with the same name - no check/ replace
If you delete 1 of 2 strategies - delete button become unailable so you can't delete another without re-opening window
Launch time increase dramatically based on number of strategies
Autotrading menu can popup randomly wihtout even clicking
Not sure about API part as well
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
        self.init_required_files()
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.closeEvent=self.closeEvent
        self.ui = Ui_Main()
        # Initial functionality
        self.controller = Fxcm()
        self.ui.setupUi(self.main_window)
        self.ui.actionLogin.triggered.connect(self.open_login)
        self.ui.actionAccInfo.triggered.connect(self.open_acc_info)
        self.ui.actionPositions.triggered.connect(self.view_open_positions)
        self.ui.actionOpenPosition.triggered.connect(self.open_position)
        self.ui.actionOpenOrder.triggered.connect(self.open_order)
        self.ui.actionView_Closed_Positions.triggered.connect(self.view_closed_positions)
        self.ui.actionViewOrders.triggered.connect(self.view_orders)
        self.ui.menuAutotrading.aboutToShow.connect(self.open_auto_trading_page) # Basically, just replace triggered with aboutToShow
        ### These lines are for testing purposes. If you want to test a new streaming - you can use these labels
        self.ui.actionConnect.triggered.connect(lambda: self.controller.enable_stream('Account'))
        self.ui.actionGet_Data.triggered.connect(lambda: print(self.controller.get_stream_data('Account')))
        self.ui.actionDisconnect.triggered.connect(lambda: self.controller.disable_stream('Account'))
        ###
        self.strategy_controller=strategy_controller.strategy_controller()
        self.strategies_name_description_dict=strategy_controller.trading_strategies_name_description_dict
        self.strategies_inputs_dict=strategy_controller.trading_strategies_inputs_dict
        self.risk_managements_name_description_dict=strategy_controller.risk_management_name_description_dict
        self.risk_managements_inputs_dict=strategy_controller.risk_management_inputs_dict
        self.news_reactors_name_description_dict=strategy_controller.news_reactor_name_description_dict
        self.news_reactors_inputs_dict=strategy_controller.news_reactor_inputs_dict
        self.auto_trading_symbol_list=configuration.auto_trading_symbol_list
        self.auto_trading_timeframe_list=configuration.auto_trading_timeframe_list
        self.db = Db_Controller()

        self.autotrading_strategy_status_stop_signal_queue=queue.Queue()
        self.autotrading_strategy_name_signal_queue=queue.Queue()
        self.autotrading_backtest_stop_signal_queue=queue.Queue()

    def open_warning(self):
        """
        Opens a popup window if connection is not established.
        Applied to every function that requires the connection to prevent unauthorized access
        """
        self.dialog = QMessageBox()
        self.dialog.setWindowTitle('Not connected to FXCM')
        self.dialog.setText('Please connect to FXCM server to proceed')
        self.dialog.setIcon(QMessageBox.Information)
        self.dialog.show()
    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self.main_window, 'Message', 
                        quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.strategy_controller.stop_all_strategies()
            event.accept()
        else:
            event.ignore()

    def open_login(self):
        """
        Method to generate login popup window. The UI template can be taken from login_popup.py
        """
        # Window initialization
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Login()
        self.ui.setupUi(self.dialog)
        def status_bar_update(): 
            self.ui.label_2.setText(str(self.controller.connection_status))
            QtWidgets.qApp.processEvents()
        def status_bar_connecting():
            self.ui.label_2.setText('Connecting')
            QtWidgets.qApp.processEvents()   
        # Window functionality
        self.ui.label_2.setText(str(self.controller.connection_status))
        self.ui.lineEdit.setText(self.controller.token)
        self.ui.pushButton_2.clicked.connect(status_bar_connecting)
        self.ui.pushButton_2.clicked.connect(self.controller.connect)
        self.ui.pushButton_2.clicked.connect(status_bar_update)
        self.ui.pushButton_3.clicked.connect(self.controller.disconnect)
        self.ui.pushButton_3.clicked.connect(status_bar_update)
        self.ui.pushButton.clicked.connect(lambda: self.controller.update_token(self.ui.lineEdit.text()))
        self.dialog.show()
    def open_acc_info(self):
        """
        Method to generate account info popup. The UI template can be taken from acc_info_popup.py
        """
        if self.controller.connection_status == False:
            self.open_warning()
        else:
            self.dialog = QtWidgets.QDialog()
            self.ui = Ui_Account()
            self.ui.setupUi(self.dialog)
            self.data = self.controller.get_acc_info()
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
            edit_info['amount'] = float(self.dialog.ui.lineEdit.text())

            #Update TableWidget at the same time
            self.ui.tableWidget.setItem(self.ui.tableWidget.currentRow(), 15, QTableWidgetItem(str(edit_info['amount'])))

            edit_info['order_id'] = int(self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text())
            if self.dialog.ui.lineEdit_2.isEnabled():
                edit_info['rate'] = float(self.dialog.ui.lineEdit_2.text())
            if self.dialog.ui.lineEdit_3.isEnabled():
                edit_info['range'] = float(self.dialog.ui.lineEdit_3.text())
            if self.dialog.ui.lineEdit_4.isEnabled():
                edit_info['trailing_step'] = float(self.dialog.ui.lineEdit_4.text())
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
        if self.controller.connection_status == False:
            self.open_warning()
        else:
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
            self.ui.pushButton_2.clicked.connect(lambda: self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow()))
            self.ui.pushButton_3.clicked.connect(self.edit_position_stop_limit)
            """
            # Work for online connection
            self.data = self.controller.get_open_positions()
            self.ui.tableWidget.setRowCount(len(self.data)) # Creating rows based on data
            self.ui.tableWidget.clicked.connect(position_info_review)
            
            # Populating the QTableWidget
            for row, position in enumerate(self.data):
                for column, data in enumerate(position):
                    # setItem function cannot accept not QTableWidgetItem objects. QTableWidgetItem accepts only strings
                    # Thus, to populate the table, convert all the data to string first, then QTableWidgetItem
                    self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(position[data])))
            """
            self.data = self.controller.db.get_table('OpenPosition')
            self.ui.tableWidget.setRowCount(len(self.data))
            self.ui.tableWidget.clicked.connect(position_info_review)
            for row, position in enumerate(self.data):
                for column, data in enumerate(position):
                    # setItem function cannot accept not QTableWidgetItem objects. QTableWidgetItem accepts only strings
                    # Thus, to populate the table, convert all the data to string first, then QTableWidgetItem
                    self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(data)))
            # Show the window
            self.dialog.show()
    def view_closed_positions(self):
        if self.controller.connection_status == False:
            self.open_warning()
        else:
            # Window initialization
            self.dialog = QtWidgets.QDialog()
            self.ui = Ui_ClosedPositions()
            self.ui.setupUi(self.dialog)
            pk = [''] # Holds a primary key for a db function
            def get_data():
                pk[0] = self.ui.tableWidget.item(self.ui.tableWidget.currentRow(), 2).text()
                #self.controller.db.delete_from_table('ClosedPosition', pk[0])
            # Window functionality
            self.data = self.controller.db.get_table('ClosedPosition')
            self.ui.tableWidget.setRowCount(len(self.data)) # Creating rows based on data
            # Populating the QTableWidget
            for row, position in enumerate(self.data):
                for column, data in enumerate(position):
                    # setItem function cannot accept not QTableWidgetItem objects. QTableWidgetItem accepts only strings
                    # Thus, to populate the table, convert all the data to string first, then QTableWidgetItem
                    self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(data)))
            self.ui.tableWidget.clicked.connect(get_data)
            self.ui.pushButton.clicked.connect(lambda: self.controller.db.delete_from_table('ClosedPosition', pk[0]))
            self.ui.pushButton.clicked.connect(lambda: self.ui.tableWidget.removeRow(self.ui.tableWidget.currentRow()))
            #self.ui.pushButton.triggered.connect(self.controller.db.)
            self.dialog.show()
    def open_position(self):
        if self.controller.connection_status == False:
            self.open_warning()
        else:
            # Window itnitialization

            trading_values = {
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
                trading_values['amount'] = float(self.ui.lineEdit.text())
                trading_values['symbol'] = str(self.ui.comboBox.currentText())
                if self.ui.lineEdit_2.isEnabled():
                    trading_values['stop'] = float(self.ui.lineEdit_2.text())
                if self.ui.lineEdit_3.isEnabled():
                    trading_values['trailing_step'] = float(self.ui.lineEdit_3.text())
                if self.ui.lineEdit_4.isEnabled():
                    trading_values['limit'] = float(self.ui.lineEdit_4.text())
                trading_values['is_in_pips'] = bool(self.ui.checkBox_4.isChecked)
                if self.ui.radioButton.isChecked():
                    trading_values['is_buy'] = True
            self.ui.checkBox.stateChanged.connect(lambda: change_status(self.ui.checkBox, self.ui.lineEdit_2))
            self.ui.checkBox_2.stateChanged.connect(lambda: change_status(self.ui.checkBox_2, self.ui.lineEdit_3))
            self.ui.checkBox_3.stateChanged.connect(lambda: change_status(self.ui.checkBox_3, self.ui.lineEdit_4))
            self.ui.buttonBox.accepted.connect(update_trading_values)
            self.ui.buttonBox.accepted.connect(lambda: self.controller.open_position(**trading_values))
            # self.ui.buttonBox.accepted.connect(lambda: self.db.insert_into_table('Open_Positions', add_position_maker(self.controller.get_open_positions()[-1])))
            self.dialog.show()
    def open_order(self):
        if self.controller.connection_status == False:
            self.open_warning()
        else:
            # Window initialization
            
            # Dictionary to hold order info for editing/closing purposes
            order_data = {
                "symbol": "EUR/USD",
                "amount": 1000,
                "is_buy": False,
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
                order_data['amount'] = float(self.ui.lineEdit.text())
                order_data['rate'] = float(self.ui.lineEdit_2.text())
                order_data['limit'] = float(self.ui.lineEdit_5.text())
                if self.ui.lineEdit_3.isEnabled():
                    order_data['stop'] = float(self.ui.lineEdit_3.text())
                if self.ui.lineEdit_4.isEnabled():
                    order_data['trailing_step'] = float(self.ui.lineEdit_4.text())
                order_data['is_in_pips'] = bool(self.ui.checkBox_3.isChecked)
                if self.ui.radioButton.isChecked():
                    order_data['is_buy'] = True
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
            self.ui.buttonBox.accepted.connect(lambda: print(self.controller.open_order(**order_data))) #Delete print
            #self.ui.buttonBox.accepted.connect(lambda: self.db.insert_into_table('Orders', add_position_maker(self.controller.get_orders()[-1])))
            #self.ui.buttonBox.accepted.connect(self.db.test_print)
            self.dialog.show()
    def view_orders(self):
        if self.controller.connection_status == False:
            self.open_warning()
        else:
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


    def open_auto_trading_page(self):
        """
        Method to open auto trading page. The UI template can be taken from auto_trading_page.py
        """

        
        self.dialog_autotrading = QtWidgets.QDialog()
        self.ui_autotrading = Ui_autotrading_page()
        self.ui_autotrading.setupUi(self.dialog_autotrading)
        self.ui_autotrading.selected_strategies_delete_strategy_button_2.setEnabled(False)
        self.ui_autotrading.selected_strategies_start_strategy_button_2.setEnabled(False)
        self.ui_autotrading.selected_strategies_stop_strategy_button_2.setEnabled(False)
        self.ui_autotrading.selected_strategies_edit_button_2.setEnabled(False)
        self.ui_autotrading.pushButton.setEnabled(False)
        try:
            self.autotrading_strategy_status_stop_signal_queue.get_nowait()
            self.autotrading_strategy_status_stop_signal_queue.task_done()
        except:
            pass
        try:
            self.autotrading_strategy_name_signal_queue.get_nowait()
            self.autotrading_strategy_name_signal_queue.task_done()
        except:
            pass
        print(threading.active_count())

        # Window initialization
        def closeEvent(event):
            try:
                print(123)
                print(threading.active_count())
                self.autotrading_strategy_status_stop_signal_queue.put(True)
                self.ui_autotrading.update_strategy_status_thread.terminate()
                self.ui_autotrading.update_strategy_status_thread.wait()
                del self.ui_autotrading.update_strategy_status_thread
                print(threading.active_count())

                event.accept()
                print(333)
            except Exception as e:
                print(e)
                event.accept()

        
        def switch_strategy_status():
            try:
                self.ui_autotrading.selected_strategies_delete_strategy_button_2.setEnabled(True)
                self.ui_autotrading.selected_strategies_start_strategy_button_2.setEnabled(True)
                self.ui_autotrading.selected_strategies_stop_strategy_button_2.setEnabled(True)
                self.ui_autotrading.selected_strategies_edit_button_2.setEnabled(True)
                self.ui_autotrading.pushButton.setEnabled(True)
                
                self.autotrading_strategy_name_signal_queue.put(self.ui_autotrading.selected_strategies_list.currentItem().text())
                print(1111)
            except Exception as e:
                print(e)
                self.ui_autotrading.selected_strategies_delete_strategy_button_2.setEnabled(False)
                self.ui_autotrading.selected_strategies_start_strategy_button_2.setEnabled(False)
                self.ui_autotrading.selected_strategies_stop_strategy_button_2.setEnabled(False)
                self.ui_autotrading.selected_strategies_edit_button_2.setEnabled(False)
                self.ui_autotrading.pushButton.setEnabled(False)

        def delete_trading_strategy():
            question_result=QtWidgets.QMessageBox.question(self.dialog_autotrading,'', "Are you sure to delete the strategy?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if question_result==QtWidgets.QMessageBox.Yes:
                self.strategy_controller.delete_strategy(self.ui_autotrading.selected_strategies_list.currentItem().text())
                self.ui_autotrading.selected_strategies_list.takeItem(self.ui_autotrading.selected_strategies_list.row(self.ui_autotrading.selected_strategies_list.selectedItems()[0]))
                self.ui_autotrading.selected_strategies_delete_strategy_button_2.setEnabled(False)

        def start_trading_strategy():
            self.strategy_controller.start_strategy(self.ui_autotrading.selected_strategies_list.currentItem().text())
        def stop_trading_strategy():
            self.strategy_controller.stop_strategy(self.ui_autotrading.selected_strategies_list.currentItem().text())

        def start_all_trading_strategy():
            self.strategy_controller.start_all_strategies()
        def stop_all_trading_strategy():
            self.strategy_controller.stop_all_strategies()

    
        
        def create_saved_strategies_content():
            for key, value in self.strategy_controller.strategy_setting_dict.items():
                self.ui_autotrading.selected_strategies_list.addItem(value['strategy_name'])
            self.ui_autotrading.selected_strategies_list.currentItemChanged.connect(switch_strategy_status)


        def update_strategy_status(status_tuple):
            self.ui_autotrading.label_10.setText(status_tuple[0])
            self.ui_autotrading.label_11.setText(status_tuple[1])
            self.ui_autotrading.label_12.setText(status_tuple[2])

        class update_strategy_status_thread_class(QThread):
            intReady = pyqtSignal(tuple)
            def __init__(self, strategy_controller_obj, stop_signal_queue, strategy_name_signal_queue):
                QThread.__init__(self)
                self.strategy_controller_obj=strategy_controller_obj
                self.stop_signal_queue=stop_signal_queue
                self.strategy_name_signal_queue=strategy_name_signal_queue

            def run(self):
                try:
                    self.strategy_name=''
                    print(self.strategy_name)
                    print(5555)
                    while True:
                        if self.stop_signal_queue.empty()==False:
                            try:
                                self.stop_signal_queue.get_nowait()
                                self.stop_signal_queue.task_done()
                            except Exception as e:
                                print(e)
                            
                            print(5555555)
                            break
                        else:
                            if self.strategy_name_signal_queue.empty()==False:
                                self.strategy_name=self.strategy_name_signal_queue.get_nowait()
                                self.strategy_name_signal_queue.task_done()
                            if self.strategy_name!='':
                                status_tuple=self.strategy_controller_obj.strategy_status_get(self.strategy_name)
                                self.intReady.emit(status_tuple)
                            time.sleep(1)
                except Exception as e:
                    print(e)



        create_saved_strategies_content()
        self.ui_autotrading.selected_strategies_add_strategy_button_2.clicked.connect(self.open_auto_trading_add_strategy_page)
        
        self.ui_autotrading.selected_strategies_delete_strategy_button_2.clicked.connect(delete_trading_strategy)
        self.ui_autotrading.selected_strategies_start_strategy_button_2.clicked.connect(start_trading_strategy)
        self.ui_autotrading.selected_strategies_stop_strategy_button_2.clicked.connect(stop_trading_strategy)
        self.ui_autotrading.selected_strategies_start_all_strategy_button_2.clicked.connect(start_all_trading_strategy)
        self.ui_autotrading.selected_strategies_stop_all_strategy_button_2.clicked.connect(stop_all_trading_strategy)
        self.ui_autotrading.selected_strategies_edit_button_2.clicked.connect(lambda: self.open_auto_trading_edit_strategy_page(self.ui_autotrading.selected_strategies_list.currentItem().text()))
        self.ui_autotrading.pushButton.clicked.connect(lambda: self.open_auto_trading_backtest_page(self.ui_autotrading.selected_strategies_list.currentItem().text()))
        self.dialog_autotrading.closeEvent=closeEvent

        self.ui_autotrading.update_strategy_status_thread=update_strategy_status_thread_class(self.strategy_controller, self.autotrading_strategy_status_stop_signal_queue, self.autotrading_strategy_name_signal_queue)
        self.ui_autotrading.update_strategy_status_thread.setTerminationEnabled(True)
        self.ui_autotrading.update_strategy_status_thread.intReady.connect(update_strategy_status)
        self.ui_autotrading.update_strategy_status_thread.start()
        print(threading.active_count())
        self.dialog_autotrading.show()



    def open_auto_trading_backtest_page(self, strategy_name):
        self.dialog_auto_trading_backtest = QtWidgets.QDialog()
        self.ui_auto_trading_backtest = Ui_Ui_autotrading_backtest_strategy_page()
        self.ui_auto_trading_backtest.setupUi(self.dialog_auto_trading_backtest)

        self.ui_auto_trading_backtest.horizontalLayout_backtest_result = QtWidgets.QHBoxLayout()
        self.ui_auto_trading_backtest.verticalLayout_backtest_result_labels = QtWidgets.QVBoxLayout()
        self.ui_auto_trading_backtest.verticalLayout_backtest_result_labels_result = QtWidgets.QVBoxLayout()
        self.ui_auto_trading_backtest.horizontalLayout_backtest_result.addLayout(self.ui_auto_trading_backtest.verticalLayout_backtest_result_labels)
        self.ui_auto_trading_backtest.horizontalLayout_backtest_result.addLayout(self.ui_auto_trading_backtest.verticalLayout_backtest_result_labels_result)
        self.ui_auto_trading_backtest.scrollAreaWidgetContents.setLayout(self.ui_auto_trading_backtest.horizontalLayout_backtest_result)
        self.ui_auto_trading_backtest.progressBar.setValue(0)
        self.ui_auto_trading_backtest.backtest_label_dict={}
        self.ui_auto_trading_backtest.backtest_label_result_dict={}
        try:
            self.autotrading_backtest_stop_signal_queue.get_nowait()
            self.autotrading_backtest_stop_signal_queue.task_done()
        except:
            pass



        def closeEvent(event):
            try:
                self.ui_auto_trading_backtest.progressBar.setValue(0)
                self.strategy_controller.backtest_stop(strategy_name)
                self.autotrading_backtest_stop_signal_queue.put(True)
                self.ui_auto_trading_backtest.backtesting_thread.terminate()
                self.ui_auto_trading_backtest.backtesting_thread.wait()
                self.ui_auto_trading_backtest.backtesting_start_thread.terminate()
                self.ui_auto_trading_backtest.backtesting_start_thread.wait()
                del self.ui_auto_trading_backtest.backtesting_thread
                del self.ui_auto_trading_backtest.backtesting_start_thread
                event.accept()
            except Exception as e:
                print(e)
                self.ui_auto_trading_backtest.progressBar.setValue(0)
                self.strategy_controller.backtest_stop(strategy_name)
                event.accept()
            


        def create_backtest_result_content(backtest_result):
            try:
                for key, value in self.ui_auto_trading_backtest.backtest_label_dict.items():
                    self.ui_auto_trading_backtest.verticalLayout_backtest_result_labels.removeWidget(value)
                    value.deleteLater()
                    value=None

                for key, value in self.ui_auto_trading_backtest.backtest_label_result_dict.items():
                    self.ui_auto_trading_backtest.verticalLayout_backtest_result_labels_result.removeWidget(value)
                    value.deleteLater()
                    value=None
                    
                self.ui_auto_trading_backtest.backtest_label_dict={}
                self.ui_auto_trading_backtest.backtest_label_result_dict={}
                for key, value in backtest_result.items():
                    self.ui_auto_trading_backtest.backtest_label_dict[key] = QtWidgets.QLabel()
                    self.ui_auto_trading_backtest.backtest_label_dict[key].setText(key)
                    self.ui_auto_trading_backtest.backtest_label_result_dict[key] = QtWidgets.QLabel()
                    self.ui_auto_trading_backtest.backtest_label_result_dict[key].setText(str(value))
                    self.ui_auto_trading_backtest.verticalLayout_backtest_result_labels.addWidget(self.ui_auto_trading_backtest.backtest_label_dict[key])
                    self.ui_auto_trading_backtest.verticalLayout_backtest_result_labels_result.addWidget(self.ui_auto_trading_backtest.backtest_label_result_dict[key])
                self.ui_auto_trading_backtest.progressBar.setValue(0)
            except Exception as e:
                print(e)

        def update_progress_bar(progress_percentage):
            self.ui_auto_trading_backtest.progressBar.setValue(progress_percentage)

        def strategy_backtest_clicked():
            try:
                qty=int(self.ui_auto_trading_backtest.lineEdit.text())
                cap=int(self.ui_auto_trading_backtest.lineEdit_2.text())
                self.ui_auto_trading_backtest.progressBar.setValue(0)
                self.ui_auto_trading_backtest.backtesting_start_thread=backtesting_start_thread(self.strategy_controller, strategy_name, qty, cap)
                self.ui_auto_trading_backtest.backtesting_start_thread.setTerminationEnabled(True)    
                self.ui_auto_trading_backtest.backtesting_start_thread.start()          
                self.ui_auto_trading_backtest.backtesting_thread=backtesting_thread(self.strategy_controller, self.autotrading_backtest_stop_signal_queue, strategy_name, qty, cap)
                self.ui_auto_trading_backtest.backtesting_thread.setTerminationEnabled(True)
                self.ui_auto_trading_backtest.backtesting_thread.intReady.connect(update_progress_bar)
                self.ui_auto_trading_backtest.backtesting_thread.finished.connect(create_backtest_result_content)
                self.ui_auto_trading_backtest.backtesting_thread.start()
            except:
                QtWidgets.QMessageBox.about(self.dialog_auto_trading_backtest, 'Result message', 'All fields must be filled')

        
        class backtesting_start_thread(QThread):
            finished = pyqtSignal(dict)
            intReady = pyqtSignal(int)
            def __init__(self, strategy_controller_obj, strategy_name, quantity, capital):
                QThread.__init__(self)
                self.strategy_controller_obj=strategy_controller_obj
                self.strategy_name=strategy_name
                self.quantity=quantity
                self.capital=capital

            def run(self):
                print(33333333)
                backtesting_result=self.strategy_controller_obj.backtest_strategy(self.strategy_name, self.quantity, self.capital)
                print(444444)



        class backtesting_thread(QThread):
            finished = pyqtSignal(dict)
            intReady = pyqtSignal(int)
            def __init__(self, strategy_controller_obj, stop_signal_queue, strategy_name, quantity, capital):
                QThread.__init__(self)
                self.strategy_controller_obj=strategy_controller_obj
                self.strategy_name=strategy_name
                self.quantity=quantity
                self.capital=capital
                self.stop_signal_queue=stop_signal_queue


            def run(self):
                print(444444)
                while True:
                    try:
                        if self.stop_signal_queue.empty()==False:
                            try:
                                print(333999987)
                                self.stop_signal_queue.get_nowait()
                                self.stop_signal_queue.task_done()
                                self.strategy_controller_obj.backtest_stop(strategy_name)
                                break
                            except Exception as e:
                                print(e)
                        elif self.strategy_controller_obj.get_backtest_result(strategy_name)!={}:
                            backtest_result=self.strategy_controller_obj.get_backtest_result(strategy_name)
                            progress_percentage=self.strategy_controller_obj.get_backtest_progress_rate(self.strategy_name)
                            self.intReady.emit(progress_percentage)
                            break

                        progress_percentage=self.strategy_controller_obj.get_backtest_progress_rate(self.strategy_name)
                        self.intReady.emit(progress_percentage)
                        time.sleep(1)
                    
                    except Exception as e:
                        print(e)
                        backtest_result={}
                self.finished.emit(backtest_result)

        def cancel_button_clicked():
            try:
                self.ui_auto_trading_backtest.progressBar.setValue(0)
                self.strategy_controller.backtest_stop(strategy_name)
                self.autotrading_backtest_stop_signal_queue.put(True)
                self.ui_auto_trading_backtest.backtesting_thread.terminate()
                self.ui_auto_trading_backtest.backtesting_thread.wait()
                self.ui_auto_trading_backtest.backtesting_start_thread.terminate()
                self.ui_auto_trading_backtest.backtesting_start_thread.wait()
                del self.ui_auto_trading_backtest.backtesting_thread
                del self.ui_auto_trading_backtest.backtesting_start_thread
                self.dialog_auto_trading_backtest.done(1)

            except Exception as e:
                print(e)
                self.ui_auto_trading_backtest.progressBar.setValue(0)
                self.strategy_controller.backtest_stop(strategy_name)
                self.dialog_auto_trading_backtest.done(1)
            

        self.dialog_auto_trading_backtest.closeEvent=closeEvent
        self.ui_auto_trading_backtest.pushButton.clicked.connect(strategy_backtest_clicked)
        self.ui_auto_trading_backtest.pushButton_2.clicked.connect(cancel_button_clicked)

        self.dialog_auto_trading_backtest.show()


    def open_auto_trading_edit_strategy_page(self, strategy_name):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_autotrading_edit_strategy_page()
        self.ui.setupUi(self.dialog)

        self.ui.horizontalLayout_risk_management_inputs = QtWidgets.QHBoxLayout()
        self.ui.verticalLayout_risk_management_inputs_labels = QtWidgets.QVBoxLayout()
        self.ui.verticalLayout_risk_management_inputs_lineEdit = QtWidgets.QVBoxLayout()
        self.ui.horizontalLayout_risk_management_inputs.addLayout(self.ui.verticalLayout_risk_management_inputs_labels)
        self.ui.horizontalLayout_risk_management_inputs.addLayout(self.ui.verticalLayout_risk_management_inputs_lineEdit)
        self.ui.scrollAreaWidgetContents_3.setLayout(self.ui.horizontalLayout_risk_management_inputs)

        self.ui.horizontalLayout_strategy_inputs = QtWidgets.QHBoxLayout()
        self.ui.verticalLayout_strategy_inputs_labels = QtWidgets.QVBoxLayout()
        self.ui.verticalLayout_strategy_inputs_lineEdit = QtWidgets.QVBoxLayout()
        self.ui.horizontalLayout_strategy_inputs.addLayout(self.ui.verticalLayout_strategy_inputs_labels)
        self.ui.horizontalLayout_strategy_inputs.addLayout(self.ui.verticalLayout_strategy_inputs_lineEdit)
        self.ui.scrollAreaWidgetContents_2.setLayout(self.ui.horizontalLayout_strategy_inputs)

        self.ui.horizontalLayout_news_reactor_inputs = QtWidgets.QHBoxLayout()
        self.ui.verticalLayout_news_reactor_inputs_labels = QtWidgets.QVBoxLayout()
        self.ui.verticalLayout_news_reactor_inputs_lineEdit = QtWidgets.QVBoxLayout()
        self.ui.horizontalLayout_news_reactor_inputs.addLayout(self.ui.verticalLayout_news_reactor_inputs_labels)
        self.ui.horizontalLayout_news_reactor_inputs.addLayout(self.ui.verticalLayout_news_reactor_inputs_lineEdit)
        self.ui.scrollAreaWidgetContents.setLayout(self.ui.horizontalLayout_news_reactor_inputs)


        required_option={'strategy':False, 'risk_management':False, 'news_reactor':False}

        strategy_system=self.strategy_controller.strategy_setting_dict[strategy_name]['trading_strategy_system']
        risk_management_system=self.strategy_controller.strategy_setting_dict[strategy_name]['risk_management_system']
        news_reactor_system=self.strategy_controller.strategy_setting_dict[strategy_name]['news_reactor_system']

        def create_risk_management_inputs():
            self.ui.risk_management_inputs_labels_obj_dict={}
            self.ui.risk_management_inputs_inputs_obj_dict={}
            for key, value in self.risk_managements_inputs_dict[risk_management_system].items():
                self.ui.risk_management_inputs_labels_obj_dict[value[0]] = QtWidgets.QLabel()
                self.ui.risk_management_inputs_labels_obj_dict[value[0]].setText(key)
                self.ui.risk_management_inputs_inputs_obj_dict[value[0]] = QtWidgets.QLineEdit()
                self.ui.risk_management_inputs_inputs_obj_dict[value[0]].setText(str(self.strategy_controller.strategy_setting_dict[strategy_name]['risk_management_system_inputs'][value[0]]))
                self.ui.verticalLayout_risk_management_inputs_labels.addWidget(self.ui.risk_management_inputs_labels_obj_dict[value[0]])
                self.ui.verticalLayout_risk_management_inputs_lineEdit.addWidget(self.ui.risk_management_inputs_inputs_obj_dict[value[0]])

        def create_trading_strategy_inputs():
            self.ui.strategy_inputs_labels_obj_dict={}
            self.ui.strategy_inputs_inputs_obj_dict={}
            for key, value in self.strategies_inputs_dict[strategy_system].items():
                self.ui.strategy_inputs_labels_obj_dict[value[0]] = QtWidgets.QLabel()
                self.ui.strategy_inputs_labels_obj_dict[value[0]].setText(key)
                self.ui.strategy_inputs_inputs_obj_dict[value[0]] = QtWidgets.QLineEdit()
                self.ui.strategy_inputs_inputs_obj_dict[value[0]].setText(str(self.strategy_controller.strategy_setting_dict[strategy_name]['trading_strategy_inputs'][value[0]]))
                self.ui.verticalLayout_strategy_inputs_labels.addWidget(self.ui.strategy_inputs_labels_obj_dict[value[0]])
                self.ui.verticalLayout_strategy_inputs_lineEdit.addWidget(self.ui.strategy_inputs_inputs_obj_dict[value[0]])

        def create_news_reactor_inputs():
            self.ui.news_reactor_inputs_labels_obj_dict={}
            self.ui.news_reactor_inputs_inputs_obj_dict={}
            for key, value in self.news_reactors_inputs_dict[news_reactor_system].items():
                self.ui.news_reactor_inputs_labels_obj_dict[value[0]] = QtWidgets.QLabel()
                self.ui.news_reactor_inputs_labels_obj_dict[value[0]].setText(key)
                self.ui.news_reactor_inputs_inputs_obj_dict[value[0]] = QtWidgets.QLineEdit()
                self.ui.news_reactor_inputs_inputs_obj_dict[value[0]].setText(str(self.strategy_controller.strategy_setting_dict[strategy_name]['news_reactor_inputs'][value[0]]))
                self.ui.verticalLayout_news_reactor_inputs_labels.addWidget(self.ui.news_reactor_inputs_labels_obj_dict[value[0]])
                self.ui.verticalLayout_news_reactor_inputs_lineEdit.addWidget(self.ui.news_reactor_inputs_inputs_obj_dict[value[0]])
        
        def edit_strategy_clicked():
            check_symbol=True
            check_timeframe=True
            check_risk_management_inputs=True
            risk_management_inputs_dict_args={}
            check_strategy_inputs=True
            strategy_inputs_dict_args={}
            check_news_reactor_inputs=True
            news_reactor_inputs_dict_args={}
            
            for key, value in self.ui.risk_management_inputs_inputs_obj_dict.items():
                try:
                    input_temp=float(value.text())
                    risk_management_inputs_dict_args[key]=input_temp
                except Exception as e:
                    check_risk_management_inputs=False
                    print(e)

            for key, value in self.ui.strategy_inputs_inputs_obj_dict.items():
                try:
                    input_temp=float(value.text())
                    strategy_inputs_dict_args[key]=input_temp
                except Exception as e:
                    check_strategy_inputs=False
                    print(e)

            if news_reactor_system!='None':
                for key, value in self.ui.news_reactor_inputs_inputs_obj_dict.items():
                    try:
                        input_temp=float(value.text())
                        news_reactor_inputs_dict_args[key]=input_temp
                    except Exception as e:
                        check_news_reactor_inputs=False
                        print(e)

            if check_risk_management_inputs==True and check_strategy_inputs==True and check_news_reactor_inputs==True and check_symbol==True and check_timeframe==True:
                strategy_arguments_dict={
                                        'timeframe':self.ui.comboBox.currentText(),
                                        'trading_strategy_system':strategy_system,
                                        'trading_strategy_inputs':strategy_inputs_dict_args,
                                        'risk_management_system':risk_management_system,
                                        'risk_management_system_inputs':risk_management_inputs_dict_args,
                                        'news_reactor_system':news_reactor_system,
                                        'news_reactor_inputs':news_reactor_inputs_dict_args
                                        }
                self.strategy_controller.edit_strategy(strategy_name, strategy_arguments_dict)
                QtWidgets.QMessageBox.about(self.dialog, 'Result message', 'Strategy is successfully edited')
                self.dialog.close()
            else:
                QtWidgets.QMessageBox.about(self.dialog, 'Result message', 'All fields must be filled')

        def cancel_button_clicked():
            self.dialog.destroy()

        create_risk_management_inputs()
        create_trading_strategy_inputs()
        if news_reactor_system!='None':
            create_news_reactor_inputs()
        self.ui.comboBox.addItems(self.auto_trading_timeframe_list)
        self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(self.strategy_controller.strategy_setting_dict[strategy_name]['timeframe']))
        self.ui.pushButton.clicked.connect(edit_strategy_clicked)
        self.ui.pushButton_2.clicked.connect(cancel_button_clicked)

        self.dialog.show()


    def open_auto_trading_add_strategy_page(self):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_autotrading_add_strategy_page()
        self.ui.setupUi(self.dialog)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.textEdit.setReadOnly(True)
        self.ui.textEdit_2.setReadOnly(True)
        self.ui.auto_trading_add_strategy_next_1_button.setEnabled(False)
        
        self.ui.horizontalLayout_risk_management_inputs = QtWidgets.QHBoxLayout()
        self.ui.verticalLayout_risk_management_inputs_labels = QtWidgets.QVBoxLayout()
        self.ui.verticalLayout_risk_management_inputs_lineEdit = QtWidgets.QVBoxLayout()
        self.ui.horizontalLayout_risk_management_inputs.addLayout(self.ui.verticalLayout_risk_management_inputs_labels)
        self.ui.horizontalLayout_risk_management_inputs.addLayout(self.ui.verticalLayout_risk_management_inputs_lineEdit)
        self.ui.scrollAreaWidgetContents_3.setLayout(self.ui.horizontalLayout_risk_management_inputs)

        self.ui.horizontalLayout_strategy_inputs = QtWidgets.QHBoxLayout()
        self.ui.verticalLayout_strategy_inputs_labels = QtWidgets.QVBoxLayout()
        self.ui.verticalLayout_strategy_inputs_lineEdit = QtWidgets.QVBoxLayout()
        self.ui.horizontalLayout_strategy_inputs.addLayout(self.ui.verticalLayout_strategy_inputs_labels)
        self.ui.horizontalLayout_strategy_inputs.addLayout(self.ui.verticalLayout_strategy_inputs_lineEdit)
        self.ui.scrollAreaWidgetContents_4.setLayout(self.ui.horizontalLayout_strategy_inputs)

        self.ui.horizontalLayout_news_reactor_inputs = QtWidgets.QHBoxLayout()
        self.ui.verticalLayout_news_reactor_inputs_labels = QtWidgets.QVBoxLayout()
        self.ui.verticalLayout_news_reactor_inputs_lineEdit = QtWidgets.QVBoxLayout()
        self.ui.horizontalLayout_news_reactor_inputs.addLayout(self.ui.verticalLayout_news_reactor_inputs_labels)
        self.ui.horizontalLayout_news_reactor_inputs.addLayout(self.ui.verticalLayout_news_reactor_inputs_lineEdit)
        self.ui.scrollAreaWidgetContents_6.setLayout(self.ui.horizontalLayout_news_reactor_inputs)

        

        required_option={'strategy':False, 'risk_management':False, 'news_reactor':False}


        def strategy_clicked():
            self.ui.textEdit.clear()
            self.ui.textEdit.textCursor().insertHtml(self.strategies_name_description_dict[self.ui.auto_trading_add_strategy_strategy_list.currentItem().text()])
            required_option['strategy']=True
            if required_option['risk_management']==True and required_option['news_reactor']==True:
                self.ui.auto_trading_add_strategy_next_1_button.setEnabled(True)
        def risk_management_clicked():
            self.ui.textEdit_2.clear()
            self.ui.textEdit_2.textCursor().insertHtml(self.risk_managements_name_description_dict[self.ui.auto_trading_add_strategy_risk_management_list.currentItem().text()])
            required_option['risk_management']=True
            if required_option['strategy']==True and required_option['news_reactor']==True:
                self.ui.auto_trading_add_strategy_next_1_button.setEnabled(True)
        def news_reactor_clicked():
            self.ui.textEdit_3.clear()
            self.ui.textEdit_3.textCursor().insertHtml(self.news_reactors_name_description_dict[self.ui.listWidget_3.currentItem().text()])
            required_option['news_reactor']=True
            if required_option['strategy']==True and required_option['risk_management']==True:
                self.ui.auto_trading_add_strategy_next_1_button.setEnabled(True)

        def create_risk_management_inputs():
            self.ui.risk_management_inputs_labels_obj_dict={}
            self.ui.risk_management_inputs_inputs_obj_dict={}
            for key, value in self.risk_managements_inputs_dict[self.ui.auto_trading_add_strategy_risk_management_list.currentItem().text()].items():
                self.ui.risk_management_inputs_labels_obj_dict[value[0]] = QtWidgets.QLabel()
                self.ui.risk_management_inputs_labels_obj_dict[value[0]].setText(key)
                self.ui.risk_management_inputs_inputs_obj_dict[value[0]] = QtWidgets.QLineEdit()
                self.ui.risk_management_inputs_inputs_obj_dict[value[0]].setText(str(value[1]))
                self.ui.verticalLayout_risk_management_inputs_labels.addWidget(self.ui.risk_management_inputs_labels_obj_dict[value[0]])
                self.ui.verticalLayout_risk_management_inputs_lineEdit.addWidget(self.ui.risk_management_inputs_inputs_obj_dict[value[0]])


        def create_trading_strategy_inputs():
            self.ui.strategy_inputs_labels_obj_dict={}
            self.ui.strategy_inputs_inputs_obj_dict={}
            for key, value in self.strategies_inputs_dict[self.ui.auto_trading_add_strategy_strategy_list.currentItem().text()].items():
                self.ui.strategy_inputs_labels_obj_dict[value[0]] = QtWidgets.QLabel()
                self.ui.strategy_inputs_labels_obj_dict[value[0]].setText(key)
                self.ui.strategy_inputs_inputs_obj_dict[value[0]] = QtWidgets.QLineEdit()
                self.ui.strategy_inputs_inputs_obj_dict[value[0]].setText(str(value[1]))
                self.ui.verticalLayout_strategy_inputs_labels.addWidget(self.ui.strategy_inputs_labels_obj_dict[value[0]])
                self.ui.verticalLayout_strategy_inputs_lineEdit.addWidget(self.ui.strategy_inputs_inputs_obj_dict[value[0]])

        def create_news_reactor_inputs():
            self.ui.news_reactor_inputs_labels_obj_dict={}
            self.ui.news_reactor_inputs_inputs_obj_dict={}
            for key, value in self.news_reactors_inputs_dict[self.ui.listWidget_3.currentItem().text()].items():
                self.ui.news_reactor_inputs_labels_obj_dict[value[0]] = QtWidgets.QLabel()
                self.ui.news_reactor_inputs_labels_obj_dict[value[0]].setText(key)
                self.ui.news_reactor_inputs_inputs_obj_dict[value[0]] = QtWidgets.QLineEdit()
                self.ui.news_reactor_inputs_inputs_obj_dict[value[0]].setText(str(value[1]))
                self.ui.verticalLayout_news_reactor_inputs_labels.addWidget(self.ui.news_reactor_inputs_labels_obj_dict[value[0]])
                self.ui.verticalLayout_news_reactor_inputs_lineEdit.addWidget(self.ui.news_reactor_inputs_inputs_obj_dict[value[0]])
        

        def go_second_page():
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.label_5.setText(self.ui.auto_trading_add_strategy_strategy_list.currentItem().text())
            self.ui.label_11.setText(self.ui.auto_trading_add_strategy_risk_management_list.currentItem().text())
            self.ui.label_14.setText(self.ui.listWidget_3.currentItem().text())
            create_risk_management_inputs()
            create_trading_strategy_inputs()
            if self.ui.listWidget_3.currentItem().text()!='None':
                create_news_reactor_inputs()

        def go_first_page():
            self.ui.stackedWidget.setCurrentIndex(0)

        def add_strategy_clicked():
            check_strategy_name=False
            check_symbol=True
            check_timeframe=True
            check_risk_management_inputs=True
            risk_management_inputs_dict_args={}
            check_strategy_inputs=True
            strategy_inputs_dict_args={}
            check_news_reactor_inputs=True
            news_reactor_inputs_dict_args={}

            if self.ui.lineEdit.text()!='':
                check_strategy_name=True
            
            for key, value in self.ui.risk_management_inputs_inputs_obj_dict.items():
                try:
                    input_temp=float(value.text())
                    risk_management_inputs_dict_args[key]=input_temp
                except Exception as e:
                    check_risk_management_inputs=False
                    print(e)

            for key, value in self.ui.strategy_inputs_inputs_obj_dict.items():
                try:
                    input_temp=float(value.text())
                    strategy_inputs_dict_args[key]=input_temp
                except Exception as e:
                    check_strategy_inputs=False
                    print(e)

            if self.ui.listWidget_3.currentItem().text()!='None':
                for key, value in self.ui.news_reactor_inputs_inputs_obj_dict.items():
                    try:
                        input_temp=float(value.text())
                        news_reactor_inputs_dict_args[key]=input_temp
                    except Exception as e:
                        check_news_reactor_inputs=False
                        print(e)

            if check_risk_management_inputs==True and check_strategy_inputs==True and check_news_reactor_inputs==True and check_strategy_name==True and check_symbol==True and check_timeframe==True:
                strategy_arguments_dict={
                                        'strategy_name':self.ui.lineEdit.text(),
                                        'symbol':self.ui.comboBox_3.currentText(),
                                        'timeframe':self.ui.comboBox.currentText(),
                                        'trading_strategy_system':self.ui.auto_trading_add_strategy_strategy_list.currentItem().text(),
                                        'trading_strategy_inputs':strategy_inputs_dict_args,
                                        'risk_management_system':self.ui.auto_trading_add_strategy_risk_management_list.currentItem().text(),
                                        'risk_management_system_inputs':risk_management_inputs_dict_args,
                                        'news_reactor_system':self.ui.listWidget_3.currentItem().text(),
                                        'news_reactor_inputs':news_reactor_inputs_dict_args
                                        }
                self.strategy_controller.add_strategy(**strategy_arguments_dict)
                QtWidgets.QMessageBox.about(self.dialog, 'Result message', 'Strategy is successfully added')
                self.dialog.close()
                self.open_auto_trading_page()
            else:
                QtWidgets.QMessageBox.about(self.dialog, 'Result message', 'All fields must be filled')

        def cancel_button_clicked():
            self.dialog.destroy()

        for key, value in self.strategies_name_description_dict.items():
            self.ui.auto_trading_add_strategy_strategy_list.addItem(key)

        for key, value in self.risk_managements_name_description_dict.items():
            self.ui.auto_trading_add_strategy_risk_management_list.addItem(key)

        for key, value in self.news_reactors_name_description_dict.items():
            self.ui.listWidget_3.addItem(key)

        self.ui.comboBox_3.addItems(self.auto_trading_symbol_list)
        self.ui.comboBox.addItems(self.auto_trading_timeframe_list)


        

        self.ui.auto_trading_add_strategy_strategy_list.currentItemChanged.connect(strategy_clicked)
        self.ui.auto_trading_add_strategy_risk_management_list.currentItemChanged.connect(risk_management_clicked)
        self.ui.listWidget_3.currentItemChanged.connect(news_reactor_clicked)
        self.ui.auto_trading_add_strategy_next_1_button.clicked.connect(go_second_page)
        self.ui.pushButton.clicked.connect(add_strategy_clicked)
        self.ui.auto_trading_add_strategy_cancel_1_button.clicked.connect(cancel_button_clicked)
        self.ui.pushButton_2.clicked.connect(cancel_button_clicked)
        self.ui.pushButton_3.clicked.connect(go_first_page)

        

        self.dialog.show()

    def launch(self):
        global time
        self.main_window.show()
        time2 = datetime.datetime.now()
        print(time2-time)
        sys.exit(self.app.exec_())

    def init_required_files(self):
        db=Db_Controller()
        if os.path.isdir('./data'):
            pass
        else:
            os.mkdir('./data')
        if os.path.isfile('./data/data.dll')==False:
            db.create_schema()
        if os.path.isfile('./data/strategies_settings.cfg')==False:
            strategy_setting_dict={}
            with open('./data/strategies_settings.cfg', 'wb') as f: 
                pickle.dump(strategy_setting_dict, f)


# Launch

if __name__=="__main__":
    global time
    time = datetime.datetime.now()
    multiprocessing.freeze_support()
    a = GUI()
    a.launch()