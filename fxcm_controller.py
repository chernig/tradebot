from fxcmpy import *
from db_controller import Db_Controller




class Fxcm():
    """
    Primary GUI controller for FXCM API
    All the methods are direct implementation of FXCM API
    Full documentation can be retrived from: https://fxcm.github.io/rest-api-docs/#section/Overview
    """
    def __init__(self):
        self.token = 'a46718dbcf04edf1b8135816d96d38a7703f2d65' # Default, for now
        self.connection = None
        self.data = None
        self.connection_status = 'Connecting'
        self.db = None
    
    def connect(self):
        self.connection = fxcmpy(access_token=self.token, log_level='error', server='demo')
        self.connection_status = self.connection.is_connected()
        self.db = Db_Controller()
    def disconnect(self):
        self.connection = None
        self.connection_status = False
    def get_acc_info(self):
        return self.connection.get_accounts(kind = 'list')
    def update_token(self, new_token):
        self.token = new_token
    def get_open_positions(self):
        return self.connection.get_open_positions(kind='list')
    def get_open_trade_ids(self):
        return self.connection.get_open_trade_ids()
    def get_closed_positions(self):
        return self.connection.get_closed_positions(kind='list')
    def open_position(self, **position_parameters):
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
        self.connection.open_trade(**position_parameters)
        self.data = self.get_open_positions()[-1]
        trade_id = self.data['tradeId']
        self.db.insert_into_table('Open_Positions', add_position_maker(self.data))
        self.data = None
        print(trade_id)
        return trade_id
    def close_position(self, **position_parameters):
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
        self.connection.close_trade(**position_parameters)
        self.db.delete_from_table('Open_Positions', position_parameters['trade_id'])
        self.db.insert_into_table('Closed_Positions', add_position_maker(self.get_closed_positions()[-1]))
    def edit_order(self, **order_parameters):
        self.connection.change_order(**order_parameters)
    def edit_order_stop_limit(self, **order_parameters):
        self.connection.change_order_stop_limit(**order_parameters)
    def edit_position_stop_limit(self, **position_parameters):
        self.connection.change_trade_stop_limit(**position_parameters)
    def close_all_positions(self):
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
        self.data = self.get_open_positions()
        for position in self.data:
            self.db.delete_from_table('Open_Positions', position['tradeId'])
        self.connection.close_all()
        self.data = self.get_closed_positions()[-len(self.data):]
        for position in self.data:
            self.db.insert_into_table('Closed_Positions', add_position_maker(position))
    def open_order(self, **order_parameters):
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
        self.connection.create_entry_order(**order_parameters)
        self.data = self.get_orders()[-1]
        order_id = self.data['orderId']
        self.db.insert_into_table('Orders', add_position_maker(self.data))
        self.data = None
        return order_id
    def get_orders(self):
        return self.connection.get_orders(kind='list')
    def close_order(self, order_id):
        self.db.delete_from_table('Orders', order_id)
        self.connection.delete_order(order_id)
    def get_open_positions_ids(self):
        return self.connection.get_open_trade_ids()
    def get_default_acc_id(self):
        return self.connection.get_default_account()

        
if __name__ == "__main__":
    import pandas
    check = Fxcm()
    check.connect()
    data = check.get_acc_info()
    print(list(data.iloc[0]))