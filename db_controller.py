import sqlite3
import os.path
from os import path
import pandas as pd

class Db_Controller():
    def __init__(self):
        pass
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
        connection, cursor=self.db_open_connection()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
            username text PRIMARY KEY not null,
            password text not null,
            unique(username)
            )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Fxcm_Info(
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS OpenPosition(
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS ClosedPosition(
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS Orders(
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS symbols_to_get(
            symbol text null PRIMARY KEY not null,
            timeframe text null,
            quantity integer null,
            unique(symbol)
            )""")
        self.db_close_connection(connection)

    def db_open_connection(self):
        connection = sqlite3.connect('./data/data.dll') #Change for folder
        cursor = connection.cursor()
        return connection, cursor
    def db_close_connection(self, connection):
        connection.close()


    def create_price_data_table(self, symbol, timeframe):
        connection, cursor=self.db_open_connection()
        cursor.execute("""CREATE TABLE IF NOT EXISTS {}_{}(
            date text primary key,
            bidopen real null,
            bidclose real null,
            bidhigh real null,
            bidlow real null,
            askopen real null,
            askclose real null,
            askhigh real null,
            asklow real null,
            tickqty
            )""".format(symbol, timeframe))

        self.db_close_connection(connection)

    def print_table(self, table):    
        """
        Supportive function to test DB values from GUI
        Input: table->str Name of the table
        Output: Prints rows from the desired table
        """
        connection, cursor = self.db_open_connection()
        cursor.execute("SELECT * FROM {}".format(table))
        data = cursor.fetchall()
        self.db_close_connection(connection)
        print(data)
    def get_table(self, table):
        """
        Supportive function to get DB values from GUI
        Input: table->str Name of the table
        Output: Returns all rows from the desired table
        """
        connection, cursor = self.db_open_connection()
        cursor.execute("SELECT * FROM {}".format(table))
        data = cursor.fetchall()
        self.db_close_connection(connection)
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
        connection, cursor = self.db_open_connection()
        cursor.execute("PRAGMA table_info({})".format(table))
        tables = cursor.fetchall()
        pk_name = ''
        for x in tables:
            if x[3]==1:
                pk_name = x[1]
                break
        statement = 'UPDATE {} SET '.format(table)
        next_statement = ', '.join([a+'='+'?' for a in columns])
        statement+= next_statement + ' WHERE '+pk_name+'= {}'.format(pk_value)
        cursor.execute(statement, values)
        connection.commit()
        self.db_close_connection(connection)

    def insert_into_price_data_table(self, data, symbol, interval):
        connection, cursor = self.db_open_connection()
        data.to_sql('{}_{}_Temp'.format(symbol, interval), con=connection, if_exists='replace', index=True)
        cursor.execute("INSERT OR IGNORE INTO {}_{}(date, bidopen, bidclose, bidhigh, bidlow, askopen, askclose, askhigh, asklow, tickqty) SELECT date, bidopen, bidclose, bidhigh, bidlow, askopen, askclose, askhigh, asklow, tickqty FROM {}_{}_Temp".format(symbol, interval, symbol, interval))
        connection.commit()
        self.db_close_connection(connection)

    def insert_into_table(self, table, data):
        """
        Function to input data into a specific table
        Inputs: 
        table->str: name of the table
        data->list: all the required data (must hold the same number of values as columns), ordered by columns
        Output: Imported data to the table
        """
        connection, cursor=self.db_open_connection()
        cursor.execute("PRAGMA table_info({})".format(table))
        number = len(cursor.fetchall())
        values = '(' + '?,'*number
        values = values[:-1]+')'
        statement = "INSERT OR IGNORE INTO {} VALUES"+values
        cursor.execute(statement.format(table), data)
        connection.commit()
        self.db_close_connection(connection)

    def delete_from_table(self, table, pk_value):
        connection, cursor= self.db_open_connection()
        cursor.execute("PRAGMA table_info({})".format(table))
        tables = cursor.fetchall()
        pk_name = ''
        for x in tables:
            if x[3]==1:
                pk_name = x[1]
                break
        cursor.execute("DELETE FROM {} WHERE {}='{}'".format(table, pk_name, pk_value))
        connection.commit()
        self.db_close_connection(connection)

    def update_table(self, table, pk_value, new_values):
        """
        Function to update a specific row in a specific table
        Inputs: 
        table->str: Name of the desired table
        pk_value->int/float/str: Primary key of the row to be updated
        new_values->list: List of the new values for the select row
        Output: Updated row in a specific table
        """
        connection, cursor= self.db_open_connection()
        cursor.execute("PRAGMA table_info({})".format(table))
        columns = [x[1] for x in cursor.fetchall()]
        cursor.execute("PRAGMA table_info({})".format(table))
        tables = cursor.fetchall()
        pk_name = ''
        for x in tables:
            if x[3]==1:
                pk_name = x[1]
                break
        statement = "UPDATE {} SET "
        next_statement = ', '.join(str(a)+'='+'?' for a, b in zip(columns, new_values))
        statement = statement.format(table)+next_statement+" WHERE {} = ?".format(pk_name)
        new_values.append(pk_value)
        cursor.execute(statement, new_values)
        connection.commit()
        self.db_close_connection(connection)

    def query_table(self, table, columns, fields=None, values=None):
        """
        Function to update a specific row in a specific table
        Inputs: 
        table->str: Name of the desired table
        pk_value->int/float/str: Primary key of the row to be updated
        new_values->list: List of the new values for the select row
        Output: Updated row in a specific table
        """
        connection, cursor= self.db_open_connection()

        if values!=None and fields!=None:
            statement = "SELECT {} FROM {} WHERE {} ".format(', '.join(columns), table, '=?, '.join(fields))
            cursor.execute(statement, values)
            result = cursor.fetchall()
            self.db_close_connection(connection)
            return result
        else:
            return []

    def query_account_info(self):
        """
        Function to get a fxcm info
        Output: fxcm info
        """
        connection, cursor= self.db_open_connection()
        statement = "SELECT from Fxcm_Info"
        cursor.execute(statement)
        result = cursor.fetchone()
        self.db_close_connection(connection)
        return result


    def query_price_data(self, symbol, interval, quantity=None):
        try:
            """
            Function to query a specific data from a specific table
            Inputs: 
            symbol->str: Name of the symbol
            timeframe->str: Name of the time frame
            quantity->int: number of rows to get
            Output: The result of query
            """
            if quantity==None:
                connection, cursor = self.db_open_connection()
                query=""" SELECT FROM {} """.format('{}_{}'.format(symbol, interval))
                result=pd.read_sql(query, connection)
                self.db_close_connection(connection)
                return result
            else:
                connection, cursor = self.db_open_connection()
                cursor.execute(""" SELECT COUNT(*) FROM {} """.format('{}_{}'.format(symbol, interval)))
                count=cursor.fetchone()
                count=count[0]
                limit_number=count-quantity
                query=""" SELECT * FROM {} LIMIT ? OFFSET ? """.format('{}_{}'.format(symbol, interval))
                result=pd.read_sql(query, connection, params=(quantity, limit_number))
                self.db_close_connection(connection)
                return result
        except Exception as e:
            print(e, 99999999999999)
            result=pd.DataFrame()
            return result


    def test_print(self):
        
        """
        Supportive function to test DB values from GUI
        Output: Prints rows from the desired table
        """
        connection, cursor=self.db_open_connection()
        cursor.execute("SELECT * FROM Orders")
        print(cursor.fetchall())
        self.db_close_connection(connection)

if __name__ == "__main__":
    a = Db_Controller()
    test = {'t': 1, 'ratePrecision': 5, 'tradeId': '31527682', 'accountName': '05616035', 'accountId': '5616035', 'roll': 0, 'com': 0, 'open': 1.10784, 'valueDate': '', 'grossPL': -0.54242, 'close': 1.10821, 'visiblePL': -3.7, 'isDisabled': False, 'currency': 'EUR/USD', 'isBuy': False, 'amountK': 1, 'currencyPoint': 0.1466, 'time': '10272019090547', 'usedMargin': 4.5, 'stop': 0, 'stopMove': 0, 'limit': 0, 'maker':'mamka'}
    test = [x for x in test.values()]
    test2 = {'t': 1, 'ratePrecision': 6, 'tradeId': '31525', 'accountName': '05665', 'accountId': '65', 'roll': 0, 'com': 0, 'open': 1.10784, 'valueDate': '', 'grossPL': -0.54242, 'close': 1.10821, 'visiblePL': -3.7, 'isDisabled': False, 'currency': 'EUR/USD', 'isBuy': False, 'amountK': 1, 'currencyPoint': 0.1466, 'time': '10272019090547', 'usedMargin': 4.5, 'stop': 0, 'stopMove': 0, 'limit': 0, 'maker':'mamka'}
    test2 = [x for x in test2.values()]
    test3 = {'t': 1, 'ratePrecision': 8, 'tradeId': '3112512525', 'accountName': '034734765', 'accountId': '65', 'roll': 122, 'com': 0, 'open': 1.10784, 'valueDate': '', 'grossPL': -0.54242, 'close': 1.10821, 'visiblePL': -3.7, 'isDisabled': False, 'currency': 'EUR/USD', 'isBuy': False, 'amountK': 1, 'currencyPoint': 0.1466, 'time': '10272019090547', 'usedMargin': 4.5, 'stop': 0, 'stopMove': 0, 'limit': 0, 'maker':'mamka'}
    test3 = [x for x in test3.values()]
    a.insert_into_table('Open_Positions', test)
    a.insert_into_table('Open_Positions', test2)
    a.update_table('Open_Positions', '31525', test3)
    a.insert_into_table('Open_Positions', test2)
    #a.update_table('Users', test2)
    a.test_print()

