
import sys

sys.path.append(r'\Users\jimhu\option_trader\src')


import os
import math
import json
import sqlite3
import logging
import pandas as pd
import numpy as np
from datetime import time, date, datetime, timedelta
from pytz import timezone
import uuid as UUID


from option_trader.settings import app_settings  as settings    
from option_trader.settings.trade_config import entryCrit, riskManager, runtimeConfig, marketCondition
from option_trader.settings import schema as schema  
from option_trader.consts import asset
from option_trader.settings import app_settings
from option_trader.consts import strategy as st

from option_trader.admin import position_summary
from option_trader.admin import position
from option_trader.admin import transaction
from option_trader.admin import quote

from option_trader.utils.data_getter import pick_option_long, pick_option_short, afterHours
from option_trader.utils.data_getter import get_price_history,get_option_leg_details 
from option_trader.utils.data_getter import pick_vertical_call_spreads, pick_vertical_put_spreads
from option_trader.utils.data_getter import pick_call_butterfly, pick_put_butterfly, pick_iron_butterfly
from option_trader.utils.data_getter import pick_iron_condor, get_next_earning_date, get_option_exp_date
from option_trader.utils.predictor  import  predict_price_range


from option_trader.settings import app_settings    


from option_trader.utils.calc_prob import calc_win_prob

account_profile_schema = "user_name TEXT, account_name TEXT NOT NULL PRIMARY KEY,equaty_percentage REAL,\
        available_to_trade REAL,available_to_trade_wo_margin REAL,non_margin_buy_power REAL,\
        margin_buy_power REAL,available_to_withdraw REAL,cash_only REAL,cash_and_margin REAL,\
        house_surplus REAL,sma REAL,exchange_surplue REAL,cash_core REAL,cash_credit_debit REAL,\
        margin_credit_debit REA,market_value_securities REAL,held_in_cash REAL, held_in_margin REAL,\
        cash_buy_power REAL,settled_cash REAL,initial_balance REAL,risk_mgr TEXT, entry_crit TEXT,\
        market_condition TEXT, runtime_config TEXT, default_strategy_list TEXT, default_watchlist TEXT, default_predictor TEXT,\
        open_date,\
        FOREIGN KEY(user_name) REFERENCES user(name)"   

account_daily_summary_schema = "'Initial Balance' REAL, 'Acct Value' REAL, 'Asset Value' REAL,'Cash' REAL,\
                            'Margin' REAL,'Unrealized PL' REAL,'Realized PL' REAL, 'Risk Ratio' REAL,\
                            'Max Risk' REAL, 'Gain' REAL, 'Trx # (all)' INTEGER, 'Win Rate (all)' REAL,\
                            'Avg Loss (all)' REAL, 'Avg Win (all)' REAL,'Trx# (opened)' INEGER,\
                            'Win Rate (opened)' REAL, 'Avg Loss (opened)' REAL, 'Avg Win (opened)' REAL,\
                            'Trx# (closed)' INTEGER,'Win Rate (closed)' REAL, 'Avg Win (closed)' REAL,\
                            'Avg Loss (closed)' REAL, 'record date' TEXT NOT NULL PRIMARY KEY"

class summary_col_name():
    INIT_BALANCE        = 'Initial Balance'
    ACCT_VALUE          = 'Acct Value'
    ASSET_VALUE         = 'Asset Value'
    CASH                = 'Cash'
    MARGIN              = 'Margin'
    UNREALIZED_PL       = 'Unrealized PL'
    REALIZED_PL         = 'Realized PL'  
    RISK_RATIO          = 'Risk Ratio'
    MAX_RISK            = 'Max Risk'      
    GAIN                = 'Gain'
    ALL_TRX_CNT         = 'Trx # (all)'
    ALL_WIN_RATE         ='Win Rate (all)'    
    AVG_ALL_TRX_LOSS_PL    = 'Avg Loss (all)'
    AVG_ALL_TRX_WIN_PL     = 'Avg Win (all)'
    OPENED_TRX_CNT      = 'Trx# (opened)'
    OPENED_WIN_RATE     = 'Win Rate (opened)'       
    AVG_OPENED_TRX_LOSS_PL = 'Avg Loss (opened)'
    AVG_OPENED_TRX_WIN_PL  = 'Avg Win (opened)'
    CLOSED_TRX_CNT      = 'Trx# (closed)'
    CLOSED_WIN_RATE     = 'Win Rate (closed)'       
    AVG_CLOSED_TRX_WIN_PL = 'Avg Win (closed)'
    AVG_CLOSED_TRX_LOSS_PL = 'Avg Loss (closed)'

class account():

    def __init__(self, 
                 user, 
                 account_name, 
                 initial_balance=app_settings.DEFAULT_ACCOUNT_INITIAL_BALANCE,
                 watchlist=[],
                 strategy_list=[]):        
        
        self.user = user
        self.account_name = account_name        
        self.logger = logging.getLogger(__name__)

        if settings.DATABASES == 'sqlite3':
            try:
                self.db_path = os.path.join(user.user_home_dir,account_name+"_account.db")                
                self.db_conn  = sqlite3.connect(self.db_path)  
                cursor = self.db_conn.cursor()                
                if os.path.exists(self.db_path) :
                    self.db_conn.commit()     
                    self.db_conn  = sqlite3.connect(self.db_path)                     
                    self.strategy_list = self.get_default_strategy_list()             
                    self.watchlist     = self.get_default_watchlist()                                         
                    self.entry_crit = self.get_default_entry_crit()
                    self.risk_mgr = self.get_default_risk_mgr()
                    self.runtime_config = self.get_default_runtime_config()
                    self.market_condition = self.get_default_market_condition()
                    self.initial_balace = self.get_initial_balance()
                    self.cash_position = self.get_cash_position()
                    self.margin_position = self.get_margin_position()                             
                    cursor.execute("DROP TABLE IF EXISTS account_history")                    
                    cursor.execute("CREATE TABLE IF NOT EXISTS account_daily_summary("+account_daily_summary_schema+")")                    
                    self.db_conn.commit()     
                    if self.risk_mgr.schema_updated:
                       self.update_default_risk_mgr(self.risk_mgr)            
                       self.risk_mgr.schema_updated = False
                    return
                else:
                # new account                 
                    try:
                        open_date = str(datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date())         
                        cursor.execute("CREATE TABLE IF NOT EXISTS account_profile("+account_profile_schema+")")                        #cursor.execute("CREATE TABLE IF NOT EXISTS account_history("+account_history_schema+")")                    
                        cursor.execute("CREATE TABLE IF NOT EXISTS account_daily_summary("+account_daily_summary_schema+")")                    
                        cursor.execute("CREATE TABLE IF NOT EXISTS position_summary("+position_summary.schema+")")
                        cursor.execute("CREATE TABLE IF NOT EXISTS position("+position.schema+")")
                        cursor.execute("CREATE TABLE IF NOT EXISTS transactions("+transaction.schema+")")

                        self.strategy_list = user.default_strategy_list if len(strategy_list) == 0 else strategy_list
                        self.watchlist = user.default_watchlist if len(watchlist) == 0 else watchlist

                        self.entry_crit = entryCrit()
                        self.risk_mgr = riskManager()
                        self.runtime_config = runtimeConfig()
                        self.market_condition = marketCondition()
                        sql = "INSERT INTO account_profile (user_name, account_name, initial_balance, default_strategy_list, entry_crit, runtime_config, risk_mgr, market_condition, default_watchlist, open_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"              
                        cursor.execute(sql, [user.user_name, 
                                            account_name, 
                                            initial_balance,
                                            json.dumps(self.strategy_list),
                                            json.dumps(vars(entryCrit())),
                                            json.dumps(vars(runtimeConfig())),
                                            json.dumps(vars(riskManager())),
                                            json.dumps(vars(marketCondition())),
                                            json.dumps(self.watchlist),
                                            open_date                                     
                                        ])               
                        sql = 'INSERT INTO position (symbol, current_value) VALUES(?,?)' 
                        cursor.execute(sql, [asset.CASH, initial_balance])
                        cursor.execute(sql, [asset.MARGIN, 0])                
                        self.cash_position = initial_balance
                        self.margin_position = 0
                        self.db_conn.commit()       
                    except Exception as e:
                        self.logger.exception(e)
                        import shutil
                        if os.path.exists(self.db_path):
                            shutil.rmtree(self.db_path)                      
                        raise e                        
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('unsupported database engine %s' % settings.DATABASES)

    def __enter__(self):
        return self
  
    def __exit__(self, *args):
        try:
            self.db_conn.close()
        except Exception as ex:
            self.logger.exception(ex)
            raise ex

    def __update_cash_position(self, cash_position, commit=True):
        
        if settings.DATABASES == 'sqlite3':                    
            try:    
                sql = "UPDATE position SET current_value = '"+str(cash_position) + "' WHERE symbol = '"+asset.CASH + "'"                              
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                if commit:
                    self.db_conn.commit()
                return cash_position                
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported DB engine %s' % settings.DATABASES)
            return np.nan
        
    def __update_margin_position(self, margin_position, commit=True):

        if math.isnan(margin_position):
            self.logger.error('Nan margin_position appears!!')
            return np.nan            

        if settings.DATABASES == 'sqlite3':                    
            try:    
                sql = "UPDATE position SET current_value = '"+str(margin_position) + "' WHERE symbol = '"+asset.MARGIN + "'"                              
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                if commit:
                    self.db_conn.commit()      
                return margin_position    
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported DB engine %s' % settings.DATABASES)
            return np.nan
                    
    def get_initial_balance(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT initial_balance FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return cursor.fetchone()[0]                   
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_open_date(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT open_date FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return cursor.fetchone()[0]                  
            except Exception as e:
                #self.logger.exception(e)   
                return None
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_default_strategy_list(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT default_strategy_list FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return json.loads(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_default_watchlist(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT default_watchlist FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return json.loads(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def update_default_strategy_list(self, strategy_list):
        if settings.DATABASES == 'sqlite3':
            try:
                sql = "UPDATE account_profile SET default_strategy_list='"+json.dumps(strategy_list)+"' WHERE account_name='"+self.account_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()      
                self.strategy_list = strategy_list                    
            except Exception as e:
                self.logger.exception(e)       
                raise e
        else:
            self.logger.error('unsupported database engine %s' % settings.DATABASES)

    def update_default_watchlist(self, watchlist):
        if settings.DATABASES == 'sqlite3':
            try:
                sql = "UPDATE account_profile SET default_watchlist='"+json.dumps(watchlist)+"' WHERE account_name='"+self.account_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()      
                self.watchlist = watchlist                    
            except Exception as e:
                self.logger.exception(e)       
                raise e
        else:
            self.logger.error('unsupported database engine %s' % settings.DATABASES)

    def get_default_entry_crit(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT entry_crit FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return entryCrit(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def get_default_entry_crit(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT entry_crit FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return entryCrit(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None
    
    def update_default_entry_crit(self, entry_crit):

        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "UPDATE account_profile SET entry_crit='"+json.dumps(vars(entry_crit))+"' WHERE account_name='"+self.account_name+"'"                                 
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)          
                self.db_conn.commit()                     
                self.entry_crit = entry_crit 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None
    
    def get_default_runtime_config(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT runtime_config FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return runtimeConfig(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def update_default_runtime_config(self, runtime_config):

        self.runtime_config = runtime_config
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "UPDATE account_profile SET runtime_config='"+json.dumps(vars(runtime_config))+"' WHERE account_name='"+self.account_name+"'"                                 
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)                
                self.db_conn.commit()
                self.runtime_config = runtime_config
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def get_default_risk_mgr(self):

        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT risk_mgr FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return riskManager(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def update_default_risk_mgr(self, risk_mgr):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "UPDATE account_profile SET risk_mgr='"+json.dumps(vars(risk_mgr))+"' WHERE account_name='"+self.account_name+"'"                                 
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)          
                self.db_conn.commit()
                self.risk_mgr = risk_mgr      
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None
    
    def get_default_market_condition(self):

        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT market_condition FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return marketCondition(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def update_default_market_condition(self, market_condition):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "UPDATE account_profile SET market_condition='"+json.dumps(vars(market_condition))+"' WHERE account_name='"+self.account_name+"'"                                 
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)       
                self.db_conn.commit()
                self.market_condition = market_condition         
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None
            
    def get_cash_position(self):

        if settings.DATABASES == 'sqlite3':                    
            try:    
                sql = "SELECT current_value FROM position WHERE symbol = '"+asset.CASH+"'"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return float(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported DB engine %s' % settings.DATABASES)
            return np.nan
                                                        
    def get_margin_position(self):
        if settings.DATABASES == 'sqlite3':                    
            try:    
                sql = "SELECT current_value FROM position WHERE symbol = '"+asset.MARGIN + "'"
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return float(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported DB engine %s' % settings.DATABASES)
            return np.nan
    
    def get_asset_value(self):
        pos = self.get_positions()
        open_pos = pos[pos[position.STATUS]==asset.OPENED]      
        bto_df = open_pos[open_pos[position.OPEN_ACTION] == asset.BUY_TO_OPEN]
        sto_df = open_pos[open_pos[position.OPEN_ACTION] == asset.SELL_TO_OPEN]
        asset_value = bto_df[position.CURRENT_VALUE].sum() - sto_df[position.CURRENT_VALUE].sum()
        return asset_value
        
    def get_pl(self):
        ps = self.get_position_summary()
        unreliazed_pl = ps[ps[position_summary.STATUS]== asset.OPENED][position_summary.PL].sum()
        realized_pl = ps[ps[position_summary.STATUS] != asset.OPENED][position_summary.PL].sum()
        return round(unreliazed_pl,2) , round(realized_pl,2)
    
    def get_account_value(self):
        return self.get_cash_position()+self.get_margin_position()+self.get_asset_value()

    def get_risk_matrix(self):
        ps = self.get_position_summary()
        ops = ps[ps[position_summary.STATUS]== asset.OPENED]
        ops[position_summary.MAX_RISK] = ops.apply(lambda x: x[position_summary.MAX_LOSS] * x[position_summary.QUANTITY] * 100 if x[position_summary.STRATEGY] != st.UNPAIRED else x[position_summary.OPEN_PRICE], axis = 1)
        max_risk = ops[position_summary.MAX_RISK].sum()
        position_summary
        symbol_risk = ops.groupby([position_summary.SYMBOL]).sum(numeric_only=True)[position_summary.MAX_RISK].to_dict()
        exp_date_risk = ops.groupby([position_summary.EXP_DATE]).sum(numeric_only=True)[position_summary.MAX_RISK].to_dict()
        strategy_risk = ops.groupby([position_summary.STRATEGY]).sum(numeric_only=True)[position_summary.MAX_RISK].to_dict()

        risk_matrix = {position_summary.MAX_RISK:max_risk, 
                       'risk ratio': max_risk/self.get_account_value(), 
                       position_summary.SYMBOL:   symbol_risk,
                       position_summary.EXP_DATE: exp_date_risk,
                       position_summary.STRATEGY: strategy_risk }
        return risk_matrix

    def submit_orders(self):
        # TBD
        return                  

    def create_position(self, symbol, legs, q, uuid_value, trade_date):

        field_names =  "uuid,leg_id,symbol,otype,strike,exp_date,open_action,quantity,open_price,current_value,average_cost_basis,init_delta,init_IV,init_volume,init_open_interest,status,trade_date"

        values =  '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?' 

        legdesc = []
        leg_id = -1
        pos = {}
        for leg in legs:

            otype       =leg[quote.OTYPE]
            if otype == asset.STOCK: # buy write or buy with protected put
                # TO BE FIXED
                open_action =leg[quote.OPEN_ACTION]
                status = asset.OPENED
                quantity = q * 100              
                average_cost_basis = quantity * leg[quote.LAST_PRICE]                  
                current_value = average_cost_basis                
                uuid = uuid_value   
                init_volume = leg[quote.VOLUME]                
 
                fields = [uuid, leg_id, symbol, otype, open_action, quantity, open_price,\
                        current_value, average_cost_basis, init_volume, status, trade_date]
    
                sql = "INSERT INTO position ("+field_names+") VALUES("+values+")" 
                cursor = self.db_conn.cursor()          
                cursor.execute(sql, fields)
                msg = "BTO [%s|%s] [price:%.2f|q:%d] [%s|%s]" %\
                            (symbol, otype, strike, open_price, quantity, 
                             self.user.user_name, self.account_name)
                                
                self.create_transaction(leg, asset.BUY, asset.OPEN)
                continue

            open_action =leg[quote.OPEN_ACTION]
            quantity    =leg[position.SCALE] * q
            strike      =leg[quote.STRIKE]
            exp_date    =leg[quote.EXP_DATE]

            average_cost_basis = quantity * leg[quote.LAST_PRICE]
            if leg[quote.BID] > 0 and leg[quote.ASK] > 0:
                open_price = (leg[quote.BID] + leg[quote.ASK]) / 2
            else:
                open_price = leg[quote.LAST_PRICE]           

            average_cost_basis = 100* quantity * open_price
            current_value = average_cost_basis
            init_delta =  leg[quote.DELTA]
            init_IV =     leg[quote.IMPLIED_VOLATILITY]
            init_volume = leg[quote.VOLUME]
            init_open_interest = leg[quote.OPEN_INTEREST]
            status = asset.OPENED
            uuid = uuid_value            
            leg_id += 1
            fields = [uuid, leg_id, symbol, otype, strike, exp_date, open_action, quantity, open_price,\
                      current_value, average_cost_basis, init_delta, init_IV, init_volume,\
                      init_open_interest, status, trade_date]
            
            sql = "INSERT INTO position ("+field_names+") VALUES("+values+")" 
            cursor = self.db_conn.cursor()          
            cursor.execute(sql, fields)

            leg[position.QUANTITY]  = leg[position.SCALE] * q
            leg[position.OPEN_PRICE]  = leg[position.LAST_PRICE] = open_price  

            if open_action == asset.BUY_TO_OPEN:
                msg = "BTO [%s|%s|%s] [strike:%.2f|price:%.2f|q:%d] [%s|%s]" %\
                            (symbol, otype, exp_date, strike, open_price, quantity, 
                             self.user.user_name, self.account_name)

                self.create_transaction(leg, asset.BUY, asset.OPEN)
            elif open_action == asset.SELL_TO_OPEN:
                msg = "STO [%s|%s|%s] [strike:%.2f|price:%.2f|q:%d] [%s|%s]" %\
                        (symbol, otype, exp_date, strike, open_price, quantity,                
                        self.user.user_name, self.account_name)

                self.create_transaction(leg, asset.SELL, asset.OPEN)                
            else:
                self.logger.error("Invalie open_action %s" % open_action)
                raise Exception("Invalie open_action %s" % open_action)

            self.logger.debug(msg)

            legdesc.append(json.dumps(vars(self.optionLegDesc(exp_date, leg))))

        return  json.dumps(legdesc)
    
    def close_position(self, row):     
        symbol      = row[position.SYMBOL]  
        stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]                
        strike      = row[position.STRIKE]
        otype       = row[position.OTYPE]
        open_action = row[position.OPEN_ACTION]
        open_price  = row[position.OPEN_PRICE]
        quantity    = row[position.QUANTITY]
        exp_date    = row[position.EXP_DATE]

        if otype == asset.CALL:
            last_price = 0 if stock_price <= strike else stock_price - strike 
        elif otype == asset.PUT:
            last_price = 0 if stock_price >= strike else strike - stock_price
        else:
            self.logger.error("Invalie otype %s" % otype)
            return
        gain = (last_price - open_price) if open_action == asset.BUY_TO_OPEN else (open_price-last_price)
        total_gain_loss = gain * quantity  * 100
        total_gain_loss_percent = (gain / open_price) * 100                               
        current_value  = last_price * quantity * 100
                            
        sql = """update position set last_price=?, current_value=?, total_gain_loss=?,\
                total_gain_loss_percent=?, status=? where leg_id ==? and uuid==?"""
        
        data = (last_price, current_value, total_gain_loss, total_gain_loss_percent, asset.CLOSED, row[position.LEG_ID], row[position.UUID])

        row[position.LAST_PRICE] = last_price
        if open_action == asset.BUY_TO_OPEN:
            msg = "[%s|%s] STC [%s|%s|%s|%.2f] [gain:%.2f|q:%d]" % (self.user.user_name, self.account_name,\
                        symbol, otype, exp_date, strike, gain, quantity)            
            self.create_transaction(row, asset.SELL, asset.CLOSE)
        elif open_action == asset.SELL_TO_OPEN:
            msg = "[%s|%s] BTC [%s|%s|%s|%.2f] [gain:%.2f|q:%d]" % (self.user.user_name, self.account_name,\
                        symbol, otype, exp_date, strike, gain, quantity)                                                                                   
            self.create_transaction(row, asset.BUY, asset.CLOSE)            
        else:
            self.logger.error("Invalie open_action %s" % open_action)
            raise Exception("Invalie open_action %s" % open_action)

        cursor = self.db_conn.cursor()       
        cursor.execute(sql, data)                    
        self.db_conn.commit()             
        self.logger.info(msg)
        return
    
    def expire_position(self, row):

        # covered call!!
        if row[position.OTYPE] == asset.STOCK:            
            return row[position.LAST_PRICE]
        
        exp_date = row[position.EXP_DATE]        
        symbol   = row[position.SYMBOL]
        data      = get_price_history(symbol, period='1mo')   
        exp_stock_price = data['Close'][pd.Timestamp(exp_date).tz_localize(data.index[-1].tz)]                     
        strike          = row[position.STRIKE]
        otype           = row[position.OTYPE]
        open_action     = row[position.OPEN_ACTION]
        quantity        = row[position.QUANTITY]
        today = datetime.now(timezone(app_settings.TIMEZONE))        
        last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")    

        if otype == asset.CALL:
            row[position.LAST_PRICE] = 0 if exp_stock_price <= strike else exp_stock_price - strike 
            if open_action == asset.BUY_TO_OPEN:
                gain = row[position.LAST_PRICE]  - row[position.OPEN_PRICE]
            else:
                gain = row[position.OPEN_PRICE]  - row[position.LAST_PRICE]
            row[position.TOTAL_GAIN_LOSS] = gain * row[position.QUANTITY]  * 100
            row[position.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[position.OPEN_PRICE]) * 100                
        elif otype == asset.PUT:
            row[position.LAST_PRICE] = 0 if exp_stock_price >= strike else strike - exp_stock_price
            if open_action == asset.BUY_TO_OPEN:
                gain = row[position.LAST_PRICE] - row[position.OPEN_PRICE]
            else:
                gain = row[position.OPEN_PRICE] - row[position.LAST_PRICE]                  
            row[position.TOTAL_GAIN_LOSS] = gain * row[position.QUANTITY]  * 100
            row[position.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[position.OPEN_PRICE]) * 100                 
        else:
            self.logger.error("Invalie otype %s" % otype)
            return
        
        row[position.CURRENT_VALUE]  = row[position.LAST_PRICE] * row[position.QUANTITY]  * 100
                            
        sql = """update position set last_price=?, current_value=?, total_gain_loss=?,\
                total_gain_loss_percent=?, status=? ,last_quote_date=? where leg_id ==? and uuid==?"""
        
        data = (row[position.LAST_PRICE], row[position.CURRENT_VALUE],row[position.TOTAL_GAIN_LOSS],\
                row[position.TOTAL_GAIN_LOSS_PERCENT], asset.EXPIRED, last_quote_date, row[position.LEG_ID], row[position.UUID])

        if open_action == asset.BUY_TO_OPEN:
            msg = "[%s|%s] EXP L [%s|%s|%s|%.2f] [gain:%.2f|q:%d]" % (self.user.user_name, self.account_name,\
                        symbol, otype, exp_date, strike, gain, quantity)            
            self.create_transaction(row, asset.SELL, asset.CLOSE)
        elif open_action == asset.SELL_TO_OPEN:
            msg = "[%s|%s] EXP S [%s|%s|%s|%.2f] [gain:%.2f|q:%d]" % (self.user.user_name, self.account_name,\
                        symbol, otype, exp_date, strike, gain, quantity)             
            self.create_transaction(row, asset.BUY, asset.CLOSE)            
        else:
            self.logger.error("Invalie open_action %s" % open_action)
            raise Exception("Invalie open_action %s" % open_action)

        cursor = self.db_conn.cursor()       
        cursor.execute(sql, data)                    
        self.db_conn.commit()             
        self.logger.info(msg)
        return row[position.LAST_PRICE]
    
    def update_position(self):
        df = pd.read_sql_query("SELECT * FROM position WHERE status = '"+asset.OPENED+"'", self.db_conn)
        if df.shape[0] == 0:
            return []
               
        today = datetime.now(timezone(app_settings.TIMEZONE))
        last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")            
        symbol_list = df[position.SYMBOL].unique()            
        for symbol in symbol_list:
            stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]                 
            sdf = df[df[position.SYMBOL]==symbol]
            for i, row in sdf.iterrows():         
                row[position.LAST_QUOTE_DATE] = last_quote_date                       
                otype = row[position.OTYPE]
                if otype == asset.STOCK:                    
                    row[position.LAST_PRICE] = stock_price
                    if row[position.OPEN_ACTION] == asset.BUY_TO_OPEN: 
                        gain = (row[position.LAST_PRICE] - row[position.OPEN_PRICE]) 
                        row[position.TOTAL_GAIN_LOSS] = gain * row[position.QUANTITY] * 100 
                        row[position.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[position.OPEN_PRICE]) * 100                
                    else:          
                        gain = (row[position.OPEN_PRICE] - row[position.LAST_PRICE])      
                        row[position.TOTAL_GAIN_LOSS] = gain * row[position.QUANTITY] 
                        row[position.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[position.OPEN_PRICE]) * 100                

                    row[position.CURRENT_VALUE] = row[position.LAST_PRICE] * row[position.QUANTITY] 

                    sql = """update position set last_price=?, current_value=?, total_gain_loss=?,\
                        total_gain_loss_percent=?,last_quote_date=? where symbol ==? and trade_date==? and quantity==? and uuid==?"""
                    data = (row[position.LAST_PRICE], row[position.CURRENT_VALUE],row[position.TOTAL_GAIN_LOSS],\
                            row[position.TOTAL_GAIN_LOSS_PERCENT],row[position.LAST_QUOTE_DATE],\
                            row[position.SYMBOL], row[position.TRADE_DATE], row[position.QUANTITY], row[position.UUID])
                    cursor = self.db_conn.cursor()        
                    cursor.execute(sql, data)
                    self.db_conn.commit()                                                        
                elif otype in [asset.CALL, asset.PUT]:
                    exp_date = row[position.EXP_DATE]
                    days_to_expire = (pd.Timestamp(exp_date).tz_localize(timezone(app_settings.TIMEZONE))-today).days                           
                    if days_to_expire < 0:
                        self.expire_position(row)
                        continue                  
                               
                    strike = row[quote.STRIKE]
                    op = get_option_leg_details(symbol, stock_price, exp_date, strike, otype)
                    if len(op) == 0:
                        self.logger.error('Cannot find quote for option leg %s %s %s %s' % (symbol, otype, str(strike), str(exp_date)))
                        continue
            
                    row[position.LAST_PRICE] = (op[quote.BID]+op[quote.ASK]) / 2  if  (op[quote.BID]+op[quote.ASK]) > 0 else  op[quote.LAST_PRICE]                 
                        
                    row[position.CURRENT_VALUE] = row[position.LAST_PRICE] * row[position.QUANTITY] * 100

                    if row[position.OPEN_ACTION] == asset.BUY_TO_OPEN: 
                        gain = (row[position.LAST_PRICE] - row[position.OPEN_PRICE]) 
                        row[position.TOTAL_GAIN_LOSS] = gain * row[position.QUANTITY] * 100 
                        row[position.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[position.OPEN_PRICE]) * 100                
                    else:          
                        gain = (row[position.OPEN_PRICE] - row[position.LAST_PRICE])      
                        row[position.TOTAL_GAIN_LOSS] = gain * row[position.QUANTITY] 
                        row[position.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[position.OPEN_PRICE]) * 100                
                       
                    row[position.LAST_DELTA] = op[quote.DELTA]
                    row[position.LAST_IV]    = op[quote.IMPLIED_VOLATILITY]
                    row[position.LAST_OPEN_INTEREST] = op[quote.OPEN_INTEREST]   
                    row[position.LAST_VOLUME] = op[quote.VOLUME]               

                    sql = """update position set last_price=?, current_value=?, total_gain_loss=?,\
                        total_gain_loss_percent=?,last_delta=?,last_IV=?,last_open_interest=?,last_volume=?,\
                        last_quote_date=? where leg_id ==? and uuid==?"""
                    
                    data = (row[position.LAST_PRICE], row[position.CURRENT_VALUE],row[position.TOTAL_GAIN_LOSS],\
                            row[position.TOTAL_GAIN_LOSS_PERCENT],row[position.LAST_DELTA],row[position.LAST_IV],\
                            row[position.LAST_OPEN_INTEREST], row[position.LAST_VOLUME], row[position.LAST_QUOTE_DATE],\
                            row[position.LEG_ID],row[position.UUID])
                    
                    cursor = self.db_conn.cursor()        
                    cursor.execute(sql, data)                    
                    self.db_conn.commit()     
                else:
                    self.logger.error('Unahndled %s type position' % otype)          

        return self.update_position_summary()

    def create_position_summary(self, row):
        uuid_value = UUID.uuid4().hex
        symbol =       row[position_summary.SYMBOL]
        exp_date =     row[position_summary.EXP_DATE]
        strategy =     row[position_summary.STRATEGY]
        quantity =     row[position_summary.QUANTITY]
        open_price =   row[position_summary.OPEN_PRICE] 
        breakeven_l =  row[position_summary.BREAKEVEN_L]
        breakeven_h =  row[position_summary.BREAKEVEN_H]
        max_profit =   row[position_summary.MAX_PROFIT]
        max_loss =     row[position_summary.MAX_LOSS]
        pnl =          row[position_summary.PNL]
        win_prob =     row[position_summary.WIN_PROB]
        credit = str(True) if row[position_summary.MARGIN] > 0 else str(False) 
        trade_date =  str(row[position_summary.TRADE_DATE])
        trade_stock_price = row[position_summary.TRADE_STOCK_PRICE]   
        spread =       row[position_summary.SPREAD]         
        target_low  = row[position_summary.TARGET_LOW]
        target_high = row[position_summary.TARGET_HIGH]

        status =      asset.OPENED
        legs =        row[position_summary.LEGS]          
        legs_desc =   self.create_position(symbol, legs, quantity, uuid_value, trade_date)        
        uuid = uuid_value

        df = self.user.site.get_monitor_df(filter=[symbol])
        if df.shape[0] == 1:
            earning_date = df.head(1)['earning'].values[0]
        else:
            try:
                earning_date = get_next_earning_date(symbol)
                earning_date = "" if earning_date == None else str(earning_date)
            except Exception as ex:
                self.logger.exception(ex)
                earning_date = ""
            
        margin = quantity * 100 * row[position_summary.MARGIN]
        cash = quantity * 100 * row[position_summary.OPEN_PRICE]    

        if self.user.site.check_afterhour:
            if afterHours() or self.runtime_config.auto_trade == False:
                msg = "CREATE PENDING [%s|%s|%s] [pri:%.2f|pnl:%.2f|prob:%.2f|q:%d] %s [%s]" %\
                    (strategy, symbol, exp_date, open_price,
                    pnl, win_prob, quantity, self.print_legs(legs_desc),self.account_name)
                self.logger.info(msg)
                return msg
    
        cash_position = self.get_cash_position()
        margin_position = self.get_margin_position()          
        if math.isnan(margin_position):
             margin_position = 0.0

        if math.isnan(margin):
            margin=0.0

        if credit == 'True':        
            margin_position += margin
            cash_position += (cash-margin)            
            self.__update_margin_position(margin_position, commit=False)        
        else:
            cash_position -= cash

        self.__update_cash_position(cash_position, commit=False)  

        last_price = open_price
        pl = 0.0
        gain=0.0
        last_quote_date = trade_date
        last_stock_price = trade_stock_price
        last_win_prob = win_prob

        fields = [uuid, symbol, strategy, credit, spread, open_price, exp_date, breakeven_l,breakeven_h,\
                  max_profit,max_loss,pnl, win_prob,trade_date,earning_date,trade_stock_price,\
                  margin,quantity,status,legs_desc, target_low, target_high, cash, margin, cash_position,\
                  margin_position,\
                  last_price, pl, gain, last_quote_date, last_stock_price, last_win_prob]

        field_names =  "uuid,symbol,strategy,credit,spread,open_price,exp_date,\
                        breakeven_l,breakeven_h,max_profit,max_loss,pnl,win_prob,trade_date,\
                        earning_date,trade_stock_price,margin,quantity,status,legs_desc, target_low, target_high,\
                        open_cash, open_margin, cash_position, margin_position,\
                        last_price, pl, gain, last_quote_date, last_stock_price, last_win_prob"        

        values =  '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?'                      

        sql = "INSERT INTO position_summary ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        self.db_conn.commit()    

        msg = "CREATE [%s|%s|%s] [pri:%.2f|pnl:%.2f|prob:%.2f|q:%d] %s [%s]" %\
              (strategy, symbol, exp_date, open_price, pnl, 
               win_prob, quantity, self.print_legs(legs_desc),self.account_name)

        self.logger.info(msg)

        #lineNotifyMessage( msg, token=self.user.notification_token)    

        return msg
                           
    def expire_position_summary(self, srow):

        today = datetime.now(timezone(app_settings.TIMEZONE))
        last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")   
                
        uuid = srow[position_summary.UUID]

        pdf= pd.read_sql_query("SELECT * FROM position WHERE uuid = '"+uuid+"'", self.db_conn)

        stock_prow = None
        last_price = 0
        for i, prow in pdf.iterrows(): 
            if prow[position.OTYPE] == asset.STOCK:
                stock_prow = prow
                continue
    
            if prow[position.STATUS] == asset.OPENED:
                exp_price = self.expire_position(prow)
            else:                
                exp_price = prow[position.LAST_PRICE] 

            if prow[position.OPEN_ACTION] == asset.BUY_TO_OPEN:
                last_price -= exp_price
            else:
                last_price += exp_price     

        exp_date = srow[position_summary.EXP_DATE]        
        symbol   = srow[position_summary.SYMBOL]
        data = get_price_history(symbol, period='1mo')        
        strategy = srow[position_summary.STRATEGY]
        exp_stock_price = data['Close'][pd.Timestamp(exp_date).tz_localize(data.index[-1].tz)]        
        open_price = srow[position_summary.OPEN_PRICE] 
        credit = srow[position_summary.CREDIT]=='True'
        quantity = srow[position_summary.QUANTITY]
        stop_date = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")
        stop_reason = asset.EXPIRED
        exp_price = stop_price = last_price
        gain = open_price-last_price if credit else last_price-open_price
        pl = gain * quantity * 100
        gain = 100 * (gain / open_price)
        cash = pl
        legs = srow[position_summary.LEGS]
        if credit:             
            margin = srow[position_summary.MARGIN]      
            margin_position = self.get_margin_position() - margin
            cash += margin
            self.__update_margin_position(margin_position, False)  
        else:
            margin_position = self.get_margin_position()             
            margin=0

        cash_position = self.get_cash_position() 
        cash_position += cash
        self.__update_cash_position(cash_position, False)                

        sql = """update position_summary set exp_stock_price=?, exp_price=?, last_price=?, pl=?, gain=?, status=?, stop_date=?, stop_reason=?, stop_price=?,last_quote_date=?, close_cash=?, close_margin=?, cash_position=?, margin_position=? where uuid==?"""        
        data = (exp_stock_price, exp_price, last_price, pl, gain, asset.EXPIRED, stop_date, stop_reason, stop_price,  last_quote_date, cash, margin, cash_position, margin_position,uuid)
        cursor = self.db_conn.cursor()    
        cursor.execute(sql, data)     
        
        msg = "EXPIRE  [%s|%s|%s] [prof:%.2f|gain:%.2f|q:%d] [cash:%.2f|margin:%.2f][cash_position:%.2f|margin_position%.2f] %s [%s] " %\
                        (strategy, symbol,exp_date, pl, gain, quantity, pl, margin, cash_position, margin_position,
                         self.print_legs(legs),self.account_name)

        self.logger.info(msg)                

        #lineNotifyMessage( msg, token=self.user.notification_token)    

        if strategy == st.COVERED_CALL:
            self.expire_covered_call_post_process(stock_prow, exp_date, exp_stock_price)

        self.db_conn.commit()    

        return msg
    
    def roll_position_summary(self, symbol, exp_date, strategy):

        today = datetime.now(timezone(app_settings.TIMEZONE))

        earning_date = get_next_earning_date(symbol)
        if earning_date is not None:
            days_to_earning = (earning_date - today).days               
            if days_to_earning <= self.risk_mgr.close_days_before_expire:
                return ""  

        cash = self.get_cash_position()
        init_balance = self.get_initial_balance()
        cash_ratio = 100 * cash/init_balance
        if cash_ratio < self.risk_mgr.min_cash_percent:
            self.logger.warning('Cash ratio %.2f lower than setting %2f' % (cash_ratio, self.risk_mgr.min_cash_percent))
            return ""

        risk_matrix = self.get_risk_matrix()
        if risk_matrix['risk ratio'] > app_settings.RISK_MGR.max_risk_ratio:
            self.logger.warning('Risk ratio %.2f higher than setting %2f' % (risk_matrix['risk ratio'], self.risk_mgr.max_risk_ratio))
            return ""

        acct_value = self.get_account_value()        

        exp_date_list = [exp_date]

        if strategy   == st.LONG_CALL:
            df = self.roll_option_long( symbol, exp_date_list, asset.CALL)                
        elif strategy == st.LONG_PUT:
            df = self.roll_option_long( symbol, exp_date_list, asset.PUT)
        elif strategy == st.COVERED_CALL:
            df = self.roll_option_short(symbol, exp_date_list, asset.CALL)     
        elif strategy == st.SHORT_PUT:
            df = self.roll_option_short( symbol, exp_date_list, asset.PUT)                       
        elif strategy == st.CREDIT_CALL_SPREAD:
            df = self.roll_vertical_call_spread( symbol, exp_date_list,  credit=True)            
        elif strategy == st.DEBIT_CALL_SPREAD:
            df = self.roll_vertical_call_spread( symbol, exp_date_list, credit=False)                                       
        elif strategy==  st.CREDIT_PUT_SPREAD:
            df = self.roll_vertical_put_spread( symbol, exp_date_list,  credit=True)                     
        elif strategy == st.DEBIT_PUT_SPREAD:
            df = self.roll_vertical_put_spread( symbol, exp_date_list, credit=False)                    
        elif strategy==  st.CREDIT_IRON_CONDOR:
            df = self.roll_iron_condor( symbol, exp_date_list, credit=True)
        elif strategy == st.DEBIT_IRON_CONDOR:
            df = self.roll_iron_condor( symbol, exp_date_list, credit=False)                    
        elif strategy == st.CREDIT_PUT_BUTTERFLY:
            df = self.roll_put_butterfly(symbol, exp_date_list, credit=True)                                              
        elif strategy == st.CREDIT_CALL_BUTTERFLY:
            df = self.roll_call_butterfly( symbol, exp_date_list, credit=True)                                               
        elif strategy == st.DEBIT_PUT_BUTTERFLY:
            df = self.roll_put_butterfly( symbol, exp_date_list, credit=False)                 
        elif strategy == st.DEBIT_CALL_BUTTERFLY:
            df = self.roll_call_butterfly( symbol, exp_date_list, credit=False)      
        elif strategy == st.IRON_BUTTERFLY:
            df = self.roll_iron_butterfly( symbol, exp_date_list, credit=True)                          
        elif strategy == st.REVERSE_IRON_BUTTERFLY:
            df = self.roll_iron_butterfly( symbol, exp_date_list, credit=False)                   
        elif strategy == st.WEEKLY_STOCK_TRADE:
            # don't roll 
            return
        else:
            self.logger.error('Unsupported strategy %s' % strategy)
            return ""
                    
        if df.shape[0] == 0:
            return ""
        
        df.sort_values(by = [position_summary.WIN_PROB, position_summary.PNL], ascending=False, inplace=True)                                          

        opt = df.head(1).to_dict('records')[0]     

        q = self.risk_mgr.max_loss_per_position // (opt[position_summary.MAX_LOSS] * 100)
        if q == 0:
            self.logger.debug('max loss %.2f exceeded max per position risk %.2f' % (opt[position_summary.MAX_LOSS] * 100, self.risk_mgr.max_loss_per_position))
            return ""

        opt[position_summary.QUANTITY] = q

        opt[position_summary.MAX_RISK] = opt[position_summary.MAX_LOSS] * opt[position_summary.QUANTITY] if opt[position_summary.STRATEGY] != st.UNPAIRED else x[position_summary.OPEN_PRICE]

        symbol_risk_list = risk_matrix[position_summary.SYMBOL]

        exp_date_risk_list = risk_matrix[position_summary.EXP_DATE]

        symbol_risk = symbol_risk_list[symbol] if symbol in symbol_risk_list else 0.0
        if symbol_risk + opt[position_summary.MAX_RISK] > acct_value * self.risk_mgr.max_risk_per_asset /100:
            return ""

        exp_risk = exp_date_risk_list[exp_date] if exp_date in exp_date_risk_list else 0.0
        if exp_risk + opt[position_summary.MAX_RISK] > acct_value * self.risk_mgr.max_risk_per_expiration_date / 100:
            return ""
        
        return self.create_position_summary(opt)  
        
    def update_position_summary(self):

        today = datetime.now(timezone(app_settings.TIMEZONE))
        last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")   
        
        sdf = pd.read_sql_query("SELECT * FROM position_summary WHERE status = '"+asset.OPENED+"'", self.db_conn)

        uuid_list = sdf[position_summary.UUID].unique()      

        trade_rec_list = []

        for uuid in uuid_list:       
            
            if uuid == None:
                continue

            srow = sdf[sdf[position_summary.UUID]==uuid].iloc[0]
            symbol = srow[position_summary.SYMBOL]
            stock_price = get_price_history(symbol, period='1d', interval='1d')['Close'][-1]          
            strategy = srow[position_summary.STRATEGY]
            if strategy == st.UNPAIRED:
                open_price = srow[position_summary.OPEN_PRICE]
                last_price = stock_price
                credit = srow[position_summary.CREDIT]=='True'
                quantity = srow[position_summary.QUANTITY]

                gain = open_price - last_price if credit else last_price - open_price            
                pl = gain * quantity
                gain = 100 * (gain / open_price)

                r = self.user.site.get_monitor_rec(symbol)
                if len(r) > 0:
                    target_low  = r['target_low']
                    target_high = r['target_high']
                else:
                    target_low = target_high = np.nan

                # quartly return target
                breakeven_l = last_price +  (last_price * app_settings.TARGET_ANNUAL_RETURN / 100)
                today = datetime.now(timezone(app_settings.TIMEZONE))        
                from dateutil.relativedelta import relativedelta        
                three_mon_rel = relativedelta(months=12)
                target_date = str((today + three_mon_rel).date()) 
                last_win_prob = calc_win_prob(symbol, target_date, st.UNPAIRED, breakeven_l, np.nan)
        
                sql = """update position_summary set last_price=?, pl=?, gain=?, last_quote_date=?, last_stock_price=?, target_low=?, target_high=?, breakeven_l=?, last_win_prob=? where uuid==?"""        
                data = (last_price, pl, gain, last_quote_date, last_price, target_low, target_high, breakeven_l, last_win_prob, uuid)                                
                cursor = self.db_conn.cursor()    
                cursor.execute(sql, data) 
                self.db_conn.commit()   
                continue
        
            exp_date = srow[position_summary.EXP_DATE]
            trade_date = str(srow[position_summary.TRADE_DATE])            

            try:
                days_open = (today-pd.Timestamp(trade_date).tz_convert(timezone(app_settings.TIMEZONE))).days+1
            except Exception as ex:
                days_open = (today-pd.Timestamp(trade_date).tz_localize(timezone(app_settings.TIMEZONE))).days+1
                pass

            days_to_expire = (pd.Timestamp(exp_date).tz_localize(timezone(app_settings.TIMEZONE))-today).days+1                      
            if days_to_expire < 0:  
                self.expire_position_summary(srow)
                continue

            ppdf = pd.read_sql_query("SELECT * FROM position WHERE uuid = '"+uuid+"'", self.db_conn)

            quantity = srow[position_summary.QUANTITY]            

            last_price = 0

            for i, prow in ppdf.iterrows():
                
                if prow[position.OTYPE] == asset.STOCK: #covered call
                    continue

                if prow[position.LAST_PRICE] == None: #canot get quote, give up update
                    last_price = 0
                    break

                scale = prow[position.QUANTITY] / quantity 
                if prow[position.OPEN_ACTION] == asset.BUY_TO_OPEN:
                    last_price -= (scale * prow[position.LAST_PRICE])
                else:
                    last_price += (scale * prow[position.LAST_PRICE])

            credit = srow[position_summary.CREDIT] == 'True'

            if (credit) and (last_price <= 0):
                continue
            
            if (credit == False) and (last_price >= 0):
                continue

            last_price = abs(last_price)
            
            win_prob = calc_win_prob(symbol, exp_date, strategy, srow[position_summary.BREAKEVEN_L], srow[position_summary.BREAKEVEN_H])

            open_price = abs(srow[position_summary.OPEN_PRICE]) 
            credit = srow[position_summary.CREDIT]=='True'
            quantity = srow[position_summary.QUANTITY]
            legs = srow[position_summary.LEGS]

            gain = open_price - last_price if credit else last_price - open_price            
            pl = gain * quantity * 100
            gain = 100 * (gain / open_price)
            sql = """update position_summary set last_price=?, pl=?, gain=?, last_quote_date=?, last_stock_price=?, last_win_prob=? where uuid==?"""        
            data = (last_price, pl, gain, last_quote_date, stock_price, win_prob, uuid)
            cursor = self.db_conn.cursor()    
            cursor.execute(sql, data)     
            self.db_conn.commit()  

            stopped = False
            roll = False
            if gain >= self.risk_mgr.stop_gain_percent:
                stopped = True
                stop_reason = 'Stop Gain %.2f >= %.2f'% (gain, self.risk_mgr.stop_gain_percent)            
                if days_to_expire > 5:
                    roll = True
            elif gain < 0 and abs(gain) >= self.risk_mgr.stop_loss_percent:
                stopped = True            
                stop_reason =  'Stop Loss %.2f >= %.2f'  % (gain, self.risk_mgr.stop_loss_percent)    
                if days_to_expire > 5:
                    roll = True
            elif days_to_expire <= self.risk_mgr.close_days_before_expire:
                stopped = True   
                stop_reason = 'Days to expire %d <= %d' % (days_to_expire, self.risk_mgr.close_days_before_expire)            
            elif win_prob < 10:
                stopped = True   
                stop_reason = 'Last Win Prob %.2f <= 10' % (win_prob)                          
            else:
                try:
                    datetime.fromisoformat(srow[position_summary.EARNING_DATE])
                    earning_date = pd.Timestamp(srow[position_summary.EARNING_DATE]).tz_convert(timezone(app_settings.TIMEZONE))                 

                    days_to_earning = (earning_date - today).days+1               
                    if days_to_earning <= self.risk_mgr.close_days_before_expire:
                        stopped = True                           
                        stop_reason = 'Days to earning %d <= %d'  % (days_to_earning, self.risk_mgr.close_days_before_expire)    
                except ValueError:
                     pass                   
                                             
            if stopped:              

                if afterHours() or self.runtime_config.auto_trade == False:
                    msg = "STOP PENDING  [%s|%s|%s] [days opened %d|reason:%s|pl:%.2f|gain:%.2f|q:%d] %s [%s]" %\
                            (strategy, symbol,exp_date, days_open,stop_reason,
                             pl, gain, quantity, self.print_legs(legs),self.account_name)
                    self.logger.info(msg)             
                    #lineNotifyMessage( msg, token=self.user.notification_token)   

                    trade_rec_list.append(msg)                    
                else:

                    for i, prow in ppdf.iterrows():
                        self.close_position(prow)

                    if credit:             
                        margin =  srow[position_summary.MARGIN]      
                        margin_position = self.get_margin_position() - margin
                        cash = pl+margin
                        self.__update_margin_position(margin_position, commit=False)  
                    else:
                        cash = pl
                        margin_position = self.get_margin_position()                         
                        margin=0

                    cash_position = self.get_cash_position() + cash  

                    self.__update_cash_position(cash_position, commit=False) 
                    last_quote_date = stop_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")
                    sql = """update position_summary set last_price=?, pl=?, gain=?, last_quote_date=?, stop_date=?, stop_reason=?, status=?, last_stock_price=?, close_cash=?, close_margin=?, cash_position=?, margin_position=? where uuid==?"""        
                    data = (last_price, pl, gain, last_quote_date, stop_date, stop_reason, asset.CLOSED, stock_price, cash, margin, cash_position, margin_position, uuid)                                
                    cursor = self.db_conn.cursor()    
                    cursor.execute(sql, data)     
                    self.db_conn.commit()   
                    msg = "STOP  [%s|%s|%s] [open days %d|reason:%s|pl:%.2f|gain:%.2f|q:%d] [cash:%.2f|margin:%.2f][cash_position:%.2f|margin_position%.2f] %s [%s]" %\
                             (strategy, symbol, exp_date, days_open, stop_reason, pl, gain, quantity, pl, margin, cash_position, margin_position, 
                              self.print_legs(legs),self.account_name)   
                    
                    self.logger.info(msg)             
                    #lineNotifyMessage( msg, token=self.user.notification_token)            

                    trade_rec_list.append(msg)

                    roll_msg = ''
                    if roll:            
                        roll_msg_list = self.roll_position_summary(symbol, exp_date, strategy)                    
                        trade_rec_list += roll_msg_list

        return trade_rec_list

    def print_legs(self, leg_list):
        output_str = ''
    
        legs = json.loads(leg_list)

        for leg in legs:
            ld = json.loads(leg)
            leg_desc = ' [%s|%s|%.2f|%.2f|%d|%s] ' % (ld['OPEN_ACTION'], ld['OTYPE'], ld['STRIKE'], ld['PRICE'], ld['QUANTITY'], ld['EXP_DATE'])
            output_str += leg_desc
    
        return output_str
    
    def get_position_summary(self, status=None, get_leg_dedail=True):    

        if settings.DATABASES == 'sqlite3':             

            df = pd.read_sql_query("SELECT * FROM position_summary", self.db_conn)   

            if status != None:
                df = df[df[position_summary.STATUS] == status]

            if get_leg_dedail:
                for i, row in df.iterrows():                    
                    if row[position_summary.LEGS] == None:
                        continue

                    index = 0                
                    legs = json.loads(row[position_summary.LEGS])    
                    for leg in legs:
                        index += 1                    
                        leg_desc = json.loads(leg)
                        df.at[i, 'leg '+ str(index) + ' otype']       = leg_desc['OTYPE']
                        df.at[i, 'leg '+ str(index) + ' strike']      = leg_desc['STRIKE']
                        df.at[i, 'leg '+ str(index) + ' exp_date']    = leg_desc['EXP_DATE']
                        df.at[i, 'leg '+ str(index) + ' open_action'] = leg_desc['OPEN_ACTION']
                        df.at[i, 'leg '+ str(index) + ' quantity']    = leg_desc['QUANTITY']                                       
                        df.at[i, 'leg '+ str(index) + ' price']       = leg_desc['PRICE']                             
                        if 'IV' in leg_desc:
                            df.at[i, 'leg '+ str(index) + ' IV']       = leg_desc['IV']                              
                        else:
                            df.at[i, 'leg '+ str(index) + ' IV']       = None                                                         

                        if 'DELTA' in leg_desc:
                            df.at[i, 'leg '+ str(index) + ' delta']    = leg_desc['DELTA']        
                        else: 
                            df.at[i, 'leg '+ str(index) + ' delta']    = None      

                        if 'OPEN_INTEREST' in leg_desc:
                            df.at[i, 'leg '+ str(index) + ' open_interest']   = leg_desc['OPEN_INTEREST'] 
                        else:
                            df.at[i, 'leg '+ str(index) + ' open_interest']   = None
            return df
        
        else:
            self.logger.error('Unsupported database engine %s' % settings.DATABASES)    
            return pd.DataFrame()
        
    def get_account_profile(self):
        if settings.DATABASES == 'sqlite3':             
            df = pd.read_sql_query("SELECT * FROM account_profile", self.db_conn)   
            return df         
        else:
            self.logger.error('Unsupported database engine %s' % settings.DATABASES)    
            return pd.DataFrame()
           
    def get_positions(self):    
        if settings.DATABASES == 'sqlite3':             
            df = pd.read_sql_query("SELECT * FROM position", self.db_conn)   
            return df            
        else:
            self.logger.error('Unsupported database engine %s' % settings.DATABASES)    
            return pd.DataFrame()
                     
    def get_transactions(self):   
        if settings.DATABASES == 'sqlite3':             
            df = pd.read_sql_query("SELECT * FROM transactions", self.db_conn)   
            return df
        else:
            self.logger.error('Unsupported database engine %s' % settings.DATABASES)    
            return pd.DataFrame()        

    def weekly_stock_play(self):
        
        if settings.DATABASES == 'sqlite3':              

            amount = self.risk_mgr.weekly_stock_trade_amount                       

            stop_percent = self.risk_mgr.weekly_stock_trade_stop_percent

            init_balance = self.get_initial_balance()

            cash_balance = self.get_cash_position()

            if cash_balance < (stop_percent / 100)  * init_balance:
                self.logger.info('cash low than %.2f %%' % stop_percent) 
                return []     

            watchlist = self.get_default_watchlist()
            if len(watchlist) == 0:
                self.logger.info('Empty watchlist!!') 
                return []
                           
            candidates = self.user.site.get_monitor_df(filter=watchlist)[['symbol', '10d change%']]
            candidates.sort_values('10d change%', inplace=True)
            symbol = candidates.head(1).symbol.values[0]

            quote = get_price_history(symbol, period='1d')

            stock_price = quote['Close'][-1]

            q = amount // stock_price

            if q <= 0:
                return []
            
            trade_rec = self.create_stockSummary(symbol, quote, q)  
            
        return trade_rec

    def get_stock_open_shares(self, symbol):
        pos = self.get_position_summary()
        
        pos = pos[(pos[position_summary.SYMBOL]==symbol) & (pos[position_summary.STATUS]==asset.OPENED) & (pos[position_summary.STRATEGY]==st.UNPAIRED)]
        if pos.shape[0] > 0:
            shares = pos[position.QUANTITY].sum()
            return shares
        else:
            return 0.0

    def get_account_history(self):
        if settings.DATABASES == 'sqlite3':             
            df = pd.read_sql_query("SELECT * FROM account_daily_summary", self.db_conn)   
            return df
        
    def create_daily_account_summary(self): 

        record_date = str(datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date())         

        s = self.get_account_summary()

        field_names =   "'Initial Balance', 'Acct Value', 'Asset Value','Cash','Margin',\
                        'Unrealized PL','Realized PL', 'Risk Ratio','Max Risk', 'Gain',\
                        'Trx # (all)', 'Win Rate (all)','Avg Loss (all)', 'Avg Win (all)','Trx# (opened)',\
                        'Win Rate (opened)', 'Avg Loss (opened)', 'Avg Win (opened)','Trx# (closed)','Win Rate (closed)',\
                        'Avg Win (closed)', 'Avg Loss (closed)', 'record date'"

        values =  '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?' 

        cl = summary_col_name

        fields = [s[cl.INIT_BALANCE], s[cl.ACCT_VALUE], s[cl.ASSET_VALUE], s[cl.CASH], s[cl.MARGIN],\
                  s[cl.UNREALIZED_PL], s[cl.REALIZED_PL], s[cl.RISK_RATIO], s[cl.MAX_RISK], s[cl.GAIN],\
                  s[cl.ALL_TRX_CNT], s[cl.ALL_WIN_RATE], s[cl.AVG_ALL_TRX_LOSS_PL], s[cl.AVG_CLOSED_TRX_WIN_PL], s[cl.OPENED_TRX_CNT],\
                  s[cl.OPENED_WIN_RATE], s[cl.AVG_OPENED_TRX_LOSS_PL], s[cl.AVG_OPENED_TRX_WIN_PL], s[cl.CLOSED_TRX_CNT],s[cl.CLOSED_WIN_RATE],\
                  s[cl.AVG_CLOSED_TRX_WIN_PL], s[cl.AVG_CLOSED_TRX_LOSS_PL], record_date]  
        
        sql = "INSERT OR REPLACE INTO  account_daily_summary ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        self.db_conn.commit()    

        return pd.DataFrame([s])
    
    def create_daily_account_summary_xxx(self): 

        record_date = str(datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date())         
        opt = self.get_position_summary()
        pos = self.get_positions()
        trx = self.get_transactions()
        cash_position = self.get_cash_position()
        margin_position = self.get_margin_position()

        open_pos = pos[pos[position.STATUS]==asset.OPENED] 

        bto_df = open_pos[open_pos[position.OPEN_ACTION] == asset.BUY_TO_OPEN]
        sto_df = open_pos[open_pos[position.OPEN_ACTION] == asset.SELL_TO_OPEN]
        asset_value = bto_df[position.CURRENT_VALUE].sum() - sto_df[position.CURRENT_VALUE].sum()

        account_value = cash_position + margin_position + asset_value        
        position_summary_count = opt.shape[0]
        position_summary_open_count = opt[opt[position_summary.STATUS]==asset.OPENED].shape[0]
        position_summary_stop_count = opt[opt[position_summary.STATUS]==asset.CLOSED].shape[0]
        position_summary_expired_count = opt[opt[position_summary.STATUS]==asset.EXPIRED].shape[0]
        position_count = pos.shape[0]-2 # dont count cash and margin record
        position_open_count = pos[pos[position.STATUS]==asset.OPENED].shape[0]
        trx_count = trx.shape[0]

        PL = account_value - self.get_initial_balance()

        field_names =  "'summary count', 'summary open count',\
                        'summary stop count', 'summary expired count',\
                        'position count', 'position open count', 'trx count',\
                        'cash position', 'margin position', 'Profit/Loss', 'asset value',\
                        'account value', 'record date'"

        values =  '?,?,?,?,?,?,?,?,?,?,?,?,?' 

        fields = [position_summary_count, position_summary_open_count,\
                position_summary_stop_count, position_summary_expired_count,\
                position_count, position_open_count, trx_count,\
                cash_position, margin_position, PL, asset_value, account_value, record_date]    
        
        sql = "INSERT OR REPLACE INTO  account_history ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        self.db_conn.commit()    

    def expire_covered_call_post_process(self, spos, exp_date, last_stock_price):
        
        symbol = spos[position.SYMBOL]
        
        uuid = spos[position.UUID] + '||' + UUID.uuid4().hex

        trade_date = spos[position.TRADE_DATE] 
        status = asset.OPENED           
        trade_stock_price  = open_price = spos[position.OPEN_PRICE]    
                         
        earning_date = get_next_earning_date(symbol)
        earning_date = "" if earning_date == None else str(earning_date)
        credit =  str(False)
        strategy = st.UNPAIRED                    
        cash = 0.0
        margin = 0.0

        cash_position = self.get_cash_position()
        margin_position = self.get_margin_position()
        quantity =  spos[position.QUANTITY]        
        pl = (last_stock_price-open_price) * quantity 
        gain = 100 * (last_stock_price-open_price)/open_price 
        last_quote_date =exp_date        

        fields = [ uuid, symbol, strategy, credit, open_price,\
                  trade_date,earning_date,trade_stock_price,quantity,status,\
                  cash, margin, cash_position, margin_position,\
                  last_stock_price, pl, gain, last_quote_date, last_stock_price]

        field_names =  "uuid,symbol,strategy,credit,open_price,\
                        trade_date,earning_date,trade_stock_price,quantity,status,\
                        open_cash, open_margin, cash_position, margin_position,\
                        last_price, pl, gain, last_quote_date, last_stock_price"
        
        values = '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?'

        sql = "INSERT INTO position_summary ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        msg = "Unpair Expired Covered Call Stock Position %s [price:%.2f|quantity:%d] %s" %\
             (symbol, open_price, quantity,self.account_name)
        self.logger.info(msg)   
        return msg

    def create_stockSummary(self, symbol, quote, quantity):
        
        uuid = UUID.uuid4().hex
        trade_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date() 
        open_action =asset.BUY_TO_OPEN
        status = asset.OPENED           
        price = quote['Close'][-1]
        volume = float(quote['Volume'][-1])
        open_price = price   
        average_cost_basis = quantity * price                 
        current_value = average_cost_basis                          
        otype = asset.STOCK
        open_action = asset.BUY_TO_OPEN        
        leg_id = 0

        if afterHours() or self.runtime_config.auto_trade == False:
            msg = "BUY PENDING %s [price:%.2f|quantity:%d] %s" % (symbol,open_price,quantity,self.account_name)
            self.logger.info(msg)
            return msg
        
        r = self.user.site.get_monitor_rec(symbol)
        target_low  = r['target_low']
        target_high = r['target_high']
                
        breakeven_l = open_price +  (open_price * app_settings.TARGET_ANNUAL_RETURN / 100)
        today = datetime.now(timezone(app_settings.TIMEZONE))        
        from dateutil.relativedelta import relativedelta        
        three_mon_rel = relativedelta(months=12)
        target_date = str((today + three_mon_rel).date()) 
        win_prob = calc_win_prob(symbol, target_date, st.UNPAIRED, breakeven_l, np.nan)
   
        # Insert position record
        field_names =  "uuid, leg_id, symbol, otype, open_action,\
                        quantity,open_price,current_value,average_cost_basis,status,\
                        trade_date, init_volume"
        
        values =  '?,?,?,?,?,?,?,?,?,?,?,?' 

        fields = [uuid, leg_id, symbol, otype, open_action,\
                 quantity, open_price, current_value, average_cost_basis,status,\
                 trade_date, volume]    
        
        sql = "INSERT INTO position ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)

        trx_time = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")     
        amount = quantity * price       
        commission = 0
        fee = 0
        field_names =  "trx_time,symbol,otype,open_close,buy_sell,quantity,price,commission,fee,amount"
        values =  '?,?,?,?,?,?,?,?,?,?' 
        fields = [trx_time, symbol, otype, asset.OPEN, asset.BUY, quantity,\
                  price, commission, fee, amount]
        sql = "INSERT INTO transactions ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)

        earning_date = get_next_earning_date(symbol)
        earning_date = "" if earning_date == None else str(earning_date)
        trade_stock_price = price  
        credit =  str(False)
        strategy = st.UNPAIRED                    

        cash = price * quantity
        margin = 0.0

        cash_position = self.get_cash_position()
        cash_position -= cash
        self.__update_cash_position(cash_position, commit=False)  

        margin_position = self.get_margin_position()
        if math.isnan(margin_position):
            margin_position = 0.0

        last_price=open_price
        pl = 0.0
        gain = 0.0
        last_quote_date=trade_date
        last_stock_price = trade_stock_price

        fields = [ uuid, symbol, strategy, credit, open_price,\
                  trade_date,earning_date,trade_stock_price,quantity,status,\
                  cash, margin, cash_position, margin_position,\
                  last_price, pl, gain, last_quote_date, last_stock_price, target_low, target_high,\
                  breakeven_l, win_prob]

        field_names =  "uuid,symbol,strategy,credit,open_price,\
                        trade_date,earning_date,trade_stock_price,quantity,status,\
                        open_cash, open_margin, cash_position, margin_position,\
                        last_price, pl, gain, last_quote_date, last_stock_price,\
                        target_low, target_high, breakeven_l, win_prob"
        
        values = '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?'

        sql = "INSERT INTO position_summary ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        self.db_conn.commit()    
        msg = "BUY %s [price:%.2f|quantity:%d] %s" %\
             (symbol,open_price,quantity,self.account_name)
        self.logger.info(msg)   
        return msg

    def open_new_strategy_positions(self, watchlist=[], strategy_list=[]):
        
        #if afterHours():
        #    self.logger.info('No trade after hours')
        #    return []
        
        if settings.DATABASES == 'sqlite3':                         
               
            watchlist = watchlist if len(watchlist) > 0 else self.get_default_watchlist()
 
            strategy_list = strategy_list if len(strategy_list) > 0 else self.get_default_strategy_list()

            return self.trade_strategy(watchlist, strategy_list)
 
    def check_earning_date(self, watchlist):

        today = datetime.now(timezone(app_settings.TIMEZONE))        
        new_list = []
        for symbol in watchlist:

            df = self.user.site.get_monitor_df(filter=[symbol])
            if df.shape[0] == 1:
                earning = df.head(1)['earning'].values[0]
                if earning != "":
                    earning_date  = pd.Timestamp(earning).tz_localize(timezone(app_settings.TIMEZONE))                     
                else:
                    earning_date = None
            else:
                try:
                    earning_date = get_next_earning_date(symbol)
                except Exception as ex:
                    self.logger.exception(ex)
                    self.logger.info('%s earning date %s today %s' % (symbol, str(earning_date), str(today)))
                    continue        

            if earning_date is not None:
                days_to_earning = (earning_date - today).days               
                if days_to_earning <= self.risk_mgr.close_days_before_expire:
                    continue
                
            new_list.append(symbol)

        return new_list   

    def get_option_candidates(self, watchlist = [], strategy_list = []):

        watchlist = watchlist if len(watchlist) > 0 else self.get_default_watchlist()
 
        strategy_list = strategy_list if len(strategy_list) > 0 else self.get_default_strategy_list()

        self.mdf = self.get_position_summary(get_leg_dedail=False)     

        candidates = pd.DataFrame()  # one per symbol        
        for strategy in strategy_list:
            if strategy   == st.LONG_CALL:
                df = self.pick_option_long( watchlist, asset.CALL)                
            elif strategy == st.LONG_PUT:
                df = self.pick_option_long( watchlist, asset.PUT)
            elif strategy == st.COVERED_CALL:
                df = self.pick_option_short( watchlist, asset.CALL)     
            elif strategy == st.SHORT_PUT:
                df = self.pick_option_short( watchlist, asset.PUT)                       
            elif strategy == st.CREDIT_CALL_SPREAD:
                df = self.pick_vertical_call_spread( watchlist, credit=True)            
            elif strategy == st.DEBIT_CALL_SPREAD:
                df = self.pick_vertical_call_spread( watchlist, credit=False)                                       
            elif strategy==  st.CREDIT_PUT_SPREAD:
                df = self.pick_vertical_put_spread( watchlist, credit=True)                     
            elif strategy == st.DEBIT_PUT_SPREAD:
                df = self.pick_vertical_put_spread( watchlist, credit=False)                    
            elif strategy==  st.CREDIT_IRON_CONDOR:
                df = self.pick_iron_condor( watchlist, credit=True)
            elif strategy == st.DEBIT_IRON_CONDOR:
                df = self.pick_iron_condor( watchlist, credit=False)                    
            elif strategy == st.CREDIT_PUT_BUTTERFLY:
                df = self.pick_put_butterfly( watchlist, credit=True)                                              
            elif strategy == st.CREDIT_CALL_BUTTERFLY:
                df = self.pick_call_butterfly( watchlist, credit=True)                                               
            elif strategy == st.DEBIT_PUT_BUTTERFLY:
                df = self.pick_put_butterfly( watchlist, credit=False)                 
            elif strategy == st.DEBIT_CALL_BUTTERFLY:
                df = self.pick_call_butterfly( watchlist, credit=False)      
            elif strategy == st.IRON_BUTTERFLY:
                df = self.pick_iron_butterfly( watchlist, credit=True)                          
            elif strategy == st.REVERSE_IRON_BUTTERFLY:
                df = self.pick_iron_butterfly( watchlist, credit=False)                                   
            elif strategy == st.WEEKLY_STOCK_TRADE:
                continue
            else:
                self.logger.error('Unsupported strategy %s' % strategy)
                continue                   

            self.logger.info('%s get %d candidates' %(strategy, df.shape[0]))

            candidates = pd.concat([candidates, df])      

        if candidates.shape[0] > 0:
            candidates.sort_values([position_summary.WIN_PROB, position_summary.PNL],  ascending=False, inplace=True)                                                

            candidates[position_summary.QUANTITY] = candidates.apply(lambda x: self.risk_mgr.max_loss_per_position//(100*x[position_summary.MAX_LOSS]) if x[position_summary.STRATEGY] != st.UNPAIRED else self.risk_mgr.max_loss_per_position/x[position_summary.MAX_LOSS], axis = 1)  
        
            candidates = candidates[candidates[position_summary.QUANTITY] > 0]

            candidates.drop_duplicates(subset=[position_summary.SYMBOL, position_summary.STRATEGY, position_summary.EXP_DATE], inplace=True)

            df = self.get_position_summary(get_leg_dedail=False, status=asset.OPENED)  

            candidates = candidates.merge(df.drop_duplicates(), on=[position_summary.SYMBOL,position_summary.STRATEGY, position_summary.EXP_DATE], how='left', suffixes=('', '_to_be_deleted'), indicator=True)

            candidates[candidates['_merge'] == 'left_only']

            candidates[position_summary.MAX_RISK] = candidates.apply(lambda x: x[position_summary.MAX_LOSS] * x[position_summary.QUANTITY] * 100 if x[position_summary.STRATEGY] != st.UNPAIRED else x[position_summary.OPEN_PRICE] * x[position_summary.QUANTITY], axis = 1)  

            monitor_df = self.user.site.get_monitor_df(filter=watchlist)

            candidates = candidates.merge(monitor_df, on=[position_summary.SYMBOL], how='left', suffixes=('', '_to_be_deleted'))

            candidates.drop(list(candidates.filter(regex='_to_be_deleted|_merge')), axis=1, inplace=True)

        return candidates

    def trade_strategy(self, watchlist=[], strategy_list=[]):   

        watchlist = watchlist if len(watchlist) > 0 else self.get_default_watchlist() 
        strategy_list = strategy_list if len(strategy_list) > 0 else self.get_default_strategy_list()
        
        cash = self.get_cash_position()
        init_balance = self.get_initial_balance()
        cash_ratio = 100 * cash/init_balance
        if cash_ratio < self.risk_mgr.min_cash_percent:
            self.logger.warning('Cash ratio %.2f lower than setting %2f' % (cash_ratio, self.risk_mgr.min_cash_percent))
            return []

        risk_matrix = self.get_risk_matrix()
        if risk_matrix['risk ratio'] > app_settings.RISK_MGR.max_risk_ratio:
            self.logger.warning('Risk ratio %.2f higher than setting %2f' % (risk_matrix['risk ratio'], self.risk_mgr.max_risk_ratio))
            return []
        
        trade_rec_list = []
        if st.WEEKLY_STOCK_TRADE in strategy_list:
            trade_rec =  self.weekly_stock_play()
            if len(trade_rec) > 0:
                trade_rec_list.append(trade_rec)
        else:   
            watchlist = self.check_earning_date(watchlist)

        candidates = self.get_option_candidates(watchlist=watchlist, strategy_list=strategy_list)
        if candidates.shape[0] == 0:
            return trade_rec_list
             
        acct_value = self.get_account_value()

        exp_date_list = candidates[position_summary.EXP_DATE].unique()
        exp_date_risk_list = risk_matrix[position_summary.EXP_DATE]           
        for exp_date in exp_date_list:
            if exp_date in exp_date_risk_list:
                if  exp_date_risk_list[exp_date] > acct_value * self.risk_mgr.max_risk_per_expiration_date / 100:
                    candidates = candidates[candidates[position_summary.EXP_DATE] != exp_date]

        symbol_list = candidates[position_summary.SYMBOL].unique()
        symbol_risk_list = risk_matrix[position_summary.SYMBOL]           
        for symbol in symbol_list:
            if symbol in symbol_risk_list:
                if  symbol_risk_list[symbol] > acct_value * self.risk_mgr.max_risk_per_asset / 100:
                    candidates = candidates[candidates[position_summary.SYMBOL] != symbol]
                
        #candidates = candidates.groupby([position_summary.SYMBOL, position_summary.EXP_DATE, position_summary.STRATEGY]).first()
        for i, opt in candidates.iterrows():  
            symbol =   opt[position_summary.SYMBOL]
            exp_date = opt[position_summary.EXP_DATE]
            strategy = opt[position_summary.STRATEGY]             

            symbol_risk = symbol_risk_list[symbol] if symbol in symbol_risk_list else 0.0
            if symbol_risk + opt[position_summary.MAX_RISK] > acct_value * self.risk_mgr.max_risk_per_asset /100:
                continue

            exp_risk = exp_date_risk_list[exp_date] if exp_date in exp_date_risk_list else 0.0
            if exp_risk + opt[position_summary.MAX_RISK] > acct_value * self.risk_mgr.max_risk_per_expiration_date / 100:
                continue

            if strategy == st.SHORT_PUT:
                cash_avail = self.get_cash_position()
                if cash_avail < 10000:
                    self.logger.info('No enough cash %.2f to sell put' % (cash_avail))
                    continue

            trade_rec = self.create_position_summary(opt)  

            if len(trade_rec) > 0:
                trade_rec_list.append(trade_rec)

        self.logger.info('%d option strategy order created' % len(trade_rec_list))

        return trade_rec_list

    class optionLegDesc(object):
        def __init__(self, exp_date, leg):
            self.STRIKE       = leg[position.STRIKE]
            self.OTYPE        = leg[position.OTYPE] 
            self.OPEN_ACTION  = leg[position.OPEN_ACTION]
            self.QUANTITY     = leg[position.QUANTITY]
            self.PRICE        = leg[position.OPEN_PRICE]
            self.EXP_DATE     = exp_date
            self.IV           = leg[quote.IMPLIED_VOLATILITY]
            self.DELTA        = leg[quote.DELTA]            
            self.OPEN_INTEREST= leg[quote.OPEN_INTEREST]
  
    def create_transaction(self, pos, buy_sell, open_close, commission=0, fee=0):

        trx_time = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")     
        symbol = pos[position.SYMBOL]
        otype = pos[position.OTYPE]
        open_close = open_close
        buy_sell = buy_sell
        quantity =pos[position.QUANTITY]
        price = pos[position.LAST_PRICE]
        amount = quantity * price        
        commission = commission
        fee = fee
        amount = 0

        if otype in [asset.CALL, asset.PUT]:
            amount = quantity * price * 100                   
            strike = pos[position.STRIKE]
            exp_date = pos[position.EXP_DATE]

            field_names =  "trx_time,symbol,otype,strike,exp_date,open_close,buy_sell,quantity,price,commission,fee,amount"

            values =  '?,?,?,?,?,?,?,?,?,?,?,?' 

            fields = [trx_time, symbol, otype, strike, exp_date, open_close, buy_sell, quantity,\
                      price, commission, fee, amount]

            sql = "INSERT INTO transactions ("+field_names+") VALUES("+values+")" 
            cursor = self.db_conn.cursor()          
            cursor.execute(sql, fields)
        elif otype == asset.STOCK:
            amount = quantity * price       

            field_names =  "trx_time,symbol,otype,open_close,buy_sell,quantity,price,commission,fee,amount"

            values =  '?,?,?,?,?,?,?,?,?,?' 

            fields = [trx_time, symbol, otype, open_close, buy_sell, quantity,\
                      price, commission, fee, amount]

            sql = "INSERT INTO transactions ("+field_names+") VALUES("+values+")" 
            cursor = self.db_conn.cursor()          
            cursor.execute(sql, fields)

    def get_account_summary(self):

        cl = summary_col_name

        summary = {}
        
        summary[cl.INIT_BALANCE] = self.get_initial_balance()
        summary[cl.ACCT_VALUE] = self.get_account_value()
        summary[cl.ASSET_VALUE] = self.get_asset_value()
        summary[cl.CASH] = self.get_cash_position()
        summary[cl.MARGIN] = self.get_margin_position()   
        summary[cl.UNREALIZED_PL], summary[cl.REALIZED_PL] = self.get_pl()
        summary[cl.GAIN] = round(100 * ((summary[cl.UNREALIZED_PL]+summary[cl.REALIZED_PL]) / summary[cl.INIT_BALANCE]),2)

        #summary['open date'] = self.get_open_date()        

        o = self.get_position_summary()                
        tc = o.shape[0]        
        summary[cl.ALL_TRX_CNT] = tc
        summary[cl.AVG_ALL_TRX_WIN_PL] = round(o[o[position_summary.GAIN]>0][position_summary.PL].sum()/tc if tc > 0 else 0,2)
        summary[cl.AVG_ALL_TRX_LOSS_PL] = round(o[o[position_summary.GAIN]<0][position_summary.PL].sum()/tc if tc > 0 else 0,2)        
        summary[cl.ALL_WIN_RATE] = round(100*o[o[position_summary.GAIN]>0].shape[0]/tc if tc > 0 else 0, 2)       

        oo = o[o[position_summary.STATUS]==asset.OPENED]
        oo[cl.MAX_RISK] = oo.apply(lambda x: x[position_summary.MAX_LOSS] * x[position_summary.QUANTITY] * 100 if x[position_summary.STRATEGY] != st.UNPAIRED else x[position_summary.OPEN_PRICE], axis = 1)  
        summary[cl.MAX_RISK] = round(oo[cl.MAX_RISK].sum(),2)
        summary[cl.RISK_RATIO] = round(100*summary[cl.MAX_RISK]/summary[cl.ACCT_VALUE],2)

        oc = oo.shape[0]
        summary[cl.OPENED_TRX_CNT] = oc        
        summary[cl.AVG_OPENED_TRX_WIN_PL] = round(oo[oo[position_summary.GAIN]>0][position_summary.PL].sum()/oc if oc > 0 else 0,2)
        summary[cl.AVG_OPENED_TRX_LOSS_PL] = round(oo[oo[position_summary.GAIN]<0][position_summary.PL].sum()/oc if oc > 0 else 0,2)           
        summary[cl.OPENED_WIN_RATE] = round(100*oo[oo[position_summary.GAIN]>0].shape[0]/oc if oc > 0 else 0,2)             

        co = o[(o[position_summary.STATUS]== asset.CLOSED) | (o[position_summary.STATUS]==asset.EXPIRED)]
        cc = co.shape[0]
        summary[cl.CLOSED_TRX_CNT] = cc                  
        summary[cl.AVG_CLOSED_TRX_WIN_PL] = round(co[co[position_summary.GAIN]>0][position_summary.PL].sum()/cc if cc > 0 else 0,2)
        summary[cl.AVG_CLOSED_TRX_LOSS_PL] = round(co[co[position_summary.GAIN]<0][position_summary.PL].sum()/cc if cc > 0 else 0,2)            
        summary[cl.CLOSED_WIN_RATE] = round(100*co[co[position_summary.GAIN]>0].shape[0]/cc if cc > 0 else 0,2)      

        return summary
    #######################Helper##################################    

    def roll_option_long(self, symbol, exp_date_list, otype):
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_option_long( symbol, 
                                otype, 
                                predictlist,                
                                min_pnl = self.entry_crit.min_pnl,                                    
                                min_win_prob = self.entry_crit.min_chance_of_win,         
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)        
        return df  
        
    def roll_option_short(self, symbol, exp_date_list, otype):
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)              
        df = pick_option_short( symbol, 
                                otype, 
                                predictlist,            
                                min_pnl = self.entry_crit.min_pnl,                                         
                                min_win_prob = self.entry_crit.min_chance_of_win,
                                min_price = self.entry_crit.min_price_to_short,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)        
        return df
    
    def roll_vertical_call_spread(self, symbol, exp_date_list, credit=True):
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)
        df = pick_vertical_call_spreads(symbol,                          
                                        predictlist,
                                        credit=credit,
                                        max_spread = self.runtime_config.max_spread,                        
                                        min_win_prob=self.entry_crit.min_chance_of_win,
                                        min_pnl = self.entry_crit.min_pnl,
                                        max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                        max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                        min_open_interest=self.entry_crit.min_open_interest)                                               
        return df       

    def roll_vertical_put_spread(self, symbol, exp_date_list, credit=True):            
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)
        df = pick_vertical_put_spreads(symbol,                          
                                    predictlist,
                                    credit=credit,
                                    max_spread = self.runtime_config.max_spread,                        
                                    min_win_prob=self.entry_crit.min_chance_of_win,
                                    min_pnl = self.entry_crit.min_pnl,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)   
            
        return df                

    def roll_iron_condor(self, symbol, exp_date_list,  credit=True):
        min_price = self.entry_crit.min_price_to_short if credit else 0.0
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_iron_condor(symbol,
                            predictlist,
                            credit=credit,                                           
                            max_spread = self.runtime_config.max_spread,
                            min_price = min_price,                              
                            min_win_prob=self.entry_crit.min_chance_of_win,
                            min_pnl = self.entry_crit.min_pnl,
                            max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                            max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                            min_open_interest=self.entry_crit.min_open_interest)
        return df                

    def roll_call_butterfly(self, symbol, exp_date_list, credit=True):

        min_price = self.entry_crit.min_price_to_short if credit else 0.0
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_call_butterfly(symbol,                          
                                predictlist,
                                credit=credit,       
                                max_spread = self.runtime_config.max_spread,
                                min_price = min_price,                              
                                min_win_prob=self.entry_crit.min_chance_of_win,
                                min_pnl = self.entry_crit.min_pnl,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)            
        return df                
    
    def roll_put_butterfly(self, symbol, exp_date_list, credit=True):

        min_price = self.entry_crit.min_price_to_short if credit else 0.0
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_put_butterfly(symbol,                          
                                predictlist,
                                credit=credit,
                                max_spread = self.runtime_config.max_spread,
                                min_price = min_price,                              
                                min_win_prob=self.entry_crit.min_chance_of_win,
                                min_pnl = self.entry_crit.min_pnl,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)
        return df    

    def roll_iron_butterfly(self, symbol, exp_date_list, credit=True):
        min_price = self.entry_crit.min_price_to_short if credit else 0.0   
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_iron_butterfly(symbol,                          
                                predictlist,
                                credit=credit,
                                max_spread = self.runtime_config.max_spread,
                                min_price = min_price,                              
                                min_win_prob=self.entry_crit.min_chance_of_win,
                                min_pnl = self.entry_crit.min_pnl,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest) 
    
        return df                

    ############################            
    def pick_option_long(self, watchlist, otype):
        candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    
        pick_df = pd.DataFrame()
        for symbol in candidates:

            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if otype == asset.CALL:                
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.LONG_CALL) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.LONG_PUT) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_option_long( symbol, 
                                    otype, 
                                    predictlist,                
                                    min_pnl = self.entry_crit.min_pnl,                                    
                                    min_win_prob = self.entry_crit.min_chance_of_win,         
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)        
            
            self.logger.info('pick_option_log %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])
    
        return pick_df    
    
    def pick_option_short(self, watchlist, otype):
        candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        pick_df = pd.DataFrame()
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if otype == asset.CALL:    
                shares = self.get_stock_open_shares(symbol)
                q = shares // 100
                if q == 0:
                    self.logger.info('No enough %s shared %.2f to sell covered call' % (symbol, shares))
                    continue                 
                # TODO: check if covered call already consume all shares 
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.COVERED_CALL) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.SHORT_PUT) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)              
            df = pick_option_short( symbol, 
                                    otype, 
                                    predictlist,            
                                    min_pnl = self.entry_crit.min_pnl,                                         
                                    min_win_prob = self.entry_crit.min_chance_of_win,
                                    min_price = self.entry_crit.min_price_to_short,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)        

            self.logger.info('pick_option_short %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])
        return pick_df

    def pick_vertical_call_spread(self, watchlist, credit=True):
        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        pick_df = pd.DataFrame()

        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)

            if credit:                
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.CREDIT_CALL_SPREAD) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.DEBIT_CALL_SPREAD) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)
            min_price = self.entry_crit.min_price_to_short if credit else 0.0
            df = pick_vertical_call_spreads(symbol,                          
                                            predictlist,
                                            credit=credit,
                                            max_spread = self.runtime_config.max_spread,                        
                                            min_win_prob=self.entry_crit.min_chance_of_win,
                                            min_pnl = self.entry_crit.min_pnl,
                                            max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                            max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                            min_open_interest=self.entry_crit.min_open_interest)                           

            self.logger.info('pick_vertical_call_spread %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])
    
        return pick_df                

    def pick_vertical_put_spread(self, watchlist, credit=True):
        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        pick_df = pd.DataFrame()

        min_price = self.entry_crit.min_price_to_short if credit else 0.0

        for symbol in candidates:    
            
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)

            if credit:                
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.CREDIT_PUT_SPREAD) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.DEBIT_PUT_SPREAD) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)

            #target = target_low if credit else target_high  

            df = pick_vertical_put_spreads(symbol,                          
                                        predictlist,
                                        credit=credit,
                                        max_spread = self.runtime_config.max_spread,                        
                                        min_win_prob=self.entry_crit.min_chance_of_win,
                                        min_pnl = self.entry_crit.min_pnl,
                                        max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                        max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                        min_open_interest=self.entry_crit.min_open_interest)   
            
            self.logger.info('pick_vertical_put_spread %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    

        return pick_df                

    def pick_iron_condor(self, watchlist, credit=True):

        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    
        
        min_price = self.entry_crit.min_price_to_short if credit else 0.0

        pick_df = pd.DataFrame()
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if credit:                
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.CREDIT_IRON_CONDOR) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.DEBIT_IRON_CONDOR) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue

            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_iron_condor(symbol,
                                predictlist,
                                credit=credit,                                           
                                max_spread = self.runtime_config.max_spread,
                                min_price = min_price,                              
                                min_win_prob=self.entry_crit.min_chance_of_win,
                                min_pnl = self.entry_crit.min_pnl,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)

            self.logger.info('pick_iron_condor %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    
    
        return pick_df                

    def pick_call_butterfly(self, watchlist, credit=True):

        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        min_price = self.entry_crit.min_price_to_short if credit else 0.0

        pick_df = pd.DataFrame()
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if credit:                
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.CREDIT_CALL_BUTTERFLY) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.DEBIT_CALL_BUTTERFLY) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
                        
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_call_butterfly(symbol,                          
                                    predictlist,
                                    credit=credit,       
                                    max_spread = self.runtime_config.max_spread,
                                    min_price = min_price,                              
                                    min_win_prob=self.entry_crit.min_chance_of_win,
                                    min_pnl = self.entry_crit.min_pnl,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)

            self.logger.info('pick_call_butterfly %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    
        return pick_df                
    
    def pick_put_butterfly(self, watchlist, credit=True):

        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        min_price = self.entry_crit.min_price_to_short if credit else 0.0

        pick_df = pd.DataFrame()
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)

            if credit:                
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.CREDIT_PUT_BUTTERFLY) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.DEBIT_PUT_BUTTERFLY) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_put_butterfly(symbol,                          
                                    predictlist,
                                    credit=credit,
                                    max_spread = self.runtime_config.max_spread,
                                    min_price = min_price,                              
                                    min_win_prob=self.entry_crit.min_chance_of_win,
                                    min_pnl = self.entry_crit.min_pnl,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)

            self.logger.info('pick_put_butterfly %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    
        return pick_df    

    def pick_iron_butterfly(self, watchlist, credit=True):
        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        min_price = self.entry_crit.min_price_to_short if credit else 0.0
        pick_df = pd.DataFrame()        
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if credit:                
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.IRON_BUTTERFLY) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[position_summary.SYMBOL]==symbol) &
                                     (self.mdf[position_summary.STRATEGY]==st.REVERSE_IRON_BUTTERFLY) &
                                     (self.mdf[position_summary.STATUS]==asset.OPENED)][position_summary.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))
            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_iron_butterfly(symbol,                          
                                    predictlist,
                                    credit=credit,
                                    max_spread = self.runtime_config.max_spread,
                                    min_price = min_price,                              
                                    min_win_prob=self.entry_crit.min_chance_of_win,
                                    min_pnl = self.entry_crit.min_pnl,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)

            self.logger.info('pick_butterfly %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    
    
        return pick_df                

if __name__ == '__main__':

    import sys

    sys.path.append(r'\Users\jimhu\option_trader\src')
    
    from option_trader.admin.site import site
    from option_trader.admin import user
    from option_trader.consts import strategy as st

    logging.basicConfig(level=logging.DEBUG)

    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    logging.getLogger('yfinance').setLevel(logging.WARNING)
    
    DEFAULT_SITE_STRATEGY = [st.CREDIT_PUT_SPREAD, st.CREDIT_IRON_CONDOR]
    
    watchlist = ['MSFT', 'AAPL', 'AMZN', 'NVDA', 'BLDR', 'COST', 'GOOGL', 'NFLX', 'META', 'SPY', 'QQQ', 'AMD', 'TSLA', 'ISRG']

    mysite = site('mysite', check_afterhour=False)


    stester = mysite.get_user('chrishua')

    account_list = stester.get_account_list()

    for account_name in account_list:
        print('%s update Account %s' % (stester.user_name, account_name))
        account_obj = stester.get_account(account_name)
        #account_obj.update_position()
        account_obj.open_new_strategy_positions()

    exit(0)
    real_user = mysite.get_user('real')
    real_bullish= real_user.get_account('bullish')
    real_bearish= real_user.get_account('bearish')    
    real_neutral= real_user.get_account('neutral')
    real_bigmove= real_user.get_account('bigmove')

    #real_bullish.open_new_strategy_positions()
    real_bearish.open_new_strategy_positions()
    real_neutral.open_new_strategy_positions()
    real_bigmove.open_new_strategy_positions()

    #x = algo_11_07_iron_condor.open_new_strategy_positions(watchlist=watchlist, strategy_list=st.ALL_STRATEGY)  

    #print(len(x))

    exit(0)



    winwin_act = winwin.create_account('butterfly')

    winwin_act.get_position_summary()

    exit(0)

  

    jihuang = mysite.create_user('jihuang')

    account_list = jihuang.get_account_list()

    for account_name in account_list:
        print('%s update Account %s' % (jihuang.user_name, account_name))
        account_obj = jihuang.get_account(account_name)
        account_obj.update_position()
  