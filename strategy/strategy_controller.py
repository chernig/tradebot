import os, glob, sys, inspect, glob
import importlib
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from db_controller import Db_Controller
import pandas as pd
import numpy as np
import risk_management.risk_management_controller
import news_reactor.news_reactor_controller
from news_reactor import *
import fxcm_controller
import pickle
import multiprocessing
import datetime
import time
import strategy
import risk_management
import news_reactor

import warnings
warnings.filterwarnings("ignore")

pd.options.mode.chained_assignment = None
np.seterr(divide='ignore', invalid='ignore')

timeframe_to_second_dict={
                            'm1':60, 'm5':300, 'm15':900, 'm30':1800, 'H1':3600, 'H2':7200, 'H3':10800, 'H4':14400, 'H6':21600, 'H8':28800, 'D1':86400, 'W1':604800, 'M1':2592000
                            }


'''
This file consists of two classes including 'strategy_controller' and 'trading_strategy'.
This file retrieve risk management systems, strategy systems and news reactor systems from their specific folders (strategy, risk_management and rews reactor),
then it insert their name and description in a specific dictionary, and their required inputs in another dictionary, and their class names in another dictionart.
These are implemented in order to be able to retrieve them from other parts of the app such as GUI.

'''


'''
Collecting all risk management systems and inserting their information in three dictionaries.
'''
imported_risk_management_dict={}
for i in risk_management.risk_management_controller.all_packages:
    if i!='general_functions':
        imported_risk_management_dict[i]=(importlib.import_module('risk_management.'+i))
risk_management_classes_dict={}
risk_management_inputs_dict={}
risk_management_name_description_dict={}
for i, j in imported_risk_management_dict.items():
    risk_management_classes_dict[j.risk_management_name]='risk_management.'+i+'.'+i
    risk_management_inputs_dict[j.risk_management_name]=j.inputs_name_dict
    risk_management_name_description_dict[j.risk_management_name]=j.risk_management_description


'''
Collecting all news reactor systems and inserting their information in three dictionaries.
'''

imported_news_reactor_dict={}
for i in news_reactor.news_reactor_controller.all_packages:
    if i!='general_functions':
        imported_news_reactor_dict[i]=(importlib.import_module('news_reactor.'+i))
news_reactor_classes_dict={}
news_reactor_inputs_dict={}
news_reactor_name_description_dict={}
news_reactor_name_description_dict['None']=''
for i, j in imported_news_reactor_dict.items():
    news_reactor_classes_dict[j.news_reactor_name]='news_reactor.'+i+'.'+i
    news_reactor_inputs_dict[j.news_reactor_name]=j.inputs_name_dict
    news_reactor_name_description_dict[j.news_reactor_name]=j.news_reactor_description


'''
Collecting all trading strategy systems and inserting their information in three dictionaries.
'''

modules_strategies = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
imports_strategies = [os.path.basename(f)[:-3] for f in modules_strategies if not f.endswith("strategy_controller.py")]
imported_strategies_dict={}
if __name__=="__main__":
    for i in imports_strategies:
        imported_strategies_dict[i]=(importlib.import_module(i))
    trading_strategies_classes_dict={}
    trading_strategies_inputs_dict={}
    trading_strategies_name_description_dict={}
    for i, j in imported_strategies_dict.items():
        trading_strategies_classes_dict[j.strategy_name]=i+'.'+i
        trading_strategies_inputs_dict[j.strategy_name]=j.inputs_name_dict
        trading_strategies_name_description_dict[j.strategy_name]=j.strategy_description
else:
    for i in imports_strategies:
        imported_strategies_dict[i]=(importlib.import_module('strategy.'+i))
    trading_strategies_classes_dict={}
    trading_strategies_inputs_dict={}
    trading_strategies_name_description_dict={}
    for i, j in imported_strategies_dict.items():
        trading_strategies_classes_dict[j.strategy_name]='strategy.'+i+'.'+i
        trading_strategies_inputs_dict[j.strategy_name]=j.inputs_name_dict
        trading_strategies_name_description_dict[j.strategy_name]=j.strategy_description


'''
strategy_controller is the class which holds all created strategies' instances and provides methods for controlling them.
also new strategies are made through this class.
'''
class strategy_controller:
    def __init__(self):
        self.strategies_dict={}
        self.strategies_shared_memory_dict={}
        self.init_saved_strategies()

    #Loading saved strategies information and creating their trading_strategy instances.
    def init_saved_strategies(self):
        with open('./data/strategies_settings.cfg', 'rb') as f: 
            self.strategy_setting_dict = pickle.load(f)
        
        for key, value in self.strategy_setting_dict.items():
            self.add_strategy(**self.strategy_setting_dict[key])
        
    #Creating new strategies. It gets a list of arguments and passes them to trading_strategy class to create an instance of trading_strategy class.
    #Then it checks if the name of the strategy is not in the saved strategies's list or strategy_setting_dict(it hold inputs of strategies), it inserts the inputs in strategies_settings.cfg file.
    def add_strategy(self, strategy_name, trading_strategy_system, trading_strategy_inputs, symbol, timeframe, risk_management_system, risk_management_system_inputs, news_reactor_system, news_reactor_inputs):
        self.manager=multiprocessing.Manager()
        self.strategies_shared_memory_dict[strategy_name]=self.manager.dict()
        self.strategies_shared_memory_dict[strategy_name]['stop_signal']=True
        self.strategies_shared_memory_dict[strategy_name]['strategy_status']='Not started'
        self.strategies_shared_memory_dict[strategy_name]['last_start']='Not started'
        self.strategies_shared_memory_dict[strategy_name]['last_stop']='Not started'
        self.strategies_shared_memory_dict[strategy_name]['stop_backtesting_signal']=True
        self.strategies_shared_memory_dict[strategy_name]['backtest_progress_counter']=0
        self.strategies_shared_memory_dict[strategy_name]['backtesting_result']={}
        
        self.strategies_dict[strategy_name]=trading_strategy(self.strategies_shared_memory_dict[strategy_name], strategy_name, trading_strategy_system, trading_strategy_inputs, symbol, timeframe, risk_management_system, risk_management_system_inputs, news_reactor_system, news_reactor_inputs)
        if strategy_name not in self.strategy_setting_dict:
            self.strategy_setting_dict[strategy_name]={
                                                        'strategy_name':strategy_name,
                                                        'symbol':symbol,
                                                        'timeframe':timeframe,
                                                        'trading_strategy_system':trading_strategy_system,
                                                        'trading_strategy_inputs':trading_strategy_inputs,
                                                        'risk_management_system':risk_management_system,
                                                        'risk_management_system_inputs':risk_management_system_inputs,
                                                        'news_reactor_system':news_reactor_system,
                                                        'news_reactor_inputs':news_reactor_inputs
                                                        }
            with open('./data/strategies_settings.cfg', 'wb') as f: 
                pickle.dump(self.strategy_setting_dict, f)



    #Editing strategy. It gets the strategy name and parameters to edit, then it reinstantiates the strategy system class, and saves the new setting.
    def edit_strategy(self, strategy_name, arguments):
        self.strategies_dict[strategy_name].stop()
        self.strategies_dict[strategy_name].terminate()
        for key, value in arguments.items():
            setattr(self.strategies_dict[strategy_name], key, value)
            self.strategy_setting_dict[self.strategies_dict[strategy_name].strategy_name][key]=value
            
        self.strategies_dict[strategy_name].init_strategy()
        with open('./data/strategies_settings.cfg', 'wb') as f: 
            pickle.dump(self.strategy_setting_dict, f)
        
    #Deleting strategy. It gets strategy name and calls delete method of the trading_strategy class, the it update strategies_settings.cfg file
    def delete_strategy(self, strategy_name):
        self.strategies_dict[strategy_name].delete()
        try:
            self.strategies_dict[strategy_name].terminate()
        except:
            pass
        del self.strategy_setting_dict[strategy_name]
        with open('./data/strategies_settings.cfg', 'wb') as f: 
            pickle.dump(self.strategy_setting_dict, f)
        del self.strategies_dict[strategy_name]

    #Stoping all strategies. It stops all strategies by stoping their processes.
    def stop_all_strategies(self):
        for key, value in self.strategies_dict.items():
            self.strategies_dict[key].stop()
            try:
                self.strategies_dict[key].terminate()
            except:
                pass

    #Stoping a strategy. It stops the strategy by stoping its processes.
    def stop_strategy(self, strategy_name):
        self.strategies_dict[strategy_name].stop()
        try:
            self.strategies_dict[strategy_name].terminate()
        except:
            pass

    #Starting all strategies. It starts all strategies by starting their processes.
    def start_all_strategies(self):
        self.init_saved_strategies()
        for key, value in self.strategies_dict.items():
            if self.strategies_dict[key].start_process()==True:
                self.strategies_dict[key].start()

    #Starting a strategy. It starts the strategy by starting its processes.
    def start_strategy(self, strategy_name):
        self.init_saved_strategies()
        if self.strategies_dict[strategy_name].start_process()==True:
            self.strategies_dict[strategy_name].start()

    #Backtesting strategy. It gets strategy name, quantity of prices for backtesting and initial capital.
    def backtest_strategy(self, strategy_name, quantity, capital):
        self.strategies_dict[strategy_name].backtest(quantity, capital)

    def get_backtest_result(self, strategy_name):
        return self.strategies_shared_memory_dict[strategy_name]['backtesting_result']


    #It gets the progress perventage of backtesing.
    def get_backtest_progress_rate(self, strategy_name):
        return self.strategies_shared_memory_dict[strategy_name]['backtest_progress_counter']

    #It raises a flag to stop backtesting.
    def backtest_stop(self, strategy_name):
        self.strategies_shared_memory_dict[strategy_name]['stop_backtesting_signal']=True
        self.strategies_shared_memory_dict[strategy_name]['backtesting_result']={}

    #It gets the status of the strategy.
    def strategy_status_get(self, strategy_name):
        return self.strategies_shared_memory_dict[strategy_name]['strategy_status'], self.strategies_shared_memory_dict[strategy_name]['last_start'], self.strategies_shared_memory_dict[strategy_name]['last_stop']



'''
trading_strategy class is a class of strategy. It gets list of setting for a strategy including:
strategy_name: str,
trading_strategy_system: str,
trading_strategy_inputs: dict,
symbol: str,
timeframe: str,
risk_management_system: str,
risk_management_system_inputs:dict,
news_reactor_system: str,
news_reactor_inputs:dict

trading_strategy class inherits from multiprocessing.Process for multiprocessing.
When start_process method of this class is called, a new process starts.

'''

class trading_strategy(multiprocessing.Process):
    def __init__(self, shared_memory_dict, strategy_name, trading_strategy_system, trading_strategy_inputs, symbol, timeframe, risk_management_system, risk_management_system_inputs, news_reactor_system, news_reactor_inputs):
        multiprocessing.Process.__init__(self)
        self.shared_memory_dict=shared_memory_dict
        self.strategy_name=strategy_name
        self.trading_strategy_system=trading_strategy_system
        self.symbol=symbol
        self.timeframe=timeframe
        self.quantity=1000
        self.risk_management_system=risk_management_system
        self.news_reactor_system=news_reactor_system
        self.trading_strategy_inputs=trading_strategy_inputs
        self.risk_management_system_inputs=risk_management_system_inputs
        self.news_reactor_inputs=news_reactor_inputs
        self.open_position_trade_id=None
        self.position_type=None
        self.db=Db_Controller()
        self.fxcm_instance=fxcm_controller.Fxcm()
        self.init_strategy()
        self.name=self.strategy_name

    def __str__(self):
        return self.strategy_name

    #Preparing required sources. This method instantiate the classes of selected systems (risk management system, trading strategy system and news reactor system) using given inputs. 
    def init_strategy(self):
        strategy_args=self.trading_strategy_inputs
        strategy_args['symbol']=self.symbol
        strategy_args['timeframe']=self.timeframe
        risk_management_args=self.risk_management_system_inputs
        risk_management_args['symbol']=self.symbol
        risk_management_args['timeframe']=self.timeframe
        self.trading_strategy_instance=eval(trading_strategies_classes_dict[self.trading_strategy_system])(**strategy_args)
        self.risk_management_instance=eval(risk_management_classes_dict[self.risk_management_system])(**risk_management_args)
        if self.news_reactor_system==None or self.news_reactor_system=='None':
            self.news_reactor_instance=None  #Temporary
        else:
            news_reactor_args=self.news_reactor_inputs
            news_reactor_args['symbol']=self.symbol
            news_reactor_args['timeframe']=self.timeframe
            self.news_reactor_instance=eval(news_reactor_classes_dict[self.news_reactor_system])(**news_reactor_args)
        self.db.insert_into_table('symbols_to_get', [self.symbol, self.timeframe, self.quantity])
        self.db.create_price_data_table(self.symbol, self.timeframe)

    def get_data_backtest(self, quantity):
        return self.db.query_price_data(self.symbol, self.timeframe, quantity)


    def backtest(self, qty, cap):
        try:
            print(9999999999999999999)
            self.shared_memory_dict['backtesting_result']={} 
            self.shared_memory_dict['backtest_progress_counter']=0 
            quantity=int(qty)
            capital=int(cap)
            initial_capital=capital
            try:
                data=self.get_data_backtest(quantity)
                if data.empty==True or len(data.index)<quantity:
                    if self.fxcm_instance.connection==None:
                        self.fxcm_instance.connect()
                        self.fxcm_instance.get_price_data(self.symbol, self.timeframe, quantity)
                        data=self.get_data_backtest(quantity)
                    else:
                        if self.fxcm_instance.connection.is_connected():
                            self.fxcm_instance.get_price_data(self.symbol, self.timeframe, quantity)
                            data=self.get_data_backtest(quantity)
            except Exception as e:
                print(e, 66666666666666666)
                backtest_result_dict={}
                backtest_result_dict['Backtesting period']=datetime.timedelta(minutes=0)
                backtest_result_dict['Number of trades']=0
                backtest_result_dict['Number of successful trades']=0
                backtest_result_dict['Number of unsuccessful trades']=0
                backtest_result_dict['Number of stop loss triggered']=0
                backtest_result_dict['Number of limit triggered']=0
                backtest_result_dict['Longest time in a trade']=0
                backtest_result_dict['Shortest time in a trade']=0
                backtest_result_dict['Average time in a trade']=0
                backtest_result_dict['Maximum drawup']=0
                backtest_result_dict['Maximum drawdown']=0
                backtest_result_dict['Maximum profit in one trade']=0
                backtest_result_dict['Maximum loss in one trade']=0
                backtest_result_dict['Maximum gained pip in one trade']=0
                backtest_result_dict['Maximum lost pip in one trade']=0
                backtest_result_dict['Average gained/lost pip per trade']=0
                backtest_result_dict['Maximum consecutive successfull trade']=0
                backtest_result_dict['Maximum consecutive unsuccessfull trade']=0
                backtest_result_dict['Total gained/lost pip']=0
                backtest_result_dict['Net gained/lost pip']=0
                backtest_result_dict['Average gained/lost pip per day']=0
                backtest_result_dict['Gained pip']=0
                backtest_result_dict['Lost pip']=0
                backtest_result_dict['Profit']=0
                backtest_result_dict['Loss']=0
                backtest_result_dict['Capital']=0
                backtest_result_dict['Net profit/loss']=0
                backtest_result_dict['Net profit/loss percentage']=0
                backtest_result_dict['Largest position size']=0
                backtest_result_dict['Smallest position size']=0
                backtest_result_dict['Largest stop loss']=0
                backtest_result_dict['Smallest stop loss']=0
                backtest_result_dict['Largest limit']=0
                backtest_result_dict['Smallest limit']=0
                self.shared_memory_dict['backtesting_result']=backtest_result_dict     
                return backtest_result_dict

            try:
                data['date'] =  pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S')
            except:
                data['date'] =  pd.to_datetime(data['date'], format='%m/%d/%Y %H:%M')

            if self.symbol[-3:]=='JPY':
                pip_multiplier=100
            else:
                pip_multiplier=10000
            round_digit=3

            position_type=None
            position_entered_price=None
            position_entered_price_index=None
            lost_pip=[]
            lost_money=[]
            gained_pip=[]
            gained_money=[]
            all_trades_pip_net=[]
            all_trades_pip_total=[]
            drawdowns=[]
            drawups=[]
            stop_loss_triggered=0
            limit_triggered=0
            time_in_trade=[]
            position_size_list=[]
            stop_loss_list=[]
            limit_list=[]

            self.shared_memory_dict['stop_backtesting_signal']=False
            for i in range(len(data.date)):
                try:
                    if self.shared_memory_dict['stop_backtesting_signal']==True:
                        self.shared_memory_dict['backtest_progress_counter']=0
                        backtest_result_dict={}
                        backtest_result_dict['Backtesting period']=datetime.timedelta(minutes=0)
                        backtest_result_dict['Number of trades']=0
                        backtest_result_dict['Number of successful trades']=0
                        backtest_result_dict['Number of unsuccessful trades']=0
                        backtest_result_dict['Number of stop loss triggered']=0
                        backtest_result_dict['Number of limit triggered']=0
                        backtest_result_dict['Longest time in a trade']=0
                        backtest_result_dict['Shortest time in a trade']=0
                        backtest_result_dict['Average time in a trade']=0
                        backtest_result_dict['Maximum drawup']=0
                        backtest_result_dict['Maximum drawdown']=0
                        backtest_result_dict['Maximum profit in one trade']=0
                        backtest_result_dict['Maximum loss in one trade']=0
                        backtest_result_dict['Maximum gained pip in one trade']=0
                        backtest_result_dict['Maximum lost pip in one trade']=0
                        backtest_result_dict['Average gained/lost pip per trade']=0
                        backtest_result_dict['Maximum consecutive successfull trade']=0
                        backtest_result_dict['Maximum consecutive unsuccessfull trade']=0
                        backtest_result_dict['Total gained/lost pip']=0
                        backtest_result_dict['Net gained/lost pip']=0
                        backtest_result_dict['Average gained/lost pip per day']=0
                        backtest_result_dict['Gained pip']=0
                        backtest_result_dict['Lost pip']=0
                        backtest_result_dict['Profit']=0
                        backtest_result_dict['Loss']=0
                        backtest_result_dict['Capital']=0
                        backtest_result_dict['Net profit/loss']=0
                        backtest_result_dict['Net profit/loss percentage']=0
                        backtest_result_dict['Largest position size']=0
                        backtest_result_dict['Smallest position size']=0
                        backtest_result_dict['Largest stop loss']=0
                        backtest_result_dict['Smallest stop loss']=0
                        backtest_result_dict['Largest limit']=0
                        backtest_result_dict['Smallest limit']=0
                        self.shared_memory_dict['backtesting_result']=backtest_result_dict   
                        return backtest_result_dict
                    else:
                        if i==len(data.date)-1:
                            data_temp=data.iloc[:].copy()
                        else:
                            data_temp=data.iloc[:i+1].copy()

                        
                        condition_result=self.trading_strategy_instance.backtest(position_type, data_temp)

                        if condition_result!=None:
                            if position_type==None and i<len(data.date)-2:
                                if condition_result=='buy':
                                    position_size, required_margin, stop_loss, limit, stop_loss_pip, limit_pip, pip_value=self.risk_management_instance.backtest('buy', data_temp, capital)
                                    position_type='buy'
                                    position_entered_price=data_temp.bidclose.iloc[i]
                                    position_entered_price_index=i
                                    position_size_list.append(position_size)
                                    stop_loss_list.append(stop_loss_pip)
                                    limit_list.append(limit_pip)
                                    
                                elif condition_result=='sell':
                                    position_size, required_margin, stop_loss, limit, stop_loss_pip, limit_pip, pip_value=self.risk_management_instance.backtest('sell', data_temp, capital)
                                    position_type='sell'
                                    position_entered_price=data_temp.bidclose.iloc[i]
                                    position_entered_price_index=i
                                    position_size_list.append(position_size)
                                    stop_loss_list.append(stop_loss_pip)
                                    limit_list.append(limit_pip)
                                    
                            elif (i==len(data.date)-2 and (position_type=='buy' or position_type=='sell')) or ((position_type=='buy' or position_type=='sell') and condition_result=='exit') or ((data.bidhigh.iloc[i]>stop_loss and position_type=='sell') or (data.bidlow.iloc[i]<limit and position_type=='sell') or (data.bidlow.iloc[i]<stop_loss and position_type=='buy') or (data.bidhigh.iloc[i]>limit and position_type=='buy')):
                                position_exit_price=data.bidclose.iloc[i]
                                spread=abs(data.bidclose.iloc[i]-data.askclose.iloc[i])
                                if condition_result=='exit' or i==len(data.date)-2:
                                    if position_type=='buy':
                                        pl_pip=position_exit_price-position_entered_price
                                        pl_pip-=spread
                                        drawups.append(max(data.bidclose.iloc[position_entered_price_index:i+1])-position_entered_price)
                                        drawdowns.append(min(data.bidclose.iloc[position_entered_price_index:i+1])-position_entered_price)
                                    else:
                                        pl_pip=position_entered_price-position_exit_price
                                        pl_pip-=spread
                                        drawups.append(position_entered_price-min(data.bidclose.iloc[position_entered_price_index:i+1]))
                                        drawdowns.append(position_entered_price-max(data.bidclose.iloc[position_entered_price_index:i+1]))

                                elif data.bidhigh.iloc[i]>stop_loss and position_type=='sell':
                                    pl_pip=position_entered_price-stop_loss
                                    pl_pip-=spread
                                    stop_loss_triggered+=1
                                    drawups.append(position_entered_price-min(data.bidclose.iloc[position_entered_price_index:i+1]))
                                    drawdowns.append(position_entered_price-max(data.bidclose.iloc[position_entered_price_index:i+1]))

                                elif data.bidlow.iloc[i]<limit and position_type=='sell':
                                    pl_pip=position_entered_price-limit
                                    pl_pip-=spread
                                    limit_triggered+=1
                                    drawups.append(position_entered_price-min(data.bidclose.iloc[position_entered_price_index:i+1]))
                                    drawdowns.append(position_entered_price-max(data.bidclose.iloc[position_entered_price_index:i+1]))

                                elif data.bidlow.iloc[i]<stop_loss and position_type=='buy':
                                    pl_pip=stop_loss-position_entered_price
                                    pl_pip-=spread
                                    stop_loss_triggered+=1
                                    drawups.append(max(data.bidclose.iloc[position_entered_price_index:i+1])-position_entered_price)
                                    drawdowns.append(min(data.bidclose.iloc[position_entered_price_index:i+1])-position_entered_price)

                                elif data.bidhigh.iloc[i]>limit and position_type=='buy':
                                    pl_pip=limit-position_entered_price
                                    pl_pip-=spread
                                    limit_triggered+1
                                    drawups.append(max(data.bidclose.iloc[position_entered_price_index:i+1])-position_entered_price)
                                    drawdowns.append(min(data.bidclose.iloc[position_entered_price_index:i+1])-position_entered_price)

                                pl=pl_pip*pip_multiplier*pip_value
                                capital+=pl
                                if pl_pip>0:
                                    gained_pip.append(pl_pip)
                                    gained_money.append(pl)
                                else:
                                    lost_pip.append(pl_pip)
                                    lost_money.append(pl)
                                all_trades_pip_net.append(pl_pip)
                                all_trades_pip_total.append(pl_pip+spread)
                                duration_in_trade=data.date.iloc[i]-data.date.iloc[position_entered_price_index]
                                time_in_trade.append(duration_in_trade)

                                position_type=None

                        self.shared_memory_dict['backtest_progress_counter']=(i/len(data.date))*100

                except Exception as e:
                    print(e, 55555555555555555555)
                    
            self.shared_memory_dict['backtest_progress_counter']=100

            consecutive_negative=0
            consecutive_positive=0
            consecutive_negative_temp=0
            consecutive_positive_temp=0
            for i, j in enumerate(all_trades_pip_net):
                if j>0:
                    consecutive_positive_temp+=1
                    consecutive_negative_temp=0
                elif j<0:
                    consecutive_negative_temp+=1
                    consecutive_positive_temp=0
                if consecutive_positive_temp>consecutive_positive:
                    consecutive_positive=consecutive_positive_temp
                elif consecutive_negative_temp>consecutive_negative:
                    consecutive_negative=consecutive_negative_temp


            backtest_result_dict={}
            backtest_result_dict['Backtesting period']=str(data.date.iloc[-1]-data.date.iloc[0])
            backtest_result_dict['Number of trades']=len(all_trades_pip_net)
            backtest_result_dict['Number of successful trades']=len(gained_pip)
            backtest_result_dict['Number of unsuccessful trades']=len(lost_pip)
            backtest_result_dict['Number of stop loss triggered']=stop_loss_triggered
            backtest_result_dict['Number of limit triggered']=limit_triggered
            try:
                backtest_result_dict['Longest time in a trade']=str(max(time_in_trade))
            except:
                backtest_result_dict['Longest time in a trade']=str(datetime.timedelta(minutes=0))
            try:
                backtest_result_dict['Shortest time in a trade']=str(min(time_in_trade))
            except:
                backtest_result_dict['Shortest time in a trade']=str(datetime.timedelta(minutes=0))
            try:
                backtest_result_dict['Average time in a trade']=str(np.mean(time_in_trade))
            except:
                backtest_result_dict['Average time in a trade']=str(datetime.timedelta(minutes=0))
            try:
                backtest_result_dict['Maximum drawup']=round(max(drawups)*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Maximum drawup']=0
            try:
                backtest_result_dict['Maximum drawdown']=round(max(drawdowns)*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Maximum drawdown']=0
            try:
                backtest_result_dict['Maximum profit in one trade']=round(max(gained_money), round_digit)
            except:
                backtest_result_dict['Maximum profit in one trade']=0
            try:
                backtest_result_dict['Maximum loss in one trade']=round(min(lost_money), round_digit)
            except:
                backtest_result_dict['Maximum loss in one trade']=0
            try:
                backtest_result_dict['Maximum gained pip in one trade']=round(max(gained_pip)*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Maximum gained pip in one trade']=0
            try:
                backtest_result_dict['Maximum lost pip in one trade']=round(min(lost_pip)*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Maximum lost pip in one trade']=0
            try:
                backtest_result_dict['Average gained/lost pip per trade']=round((sum(all_trades_pip_net)/len(data.date))*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Average gained/lost pip per trade']=0
            backtest_result_dict['Maximum consecutive successfull trade']=consecutive_positive
            backtest_result_dict['Maximum consecutive unsuccessfull trade']=consecutive_negative
            try:
                backtest_result_dict['Total gained/lost pip']=round(sum(all_trades_pip_total)*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Total gained/lost pip']=0
            try:
                backtest_result_dict['Net gained/lost pip']=round(sum(all_trades_pip_net)*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Net gained/lost pip']=0
            try:
                backtest_result_dict['Average gained/lost pip per day']=round(sum(all_trades_pip_net)*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Average gained/lost pip per day']=0
            try:
                backtest_result_dict['Gained pip']=round(sum(gained_pip)*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Gained pip']=0
            try:
                backtest_result_dict['Lost pip']=round(sum(lost_pip)*pip_multiplier, round_digit)
            except:
                backtest_result_dict['Lost pip']=0
            try:
                backtest_result_dict['Profit']=round(sum(gained_money), round_digit)
            except:
                backtest_result_dict['Profit']=0
            try:
                backtest_result_dict['Loss']=round(sum(lost_money), round_digit)
            except:
                backtest_result_dict['Loss']=0
            backtest_result_dict['Capital']=round(capital, round_digit)
            try:
                backtest_result_dict['Net profit/loss']=round(capital-initial_capital, round_digit)
            except:
                backtest_result_dict['Net profit/loss']=0
            try:
                backtest_result_dict['Net profit/loss percentage']=round(((capital-initial_capital)/initial_capital)*100, round_digit)
            except:
                backtest_result_dict['Net profit/loss percentage']=0
            try:
                backtest_result_dict['Largest position size']=max(position_size_list)
            except:
                backtest_result_dict['Largest position size']=0
            try:
                backtest_result_dict['Smallest position size']=min(position_size_list)
            except:
                backtest_result_dict['Smallest position size']=0
            try:
                backtest_result_dict['Smallest stop loss']=round(min(stop_loss_list), round_digit)
            except:
                backtest_result_dict['Smallest stop loss']=0
            try:
                backtest_result_dict['Largest stop loss']=round(max(stop_loss_list), round_digit)
            except:
                backtest_result_dict['Largest stop loss']=0
            try:
                backtest_result_dict['Smallest limit']=round(min(limit_list), round_digit)
            except:
                backtest_result_dict['Smallest limit']=0
            try:
                backtest_result_dict['Largest limit']=round(max(limit_list), round_digit)
            except:
                backtest_result_dict['Largest limit']=0

            self.shared_memory_dict['backtesting_result']=backtest_result_dict
            return backtest_result_dict
        except Exception as e:
            print(e, 76765678999987)
            self.shared_memory_dict['backtest_progress_counter']=0
            backtest_result_dict['Backtesting period']=datetime.timedelta(minutes=0)
            backtest_result_dict['Number of trades']=0
            backtest_result_dict['Number of successful trades']=0
            backtest_result_dict['Number of unsuccessful trades']=0
            backtest_result_dict['Number of stop loss triggered']=0
            backtest_result_dict['Number of limit triggered']=0
            backtest_result_dict['Longest time in a trade']=0
            backtest_result_dict['Shortest time in a trade']=0
            backtest_result_dict['Average time in a trade']=0
            backtest_result_dict['Maximum drawup']=0
            backtest_result_dict['Maximum drawdown']=0
            backtest_result_dict['Maximum profit in one trade']=0
            backtest_result_dict['Maximum loss in one trade']=0
            backtest_result_dict['Maximum gained pip in one trade']=0
            backtest_result_dict['Maximum lost pip in one trade']=0
            backtest_result_dict['Average gained/lost pip per trade']=0
            backtest_result_dict['Maximum consecutive successfull trade']=0
            backtest_result_dict['Maximum consecutive unsuccessfull trade']=0
            backtest_result_dict['Total gained/lost pip']=0
            backtest_result_dict['Net gained/lost pip']=0
            backtest_result_dict['Average gained/lost pip per day']=0
            backtest_result_dict['Gained pip']=0
            backtest_result_dict['Lost pip']=0
            backtest_result_dict['Profit']=0
            backtest_result_dict['Loss']=0
            backtest_result_dict['Capital']=0
            backtest_result_dict['Net profit/loss']=0
            backtest_result_dict['Net profit/loss percentage']=0
            backtest_result_dict['Largest position size']=0
            backtest_result_dict['Smallest position size']=0
            backtest_result_dict['Largest stop loss']=0
            backtest_result_dict['Smallest stop loss']=0
            backtest_result_dict['Largest limit']=0
            backtest_result_dict['Smallest limit']=0
            self.shared_memory_dict['backtesting_result']=backtest_result_dict
            return backtest_result_dict


    def check_condition(self):
        try:
            print('aaaaaaaa')
            if self.news_reactor_instance==None:
                if len(self.db.query_table('Open_Positions', 'tradeId', fields='tradeId', values=self.open_position_trade_id))==0:
                    self.open_position_trade_id=None
                    self.position_type=None
                condition_result=self.trading_strategy_instance.check_strategy(self.position_type)
                if condition_result!=None:
                    if self.position_type==None:
                        if condition_result=='buy':
                            self.position_size, required_margin, stop_loss, limit, stop_loss_pip, limit_pip=self.risk_management_instance.position_size_stop_loss('buy')
                            fxcm_info=self.db.query_account_info()
                            if fxcm_info[11]>required_margin:
                                open_position_args={'symbol':'USD/JPY', 'is_buy':True,
                                                    'rate':stop_loss, 'is_in_pips':False,
                                                    'amount':self.position_size, 'time_in_force':'GTC',
                                                    'order_type':'AtMarket', "limit":limit, 'maker':self.strategy_name}
                                self.open_position_trade_id=self.fxcm_instance.open_position(**open_position_args)
                                self.position_type='buy'
                            
                        elif condition_result=='sell':
                            self.position_size, required_margin, stop_loss, limit, stop_loss_pip, limit_pip=self.risk_management_instance.position_size_stop_loss('sell')
                            fxcm_info=self.db.query_account_info()
                            if fxcm_info[11]>required_margin:
                                open_position_args={'symbol':'USD/JPY', 'is_buy':False,
                                                    'rate':stop_loss, 'is_in_pips':False,
                                                    'amount':self.position_size, 'time_in_force':'GTC',
                                                    'order_type':'AtMarket', "limit":limit, 'maker':self.strategy_name}
                                self.open_position_trade_id=self.fxcm_instance.open_position(**open_position_args)
                                self.position_type='buy'
                            
                    elif (self.position_type=='buy' or self.position_type=='sell') and condition_result=='exit':
                        close_position_args={'trade_id':self.open_position_trade_id, 'amount':self.position_size, 'maker':self.strategy_name}
                        self.fxcm_instance.close_position(**close_position_args)
                        self.open_position_trade_id=None
                        self.position_type=None
        except Exception as e:
            print(e, 'errrrrrrrrrr')

    def start_process(self):
        if self.shared_memory_dict['stop_signal']==True and self.process_status()==False:
            last_start=str(datetime.datetime.now())
            self.strategy_status='Started'
            self.shared_memory_dict['stop_signal']=False
            self.shared_memory_dict['strategy_status']='Started'
            self.shared_memory_dict['last_start']=last_start
            return True
        else:
            return False

                
    def run(self):
        try:
            print('ssssssssssss')
            
            def fxcm_reconnect():
                self.fxcm_instance=fxcm_controller.Fxcm()
                self.fxcm_instance.connect()
            try:
                self.strategy_status='Initializing'
                self.fxcm_instance=fxcm_controller.Fxcm()
                self.fxcm_instance.connect()
            except Exception as e:
                print(e)

            while True:
                try:
                    #print(11111111)
                    if self.shared_memory_dict['stop_signal']==True:
                        print(65665)
                        break
                    elif datetime.datetime.now().second==0:
                        try:
                            print(5555)
                            print(self.symbol, self.timeframe)
                            if self.fxcm_instance.connection==None:
                                fxcm_reconnect()
                            self.fxcm_instance.get_price_data(self.symbol, self.timeframe)
                            self.db=Db_Controller()
                            self.data=self.db.query_price_data(self.symbol, self.timeframe, self.quantity)
                            print(self.data)
                            print(8888)
                            self.check_condition()
                            print(9999)
                            self.shared_memory_dict['strategy_status']='Running'
                            print(1010101)
                        except Exception as e:
                            print(2222)
                            print(e)
                            self.shared_memory_dict['strategy_status']='Connection issue'
                            print(3333)
                            fxcm_reconnect()
                            print(4444)
                    time.sleep(0.3)
                except Exception as e:
                    print(e)
                    self.shared_memory_dict['strategy_status']='Connection issue'
                    time.sleep(0.3)
            print(222222222222222222222222)
            print(33333333333333333333333)
        except Exception as e:
            print(e)

    def stop(self):
        print('wwww')
        if self.shared_memory_dict['stop_signal']==False:
            print('eeee')
            last_stop=str(datetime.datetime.now())
            self.shared_memory_dict['stop_signal']=True
            self.shared_memory_dict['strategy_status']='Stopped'
            self.shared_memory_dict['last_stop']=last_stop

            print('vvvv')

    def delete(self):
        print('xxxx')
        if self.is_alive():
            self.stop()
            print('oooo')

    def process_status(self):
        return self.is_alive()

