from fxcmpy import *




class Fxcm():
    def __init__(self):
        self.connection = fxcmpy(access_token='a46718dbcf04edf1b8135816d96d38a7703f2d65', log_level='error', server='demo')
        self.connection_status = self.connection.is_connected()

if __name__ == "__main__":
    print('tadadadma')
    check = Fxcm()

    print(check.connection_status)
    