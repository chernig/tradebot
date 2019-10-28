from fxcmpy import *





class Fxcm():
    """
    Primary GUI controller for FXCM API
    All the methods are direct implementation of FXCM API
    Full documentation can be retrived from: https://fxcm.github.io/rest-api-docs/#section/Overview
    """
    def __init__(self):
        self.token = 'a46718dbcf04edf1b8135816d96d38a7703f2d65' # Default, for now
        self.connection = fxcmpy(access_token=self.token, log_level='error', server='demo')
        self.connection_status = self.connection.is_connected()
        
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
        self.connection.open_trade(**position_parameters)
    def close_position(self, **position_parameters):
        self.connection.close_trade(**position_parameters)
    def edit_order(self, **order_parameters):
        self.connection.change_order(**order_parameters)
    def edit_order_stop_limit(self, **order_parameters):
        self.connection.change_order_stop_limit(**order_parameters)
    def edit_position_stop_limit(self, **position_parameters):
        self.connection.change_trade_stop_limit(**position_parameters)
    def close_all_positions(self):
        self.connection.close_all()
    def open_order(self, **order_parameters):
        self.connection.create_entry_order(**order_parameters)
    def get_orders(self):
        return self.connection.get_orders(kind='list')
    def close_order(self, order_id):
        self.connection.delete_order(order_id)
    def get_open_positions_ids(self):
        return self.connection.get_open_trade_ids()
    def get_default_acc_id(self):
        return self.connection.get_default_account()

        
if __name__ == "__main__":
    import pandas
    check = Fxcm()
    data = check.get_acc_info()
    print(list(data.iloc[0]))