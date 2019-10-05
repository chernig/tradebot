from fxcmpy import *




class Fxcm():
    def __init__(self):
        self.connection = fxcmpy(access_token='a46718dbcf04edf1b8135816d96d38a7703f2d65', log_level='error', server='demo')
        self.connection_status = self.connection.is_connected()
    def get_acc_info(self):
        return self.connection.get_accounts().T
        
if __name__ == "__main__":
    check = Fxcm()

    print(type(check.get_acc_info()))
    