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
        self.connection_status = False
        self.db = None
    
    def connect(self):
        self.connection = fxcmpy(access_token=self.token, log_level='error', server='demo')
        self.connection_status = self.connection.is_connected()
        self.db = Db_Controller()
        self.enable_stream('OpenPosition') # Enables streaming once connected
        
    def disconnect(self):
        self.disable_stream('OpenPosition')
        self.connection = None
        self.connection_status = False

    def get_price_data(self, trading_symbol, timeframe, quantity=10000):
        try:
            symbol=list(trading_symbol)
            symbol.insert(3, '/')
            symbol=''.join(symbol)
            data=self.connection.get_candles(symbol, period=timeframe, number=quantity)
            self.db.insert_into_price_data_table(data, trading_symbol, timeframe)
        except Exception as e:
            print(e, 777777777777)
    def enable_stream(self, model):
        """
        Enables a specific model stream according to the FXCM documentation

        Inputs: model->str Name of the model from FXCM model list (OpenPosition, ClosedPosition, Account, Order)
        Output: Enables streaming data and updates corresponding db rows
        """
        def process_data(data):
            # Work for open
            if len(data) == 5:
                columns = [x for x in data.keys()][:-1]
                values = [x for x in data.values()][:-1]
                pk_key = list(data.values())[-1]
                self.db.update_from_stream(model, columns, values, pk_key)
                #self.db.print_table('OpenPosition') #Enable to track real-time progress in console
        self.connection.subscribe_data_model(model, (process_data,))
    def enable_test_stream(self, model):
        def print_data(data):
            print(data)
        self.connection.subscribe_data_model(model, (print_data,))
    def disable_stream(self, model):
        self.connection.unsubscribe_data_model(model)
    def get_stream_data(self, model):
        return self.connection.get_model([model])
    
    def get_acc_info(self):
        try:
            return self.connection.get_accounts(kind = 'list')
        except:
            return []
    def update_token(self, new_token):
        self.token = new_token
    def get_open_positions(self):
        try:
            return self.connection.get_open_positions(kind='list')
        except:
            return []
    def get_open_trade_ids(self):
        return self.connection.get_open_trade_ids()
    def get_closed_positions(self):
        try:
            return self.connection.get_closed_positions(kind='list')
        except:
            return []
    def open_position(self, **position_parameters):
        """
        Function to add a position to FXCM server
        
        Inputs: **position_parameters->dictionary List of different variables to open a position
        Output: Opened position and created db row
        """
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
        self.db.insert_into_table('OpenPosition', add_position_maker(self.data))
        self.data = None
        return trade_id
    def close_position(self, **position_parameters):
        """
        Function to close a position from FXCM server
        
        Inputs: **position_parameters->dictionary List of different variables to close a position
        Output: Closed FXCM position, deleted OpenPosition row and created ClosedPosition row in db
        """
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
        self.db.delete_from_table('OpenPosition', position_parameters['trade_id'])
        self.db.insert_into_table('ClosedPosition', add_position_maker(self.get_closed_positions()[-1]))
    def edit_order(self, **order_parameters):
        try:
            self.connection.change_order(**order_parameters)
        except:
            pass
    def edit_order_stop_limit(self, **order_parameters):
        try:
            self.connection.change_order_stop_limit(**order_parameters)
        except:
            pass
    def edit_position_stop_limit(self, **position_parameters):
        try:
            self.connection.change_trade_stop_limit(**position_parameters)
        except:
            pass
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
            self.db.delete_from_table('OpenPosition', position['tradeId'])
        self.connection.close_all()
        self.data = self.get_closed_positions()[-len(self.data):]
        for position in self.data:
            self.db.insert_into_table('ClosedPosition', add_position_maker(position))
    def open_order(self, **order_parameters):
        """
        Function to open an order from FXCM 
        
        Inputs: **position_parameters->dictionary List of different variables to open an order
        Output: Opened FXCM order and created Order row in db
        """
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
        try:
            return self.connection.get_orders(kind='list')
        except:
            return []
    def close_order(self, order_id):
        try:
            self.db.delete_from_table('Orders', order_id)
            self.connection.delete_order(order_id)
        except:
            pass
    def get_open_positions_ids(self):
        try:
            return self.connection.get_open_trade_ids()
        except:
            return []
    def get_default_acc_id(self):
        try:
            return self.connection.get_default_account()
        except:
            return []

        
if __name__ == "__main__":
    import pandas
    check = Fxcm()
    check.connect()
    data = check.get_acc_info()
    print(list(data.iloc[0]))