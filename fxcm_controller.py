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
        return self.connection.get_open_positions_summary()
    def get_closed_positions(self):
        return self.connection.get_closed_positions_summary()

        
if __name__ == "__main__":
    import pandas
    check = Fxcm()
    data = check.get_acc_info()
    print(list(data.iloc[0]))