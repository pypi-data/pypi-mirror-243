from __future__ import annotations

import numpy as np
import pandas as pd
import datetime
import pathlib
import functools
import sys
import matplotlib.pyplot as plt

_path_to_this_file = pathlib.Path(__file__).parent.resolve()
# add this files directory to path
sys.path.append(str(_path_to_this_file))

global _config
global _util_funcs
# project specific imports
import _config
import _util_funcs

# suppress chained assignment warning
pd.options.mode.chained_assignment = None

# TODO: Check for none dates
#def FF_factors(
#               dfin: pd.DataFrame,
#               factors: list[str] = None,  
#               start_date: datetime.datetime = None, 
#               end_date: datetime.datetime = None, 
#               date_col: str = 'date',
#               ret_type: str = 'adjret', 
#               risk_free: str = 'rf',
#               drop_na: bool = True
#    ) -> pd.DataFrame:
#    """Creates standard Fama-French factors
#    
#    Creates the Fama-French factors using the original accounting practices from
#    Eugene Fama's and Kenneth French's original 1992 paper. 
#    The Cross-Section of Expected Stock Returns https://doi.org/10.1111/j.1540-6261.1992.tb04398.x
#    
#    Constructable factors include: 'mkt' market return, 'rf' risk free rate, 'mkt_rf' equity premium, 
#    'smb3' 3 factor small minus big, 'smb5' 5 factor small minus big, 'hml' high minus low, 
#    'rmw' robust minus weak, 'cma' conservative minus aggresive, 'mom' momentum, 
#    'st_rev' short term reversal, 'lt_rev' long term reversal. 
#    See https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html for constrution notes.
#    
#    Args:
#        factors: list of factors (optional)
#        dfin: datadrame with assets to use (optional)
#        start_date: start date for factors (optional)
#        end_date: end date for factors (optional)
#        weight_type: weights used to calculate returns
#        ret_type: return type with or without dividends
#        drop_na: if true drop rows that have NaN values
#    Returns: 
#        A dataframe with the specifed factros and a date column. Dataframe sorted by date.
#    Example:
#        Create the original 3 factor Fama-French model between 'date1' and 'date2'
#        df = FamaFrench.FF_factors(
#            factors = ['mkt_rf', 'smb3', 'hml'], 
#            start_date = date1, 
#            end_date = date2
#        )
#    TODO:
#        Error checking
#    """
#    # construct all factors or not
#    if(factors is None):
#        construct_factors = ['mkt', 'rf', 'mkt_rf', 'smb3', 'smb5', 'hml', 'rmw',
#                             'cma', 'mom', 'st_rev', 'lt_rev']
#    else:
#        construct_factors = factors     
#
#    # create resulting dataframe
#    res = pd.DataFrame()
#    date_s = dfin[date_col].unique()
#    res[date_col] = date_s
#    res = res.sort_values(by = [date_col])
#
#    # calculate the market return of supplied assets
#    if('mkt' in construct_factors):
#        mkt_df = _util_funcs.gorup_avg(df = dfin, 
#                                      gr = date_col, 
#                                      vr = ret_type, 
#                                      wt = 'me',
#                                      name = 'mkt'
#                                    )
#        res = res.merge(mkt_df, how = 'left', on = ['date'])
#    
#    # add the risk free rate
#    if('rf' in construct_factors):
#        rf_df = self.DB.query_riskfree(query_start_date, query_end_date, 'M')
#        rf_df = rf_df.rename(columns = {'rf': 'rf'}) # just for naming consistency
#        res = res.merge(rf_df, on = ['date'], how = 'left')
#
#    
#    # add the market premium
#    if('mkt_rf' in construct_factors):
#        if('mkt' in construct_factors and 'rf' in construct_factors):
#            res['mkt_rf'] = res.mkt - res.rf
#        elif('mkt' in construct_factors and not 'rf' in construct_factors):
#            rf_df = self.DB.query_riskfree(query_start_date, query_end_date, 'M')
#            rf_df = rf_df.rename(columns = {'rf': 'rf'}) # just for naming consistency
#            res = res.merge(rf_df, on = ['date'], how = 'left')
#            res['mkt_rf'] = res.mkt - res.rf
#            res = res.drop(columns = ['mkt', 'rf'])
#        elif(not 'mkt' in construct_factors and 'rf' in construct_factors):
#            mkt_df = _util_funcs.gorup_avg(df = ccm_df, 
#                                          gr = 'date', 
#                                          vr = ret_type, 
#                                          wt = 'me',
#                                          name = 'mkt'
#                                        )
#            res = res.merge(mkt_df, how = 'left', on = ['date'])
#            res['mkt_rf'] = res.mkt - res.rf
#            res = res.drop(columns = ['mkt', 'rf'])
#        else:
#            mkt_df = _util_funcs.gorup_avg(df = ccm_df, 
#                                          gr = 'date', 
#                                          vr = ret_type, 
#                                          wt = 'me',
#                                          name = 'mkt'
#                                        )
#            res = res.merge(mkt_df, how = 'left', on = ['date'])
#            rf_df = self.DB.query_riskfree(query_start_date, query_end_date, 'M')
#            rf_df = rf_df.rename(columns = {'rf': 'rf'}) # just for naming consistency
#            res = res.merge(rf_df, on = ['date'], how = 'left')
#            res['mkt_rf'] = res.mkt - res.rf
#            res = res.drop(columns = ['mkt', 'rf'])
#    # SMB factor from the 3-factor Fama-French model
#    if('smb3' in construct_factors):
#        # portfolio sorts on ME and BM
#        sorts_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'ffbm': [0.3, 0.7]},
#            sorting_funcs = {'me': self.sort_50, 'ffbm': self.sort_3070},
#            drop_na = False, rebalance_freq = 'A'
#        )
#        sorts_df['smb3'] = (sorts_df[['me1_ffbm1', 'me1_ffbm2', 'me1_ffbm3']].mean(axis = 1)
#                             - sorts_df[['me2_ffbm1', 'me2_ffbm2', 'me2_ffbm3']].mean(axis = 1))
#        
#        res = res.merge(sorts_df[['date', 'smb3']], how = 'left', on = ['date'])
#    # SMB factor from the 5-factor Fama-French model
#    if('smb5' in construct_factors):
#        # sorts on BM
#        sortsBM_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'ffbm': [0.3, 0.7]}, 
#            sorting_funcs = {'me': self.sort_50, 'ffbm': self.sort_3070}, 
#            drop_na = False, rebalance_freq = 'A'
#        )
#        # sorts on OP
#        sortsOP_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'op': [0.3, 0.7]}, 
#            sorting_funcs = {'me': self.sort_50, 'op': self.sort_3070}, 
#            drop_na = False, rebalance_freq = 'A'
#        )
#        # sorts on INV
#        sortsINV_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'inv': [0.3, 0.7]}, 
#            sorting_funcs = {'me': self.sort_50, 'inv': self.sort_3070}, 
#            drop_na = False, rebalance_freq = 'A'
#        )
#        # combine sorts into one dataframe
#        sortsBM_df = sortsBM_df.merge(sortsOP_df, how = 'left', on = ['date'])
#        sortsBM_df = sortsBM_df.merge(sortsINV_df, how = 'left', on = ['date'])
#        # housekeeping
#        sortsBM_df = sortsBM_df.set_index('date')
#        sortsBM_df = sortsBM_df.dropna(how = 'all')
#        # create factors
#        sortsBM_df['SMB_BM'] = (sortsBM_df[['me1_ffbm1', 'me1_ffbm2', 'me1_ffbm3']].mean(axis = 1)
#                                 - sortsBM_df[['me2_ffbm1', 'me2_ffbm2', 'me2_ffbm3']].mean(axis = 1))
#        
#        sortsBM_df['SMB_OP'] = (sortsOP_df[['me1_op1', 'me1_op2', 'me1_op3']].mean(axis = 1)
#                                 - sortsOP_df[['me2_op1', 'me2_op2', 'me2_op3']].mean(axis = 1))
#        
#        sortsBM_df['SMB_INV'] = (sortsINV_df[['me1_inv1', 'me1_inv2', 'me1_inv3']].mean(axis = 1)
#                                  - sortsINV_df[['me2_inv1', 'me2_inv2', 'me2_inv3']].mean(axis = 1))
#        # average factors
#        sortsBM_df['smb5'] = sortsBM_df[['SMB_BM', 'SMB_OP', 'SMB_INV']].mean(axis = 1)
#        # add to result dataframe
#        sortsBM_df = sortsBM_df.reset_index()
#        res = res.merge(sortsBM_df[['date', 'smb5']], how = 'left', on = ['date'])
#    if('hml' in construct_factors):
#        sortsBM_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'ffbm': [0.3, 0.7]}, 
#            sorting_funcs = {'me': self.sort_50, 'ffbm': self.sort_3070}, 
#            drop_na = False, rebalance_freq = 'A'
#        )
#        sortsBM_df['hml'] = (sortsBM_df[['me1_ffbm3', 'me2_ffbm3']].mean(axis = 1)
#                              - sortsBM_df[['me1_ffbm1', 'me2_ffbm1']].mean(axis = 1))
#        res = res.merge(sortsBM_df[['date', 'hml']], how = 'left', on = ['date'])
#    if('rmw' in construct_factors):
#        sortsOP_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'op': [0.3, 0.7]}, 
#            sorting_funcs = {'me': self.sort_50, 'op': self.sort_3070}, 
#            drop_na = False, rebalance_freq = 'A'
#        )
#        sortsOP_df['rmw'] = (sortsOP_df[['me1_op3', 'me2_op3']].mean(axis = 1)
#                              - sortsOP_df[['me1_op1', 'me2_op1']].mean(axis = 1))
#        res = res.merge(sortsOP_df[['date', 'rmw']], how = 'left', on = ['date'])
#    if('cma' in construct_factors):
#        sortsINV_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'inv': [0.3, 0.7]}, 
#            sorting_funcs = {'me': self.sort_50, 'inv': self.sort_3070}, 
#            drop_na = False, rebalance_freq = 'A'
#        )
#        sortsINV_df['cma'] = (sortsINV_df[['me1_inv1', 'me2_inv1']].mean(axis = 1)
#                              - sortsINV_df[['me1_inv3', 'me2_inv3']].mean(axis = 1))
#        res = res.merge(sortsINV_df[['date', 'cma']], how = 'left', on = ['date'])
#    if('mom' in construct_factors):
#        sortsPR2_12_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'pr2_12': [0.3, 0.7]}, 
#            sorting_funcs = {'me': self.sort_50, 'pr2_12': self.sort_3070}, 
#            drop_na = False, rebalance_freq = 'A'
#        )
#        sortsPR2_12_df['mom'] = (sortsPR2_12_df[['me1_pr2_123', 'me2_pr2_123']].mean(axis = 1)
#                                 - sortsPR2_12_df[['me1_pr2_121', 'me2_pr2_121']].mean(axis = 1))
#        res = res.merge(sortsPR2_12_df[['date', 'mom']], how = 'left', on = ['date'])
#    if('st_rev' in construct_factors):
#        sortsPR1_1_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'pr1_1': [0.3, 0.7]}, 
#            sorting_funcs = {'me': self.sort_50, 'pr1_1': self.sort_3070}, 
#            drop_na = False, rebalance_freq = 'A'
#        )
#        sortsPR1_1_df['st_rev'] = (sortsPR1_1_df[['me1_pr1_11', 'me2_pr1_11']].mean(axis = 1)
#                                    - sortsPR1_1_df[['me1_pr1_13', 'me2_pr1_13']].mean(axis = 1))
#        res = res.merge(sortsPR1_1_df[['date', 'st_rev']], how = 'left', on = ['date'])
#    if('lt_rev' in construct_factors):
#        sortsPR13_60_df = self.sort_portfolios(
#            stocks = ccm_df, char_bkpts = {'me': [0.5], 'pr13_60': [0.3, 0.7]}, 
#            sorting_funcs = {'me': self.sort_50, 'pr13_60': self.sort_3070}, 
#            drop_na = False, rebalance_freq = 'A'
#        )
#        sortsPR13_60_df['lt_rev'] = (sortsPR13_60_df[['me1_pr13_601', 'me2_pr13_601']].mean(axis = 1)
#                                     - sortsPR13_60_df[['me1_pr13_603', 'me2_pr13_603']].mean(axis = 1))
#        res = res.merge(sortsPR13_60_df[['date', 'lt_rev']], how = 'left', on = ['date'])
#    res = res.set_index('date').sort_index()
#    res = res.reset_index(drop = False)
#    if(drop_na): 
#        res = res.dropna(how = 'all')
#    return(res)


#def FF_3factor(self, 
#               start_date: datetime.datetime = None, 
#               end_date: datetime.datetime = None, 
#               weigth_type: str = 'vw', 
#               ret_type: str = 'adjret', 
#               drop_na: bool = True, 
#               dfin = None):
#    
#    return(self.FF_factors(factors = ['mkt_rf', 'smb3', 'hml'], 
#                           dfin = dfin,
#                           start_date = start_date, end_date = end_date, 
#                           weight_type = weigth_type, ret_type = ret_type, 
#                           drop_na = drop_na
#                        )
#        )
#def FF_5factor(self, 
#               start_date: datetime.datetime = None, 
#               end_date: datetime.datetime = None, 
#               weigth_type: str = 'vw', 
#               ret_type: str = 'adjret', 
#               drop_na: bool = True, 
#               dfin = None):
#    
#    return(self.FF_factors(factors = ['mkt_rf', 'smb5', 'hml', 'cma', 'rmw'], 
#                           dfin = dfin,
#                           start_date = start_date, end_date = end_date, 
#                           weight_type = weigth_type, ret_type = ret_type, 
#                           drop_na = drop_na))

def breakpoint_ts(df_in, vars, qtiles = None):
    
    DEFAULT_QTILES = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 
                      0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    DECILES_QTILES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    QUINTIL_QTILES = [0.2, 0.4, 0.6, 0.8]
    dict_in = {}
    if(type(vars) is dict):
        dict_in = vars
    else:
        if(type(qtiles) is int or qtiles is None):
            for var in vars:
                if(qtiles == 5):
                    dict_in[var] = QUINTIL_QTILES
                elif(qtiles == 10):
                    dict_in[var] = DECILES_QTILES
                else:
                    dict_in[var] = DEFAULT_QTILES
        elif(type(qtiles) is list):
            for var in vars:
                dict_in[var] = qtiles
        else:
            raise TypeError("No valid vars or qtile combination given.")
    res = []
    for var, qtiles in dict_in.items():
        temp = df_in.groupby('date')[var].describe(percentiles = qtiles)
        ptiles = [f'{int(100 * q)}%' for q in qtiles]
        temp = temp[ptiles]
        temp = temp.add_prefix(f'{var}_')
        res.append(temp)
    fin = functools.reduce(lambda x, y: pd.merge(x, y, on = 'date'), res)
    fin = fin.reset_index()
    return(fin)

# sorting functions
def sort_50(row, var):
    if(row[var] < row[f'{var}_50%']):
        res = f'{var}1'
    elif(row[var] >= row[f'{var}_50%']):
        res = f'{var}2'
    else:
        res = '--fail'
    return(res)

def sort_050(row, var):
    if(row[var] < 0):
        res = f'{var}1'
    if(row[var] >= 0 and row[var] < row[f'{var}_50%']):
        res = f'{var}2'
    elif(row[var] >= row[f'{var}_50%']):
        res = f'{var}3'
    else:
        res = '--fail'
    return(res)

def sort_3070(row, var):
    if(row[var] < row[f'{var}_30%']):
        res = f'{var}1'
    elif(row[var] >= row[f'{var}_30%'] and row[var] < row[f'{var}_70%']):
        res = f'{var}2'
    elif(row[var] >= row[f'{var}_70%']):
        res = f'{var}3'
    else:
        res = '--fail'
    return(res)

def sort_03070(row, var):
    if(row[var] <= 0):
        res = f'{var}1'
    elif(row[var] >= 0 and row[var] < row[f'{var}_30%']):
        res = f'{var}2'
    elif(row[var] >= row[f'{var}_30%'] and row[var] < row[f'{var}_70%']):
        res = f'{var}3'
    elif(row[var] >= row[f'{var}_70%']):
        res = f'{var}4'
    else:
        res = '--fail'
    return(res)

def sort_quintile(row, var):
    if(row[var] <= row[f'{var}_20%']):
        res = f'{var}1'
    elif(row[var] > row[f'{var}_20%'] and row[var] <= row[f'{var}_40%']):
        res = f'{var}2'
    elif(row[var] > row[f'{var}_40%'] and row[var] <= row[f'{var}_60%']):
        res = f'{var}3'
    elif(row[var] > row[f'{var}_60%'] and row[var] <= row[f'{var}_80%']):
        res = f'{var}4'
    elif(row[var] > row[f'{var}_80%']):
        res = f'{var}5'
    else:
        res = '--fail'
    return(res)

def sort_deciles(row, var):
    if(row[var] < row[f'{var}_10%']):
        res = f'{var}1'
    elif(row[var] >= row[f'{var}_10%'] and row[var] < row[f'{var}_20%']):
        res = f'{var}2'
    elif(row[var] >= row[f'{var}_20%'] and row[var] < row[f'{var}_30%']):
        res = f'{var}3'
    elif(row[var] >= row[f'{var}_30%'] and row[var] < row[f'{var}_40%']):
        res = f'{var}4'
    elif(row[var] >= row[f'{var}_40%'] and row[var] < row[f'{var}_50%']):
        res = f'{var}5'
    elif(row[var] >= row[f'{var}_50%'] and row[var] < row[f'{var}_60%']):
        res = f'{var}6'
    elif(row[var] >= row[f'{var}_60%'] and row[var] < row[f'{var}_70%']):
        res = f'{var}7'
    elif(row[var] >= row[f'{var}_70%'] and row[var] < row[f'{var}_80%']):
        res = f'{var}8'
    elif(row[var] >= row[f'{var}_80%'] and row[var] < row[f'{var}_90%']):
        res = f'{var}9'
    elif(row[var] >= row[f'{var}_90%']):
        res = f'{var}10'
    else:
        res = '--fail'
    return(res)

def sort_mutual_funds(funds, char_bkpts, sorting_funcs, rebalnce_freq):
    pass

def sort_portfolios(dfin: pd.DataFrame,
                    sorting_funcs,
                    char_bkpts: dict[str, list[float]] = None,
                    date_col: str = 'date',
                    rebalance_freq: str = 'A',
                    return_col: str = 'adjret',
                    weight_col: str = 'me',
                    sort_month: int = 7,
                    drop_na: bool = True,
                    breakpoint_exchanges: list[int] = [1],
                    suppress: bool = False):
    
    # removes nans
    dfin = dfin[dfin[weight_col] > 0]
    dfin.date = pd.to_datetime(dfin.date)

    if(rebalance_freq == 'A'):
        rebalance_df = dfin[dfin.month == sort_month]
    else:
        rebalance_df = dfin
    
    breakpoint_stocks_df = rebalance_df[rebalance_df.exchcd.isin(breakpoint_exchanges)]

    # calculate breakpoints
    breakpoints_df = breakpoint_ts(breakpoint_stocks_df, vars = char_bkpts)

    # merge breakpoints to the rebalance df
    rebalance_df = breakpoints_df.merge(rebalance_df, how = 'inner', on = [date_col])

    rank_cols = []
    for char, func in sorting_funcs.items():
        rank_cols.append(f'{char}_rank')
        rebalance_df[f'{char}_rank'] = rebalance_df.apply(func, args = (char, ), axis = 1)

    #rebalance_df = rebalance_df[rebalance_df.date >= datetime.datetime(1986, 1, 1)]

    #print(rebalance_df[['date', 'dp_20%', 'dp_40%', 'dp_60%', 'dp_80%', 'dp', 'dp_rank']].head(1000))
    #exit()
    
    for rank_col in rank_cols:
        if('--fail' in rebalance_df[rank_col].unique()):
            if(not suppress):
                print(f'{_config.bcolors.WARNING}There are stocks that could not be sorted in {rank_col}. They will be removed before constructing portfolios.{_config.bcolors.ENDC}')
            rebalance_df = rebalance_df[rebalance_df[rank_col] != '--fail']

    rebalance_df['port_name'] = rebalance_df[rank_cols].agg('_'.join, axis = 1)
    
    if(rebalance_freq == 'A'):
        fin = dfin.merge(rebalance_df[['gvkey', 'ffyear', 'port_name']], how = 'left', on = ['gvkey', 'ffyear'])
    else:
        fin = rebalance_df
    
    fin = fin.dropna(subset = ['port_name'])
    rets = _util_funcs.gorup_avg(df = fin, 
                                 gr = [date_col, 'port_name'], 
                                 vr = return_col, 
                                 wt = weight_col)
    firm = fin.groupby([date_col, 'port_name'])['gvkey'].count().reset_index().rename(columns = {'gvkey': 'num_firms'})
    rets = rets.pivot(index = date_col, columns = 'port_name', values = return_col)
    firm = firm.pivot(index = date_col, columns = 'port_name', values = 'num_firms')
    firm = firm.add_suffix('_num_firms')
    res = rets.merge(firm, how = 'inner', on = [date_col])
    if(drop_na): 
        res = res.dropna()
    res = res.reset_index()
    return(res)