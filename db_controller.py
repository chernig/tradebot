import sqlite3

class Db_Controller():
    def __init__(self):
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        self.create_schema()
        self.connection.commit()
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
        self.cursor.execute("""CREATE TABLE Users (
            username text PRIMARY KEY not null,
            password text not null
            )""")
        self.cursor.execute("""CREATE TABLE Fxcm_Info(
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
        self.cursor.execute("""CREATE TABLE Open_Positions(
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
        self.cursor.execute("""CREATE TABLE Closed_Positions(
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
    def insert_into_table(self, table, data):
        """
        Function to input data into a specific table
        Inputs: 
        table->str: name of the table
        data->list: all the required data (must hold the same number of values as columns), ordered by columns
        Output: Imported data to the table
        """
        self.cursor.execute("PRAGMA table_info({})".format(table))
        number = len(self.cursor.fetchall())
        values = '(' + '?,'*number
        values = values[:-1]+')'
        statement = "INSERT INTO {} VALUES"+values
        self.cursor.execute(statement.format(table), data)
        self.connection.commit()
    def delete_from_table(self, table, pk_value):
        self.cursor.execute("PRAGMA table_info({})".format(table))
        tables = self.cursor.fetchall()
        pk_name = ''
        for x in tables:
            if x[3]==1:
                pk_name = x[1]
                break
        self.cursor.execute("DELETE FROM {} WHERE {}='{}'".format(table, pk_name, pk_value))
        self.connection.commit()
    def update_table(self, table, pk_value, new_values):
        """
        Function to update a specific row in a specific table
        Inputs: 
        table->str: Name of the desired table
        pk_value->int/float/str: Primary key of the row to be updated
        new_values->list: List of the new values for the select row
        Output: Updated row in a specific table
        """
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
    def test_print(self):
        """
        Supportive function to test DB values from GUI
        Output: Prints rows from the desired table
        """
        self.cursor.execute("SELECT * FROM Open_Positions")
        print(self.cursor.fetchall())

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
    #a.update_table('Users', test2)
    a.test_print()

