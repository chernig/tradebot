from fxcmpy import *





class Fxcm():
    def __init__(self):
        self.token = 'a46718dbcf04edf1b8135816d96d38a7703f2d65'
        self.connection = fxcmpy(access_token=self.token, log_level='error', server='demo')
        self.connection_status = self.connection.is_connected()
        
    def get_acc_info(self):
        return self.connection.get_accounts()
    def update_token(self, new_token):
        self.token = new_token
    def get_open_positions(self):
        return self.connection.get_open_positions(kind='list')
    def get_closed_positions(self):
        return self.connection.get_closed_positions(kind='list')
    def open_position(self, **position_parameters):
        self.connection.open_trade(**position_parameters)
    def close_position(self, **position_parameters):
        self.connection.close_trade(**position_parameters)
    def edit_position(self, **position_parameters):
        self.connection.change_order(**position_parameters)
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