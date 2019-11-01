import sqlite3
import os.path
from os import path

class Db_Controller():
    def __init__(self):
        self.connection = None
        self.cursor = None
    def create_schema(self):
        
        """
        Create all the required tables and their columns
        Output: created schema in SQLITE database
        List of created tables:
        Users - user info (login and password)
        Fxcm_Info - user related info from FXCM server
        Open_Positions - list of currently opened positions at FXCM server from this user
        Closed_Positions - list of currently closed positions at FXCM server from this user
        Orders - list of currently open orders at FXCM server from this user
        """
        self.db_open_connection()
        self.cursor.execute("""CREATE TABLE Users (
            username text PRIMARY KEY not null,
            password text not null
            )""")
        self.cursor.execute("""CREATE TABLE Account(
            accountId int PRIMARY KEY not null,
            accountName text null,
            balance real null,
            dayPL real null,
            equity real null,
            grossPL real null,
            hedging text null,
            mc text null,
            mcDate text null,
            ratePrecision real null,
            t real null,
            usableMargin real null,
            usableMargin3Perc real null,
            usableMargininPerc real null,
            usdMr real null,
            usdMr3 real null
            )""")
        self.cursor.execute("""CREATE TABLE OpenPosition(
            t real null,
            ratePrecision real null,
            tradeId text not null PRIMARY KEY,
            accountName text null,
            accountId text null,
            roll real null,
            com real null,
            open real null,
            valueDate text null,
            grossPL real null,
            close real null,
            visiblePL real null,
            isDisabled text null,
            currency text null,
            isBuy text null,
            amountK real null,
            currencyPoint real null,
            time text null,
            usedMargin real null,
            stop real null,
            stopMove real null,
            lim real null,
            positionMaker text null
            )""")
        self.cursor.execute("""CREATE TABLE ClosedPosition(
            t real null,
            ratePrecision real null,
            tradeId text not null PRIMARY KEY,
            accountName text null,
            roll real null,
            com real null,
            open real null,
            valueDate text null,
            grossPL real null,
            close real null,
            visiblePL real null,
            currency text null,
            isBuy text null,
            amountK real null,
            currencyPoint real null,
            openTime text null,
            closeTime text null,
            positionMaker text null
            )""")
        self.cursor.execute("""CREATE TABLE Orders(
            t real null,
            ratePrecision real null,
            orderId text not null PRIMARY KEY,
            tradeId text null,
            time text null,
            accountName text null,
            accountId text null,
            timeInForce text null,
            expireDate text null,
            currency text null,
            isBuy text null,
            buy text null,
            sell text null,
            type text null,
            status int null,
            amountK real null,
            currencyPoint real null,
            stopMove real null,
            stop real null,
            stopRate real null,
            lim real null,
            limitRate real null,
            isEntryOrder text null,
            ocoBulkId real null,
            isNetQuantity text null,
            isLimitOrder text null,
            isStopOrder text null,
            isELSOrder text null,
            stopPegBaseType real null,
            limitPegBaseType real null,
            range real null,
            position_maker text null
            )""")
    def db_open_connection(self):
        if path.exists('data/data.dll'):
            self.connection = sqlite3.connect('data/data.dll') #Change for folder
            self.cursor = self.connection.cursor()
        else:
            self.connection = sqlite3.connect('data/data.dll') #Change for folder
            self.cursor = self.connection.cursor()
            self.create_schema()
        return self.connection, self.cursor
    def db_close_connection(self):
        self.connection.close()
    def insert_into_table(self, table, data):
        """
        Function to input data into a specific table
        Inputs: 
        table->str: name of the table
        data->list: all the required data (must hold the same number of values as columns), ordered by columns
        Output: Imported data to the table
        """
        self.db_open_connection()
        self.cursor.execute("PRAGMA table_info({})".format(table))
        number = len(self.cursor.fetchall())
        values = '(' + '?,'*number
        values = values[:-1]+')'
        statement = "INSERT or IGNORE INTO {} VALUES"+values
        self.cursor.execute(statement.format(table), data)
        self.connection.commit()
        self.db_close_connection()
    def delete_from_table(self, table, pk_value):
        self.db_open_connection()
        self.cursor.execute("PRAGMA table_info({})".format(table))
        tables = self.cursor.fetchall()
        pk_name = ''
        for x in tables:
            if x[3]==1:
                pk_name = x[1]
                break
        self.cursor.execute("DELETE FROM {} WHERE {}='{}'".format(table, pk_name, pk_value))
        self.connection.commit()
        self.db_close_connection()
    def update_table(self, table, pk_value, new_values):
        """
        Function to update a specific row in a specific table
        Inputs: 
        table->str: Name of the desired table
        pk_value->int/float/str: Primary key of the row to be updated
        new_values->list: List of the new values for the select row
        Output: Updated row in a specific table
        """
        self.db_open_connection()
        self.cursor.execute("PRAGMA table_info({})".format(table))
        columns = [x[1] for x in self.cursor.fetchall()]
        self.cursor.execute("PRAGMA table_info({})".format(table))
        tables = self.cursor.fetchall()
        pk_name = ''
        for x in tables:
            if x[3]==1:
                pk_name = x[1]
                break
        statement = "UPDATE {} SET "
        next_statement = ', '.join(str(a)+'='+'?' for a, b in zip(columns, new_values))
        statement = statement.format(table)+next_statement+" WHERE {} = ?".format(pk_name)
        new_values.append(pk_value)
        self.cursor.execute(statement, new_values)
        self.connection.commit()
        self.db_close_connection()
    def print_table(self, table):
        
        """
        Supportive function to test DB values from GUI
        Input: table->str Name of the table
        Output: Prints rows from the desired table
        """
        self.db_open_connection()
        self.cursor.execute("SELECT * FROM {}".format(table))
        data = self.cursor.fetchall()
        print(data)
        self.db_close_connection()
        return data
    def update_from_stream(self, table, columns, values, pk_value):
        """
        Function to update a row based on update from streaming data
        Inputs:
        table->str: Name of the table
        columns->list: List of the table's columns to be updated
        values->int/float/str: Corresponding column value, must be in order with columns
        pk_value->int/float/str: Primary key value for update statement
        """
        self.db_open_connection()
        self.cursor.execute("PRAGMA table_info({})".format(table))
        tables = self.cursor.fetchall()
        pk_name = ''
        for x in tables:
            if x[3]==1:
                pk_name = x[1]
                break
        statement = 'UPDATE {} SET '.format(table)
        next_statement = ', '.join([a+'='+'?' for a in columns])
        statement+= next_statement + ' WHERE '+pk_name+'= {}'.format(pk_value)
        self.cursor.execute(statement, values)
        self.connection.commit()
        self.db_close_connection()


if __name__ == "__main__":
    a = Db_Controller()
    test = {'t': 1, 'ratePrecision': 5, 'tradeId': '31527682', 'accountName': '05616035', 'accountId': '5616035', 'roll': 0, 'com': 0, 'open': 1.10784, 'valueDate': '', 'grossPL': -0.54242, 'close': 1.10821, 'visiblePL': -3.7, 'isDisabled': False, 'currency': 'EUR/USD', 'isBuy': False, 'amountK': 1, 'currencyPoint': 0.1466, 'time': '10272019090547', 'usedMargin': 4.5, 'stop': 0, 'stopMove': 0, 'limit': 0, 'maker':'mamka'}
    test = [x for x in test.values()]
    test2 = {'t': 1, 'ratePrecision': 6, 'tradeId': '31525', 'accountName': '05665', 'accountId': '65', 'roll': 0, 'com': 0, 'open': 1.10784, 'valueDate': '', 'grossPL': -0.54242, 'close': 1.10821, 'visiblePL': -3.7, 'isDisabled': False, 'currency': 'EUR/USD', 'isBuy': False, 'amountK': 1, 'currencyPoint': 0.1466, 'time': '10272019090547', 'usedMargin': 4.5, 'stop': 0, 'stopMove': 0, 'limit': 0, 'maker':'mamka'}
    test2 = [x for x in test2.values()]
    test3 = {'t': 1, 'ratePrecision': 8, 'tradeId': '3112512525', 'accountName': '034734765', 'accountId': '65', 'roll': 122, 'com': 0, 'open': 1.10784, 'valueDate': '', 'grossPL': -0.54242, 'close': 1.10821, 'visiblePL': -3.7, 'isDisabled': False, 'currency': 'EUR/USD', 'isBuy': False, 'amountK': 1, 'currencyPoint': 0.1466, 'time': '10272019090547', 'usedMargin': 4.5, 'stop': 0, 'stopMove': 0, 'limit': 0, 'maker':'mamka'}
    test3 = [x for x in test3.values()]
    a.insert_into_table('OpenPosition', test)
    a.insert_into_table('OpenPosition', test2)
    a.update_table('OpenPosition', '31525', test3)
    a.insert_into_table('OpenPosition', test2)
    columns = ['roll', 'com', 'open']
    values = [2, 5, 7]
    a.update_from_stream('OpenPosition', columns, values, '31525')
    #a.update_table('Users', test2)
    a.print_table('OpenPosition')

