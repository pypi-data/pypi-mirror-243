from option_trader.settings import app_settings   

class entryCrit(object):
    def __init__(self, data=None):  
        if data != None:
            self.min_pnl = data['min_pnl']
            self.min_chance_of_win = data['min_chance_of_win']
            self.min_delta_for_long = data['min_delta_for_long']
            self.max_delta_for_short = data['max_delta_for_short']  
            self.max_slope = data['max_slope']            
            self.min_open_interest = data['min_open_interest']
            self.min_opt_vol = data['min_opt_vol']  
            self.min_IV_HV_ratio_for_short = data['min_IV_HV_ratio_for_short']       
            self.max_IV_HV_ratio_for_long = data['max_IV_HV_ratio_for_long']       
            self.max_rating = data['max_rating']
            self.covered_call_contract = data['covered_call_contract']       
            self.iron_condor_min_theta =data['iron_condor_min_theta']       
            self.min_price_to_short = data['min_price_to_short']
        else:
            self.min_pnl = app_settings.ENTRY_CRIT.min_pnl
            self.min_chance_of_win = app_settings.ENTRY_CRIT.min_chance_of_win
            self.min_delta_for_long = app_settings.ENTRY_CRIT.min_delta_for_long
            self.max_delta_for_short = app_settings.ENTRY_CRIT.max_delta_for_short  
            self.max_slope = app_settings.ENTRY_CRIT.max_slope            
            self.min_open_interest =  app_settings.ENTRY_CRIT.min_open_interest
            self.min_opt_vol = app_settings.ENTRY_CRIT.min_opt_vol  
            self.min_IV_HV_ratio_for_short = app_settings.ENTRY_CRIT.min_IV_HV_ratio_for_short       
            self.max_IV_HV_ratio_for_long = app_settings.ENTRY_CRIT.max_IV_HV_ratio_for_long      
            self.max_rating = app_settings.ENTRY_CRIT.max_rating
            self.covered_call_contract = app_settings.ENTRY_CRIT.covered_call_contract        
            self.iron_condor_min_theta = app_settings.ENTRY_CRIT.iron_condor_min_theta  
            self.min_price_to_short = app_settings.ENTRY_CRIT.min_price_to_short                        
        
import numpy as np
class marketCondition(object):
    def __init__(self, data=None):  
        if data != None:
            self.current_vix = data['current_vix']
            self.VIX_low = data['VIX_low'] 
            self.VIX_high = data['VIX_high']
            self.IV_Rank_low = data['IV_Rank_low']
            self.IV_Rang_high = data['IV_Rang_high']                         
        else:
            self.current_vix = np.nan
            self.VIX_low = 20 
            self.VIX_high = 30
            self.IV_Rank_low = 20
            self.IV_Rang_high = 90            
class riskManager(object):
    def __init__(self, data=None):  
        if data != None: 
            self.stop_loss_percent = data['stop_loss_percent']
            self.stop_gain_percent = data['stop_gain_percent']
            self.close_days_before_earning = data['close_days_before_earning']
            self.close_days_before_expire = data['close_days_before_expire']
            self.open_min_days_to_earning = data['open_min_days_to_earning']        
            self.open_min_days_to_expire = data['open_min_days_to_expire']
            self.max_option_positions = data['max_option_positions']
            self.max_loss_per_position = data['max_loss_per_position']
            self.max_risk_per_asset = data['max_risk_per_asset']
            self.max_risk_per_expiration_date = data['max_risk_per_expiration_date']          
            self.weekly_stock_trade_amount = data['weekly_stock_trade_amount']              
            self.weekly_stock_trade_stop_percent = data['weekly_stock_trade_stop_percent'] 
            self.schema_updated = False
            if 'min_cash_percent' in data:
                self.min_cash_percent = data['min_cash_percent']                       
            else:
                self.min_cash_percent = app_settings.RISK_MGR.min_cash_percent       
                self.schema_updated = True
            if 'max_risk_ratio' in data:
                self.max_risk_ratio = data['max_risk_ratio']                       
            else:
                self.max_risk_ratio = app_settings.RISK_MGR.max_risk_ratio       
                self.schema_updated = True                
        else:
            self.stop_loss_percent = app_settings.RISK_MGR.stop_loss_percent
            self.stop_gain_percent = app_settings.RISK_MGR.stop_gain_percent
            self.close_days_before_earning = app_settings.RISK_MGR.close_days_before_earning
            self.close_days_before_expire = app_settings.RISK_MGR.close_days_before_expire
            self.open_min_days_to_earning = app_settings.RISK_MGR.open_min_days_to_earning        
            self.open_min_days_to_expire = app_settings.RISK_MGR.open_min_days_to_expire
            self.max_option_positions = app_settings.RISK_MGR.max_option_positions
            self.max_loss_per_position = app_settings.RISK_MGR.max_loss_per_position           
            self.max_risk_per_asset = app_settings.RISK_MGR.max_risk_per_asset
            self.max_risk_per_expiration_date = app_settings.RISK_MGR.max_risk_per_expiration_date
            self.weekly_stock_trade_amount = app_settings.RISK_MGR.weekly_stock_trade_amount
            self.weekly_stock_trade_stop_percent =app_settings.RISK_MGR.weekly_stock_trade_stop_percent     
            self.min_cash_percent = app_settings.RISK_MGR.min_cash_percent    
            self.max_risk_ratio = app_settings.RISK_MGR.max_risk_ratio
            self.schema_updated  = False   
            
class runtimeConfig(object):
    def __init__(self, data=None):  
        if data != None:    
            self.init_balance = data['init_balance']           
            self.nweek = data['nweek'] 
            self.weekday = data['weekday']    
            self.trend_window_size = data['trend_window_size']         
            self.max_days_to_expire = data['max_days_to_expire']  
            self.max_spread = data['max_spread']  
            self.max_strike_ratio = data['max_strike_ratio']      
            self.max_bid_ask_spread = data['max_bid_ask_spread']
            self.auto_trade = data['auto_trade']           
        else:
            self.init_balance = app_settings.RUNTIME_CONFIG.init_balance
            self.nweek = app_settings.RUNTIME_CONFIG.nweek 
            self.weekday = app_settings.RUNTIME_CONFIG.weekday    
            self.trend_window_size = app_settings.RUNTIME_CONFIG.trend_window_size        
            self.max_days_to_expire = app_settings.RUNTIME_CONFIG.max_days_to_expire
            self.max_spread = app_settings.RUNTIME_CONFIG.max_spread
            self.max_strike_ratio = app_settings.RUNTIME_CONFIG.max_strike_ratio
            self.max_bid_ask_spread = app_settings.RUNTIME_CONFIG.max_bid_ask_spread
            self.auto_trade = app_settings.RUNTIME_CONFIG.auto_trade
          


# weekday = 0: Monday
# nweek 0..N : number of weeks to expire
# stop_gain - profit taking percent
# stop_loss - stop loss percent

 