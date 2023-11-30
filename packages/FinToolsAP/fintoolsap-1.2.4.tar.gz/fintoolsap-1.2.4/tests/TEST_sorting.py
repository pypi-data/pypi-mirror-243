import os
import sys
import time
import shutil
import pathlib
import datetime
import functools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas.tseries.offsets

# add source directory to path
sys.path.insert(0, '../src/FinToolsAP/')

import LocalDatabase
import PortfolioSorts as SP
import _util_funcs


# set printing options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', shutil.get_terminal_size()[0])
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# directory for loacl wrds database
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents')
desktop = pathlib.Path('/home/andrewperry/Desktop')

save_directory = pathlib.Path('/home/andrewperry/Dropbox/Characteristics_construction/Characteristic_Con')

def main():

    DB = LocalDatabase.LocalDatabase(LOCAL_WRDS_DB, database_name = 'WRDS')
    df = DB.query_DB(DB.DBP.Compustat.COMP_A)

    df = DB.query_DB(DB.DBP.CCM)

    sorts_df = PS.sort_portfolios(dfin = df, 
                                          sorting_funcs = {'me': FF.sort_quintile, 'dp': FF.sort_quintile},
                                          char_bkpts = {'me': [0.2, 0.4, 0.6, 0.8], 'dp': [0.2, 0.4, 0.6, 0.8]},
                                          drop_na = False
                                        )
    sorts_df.to_csv(desktop / 'test_dp_sort_left_inclusive.csv', index = False)
    exit()
    
    '''
    for wt in ['me', 'wt']:
        for var in DB.DBP.CCM.CHARACTERISTICS:
            
            sorts_df = FF.sort_portfolios(dfin = df, 
                                          sorting_funcs = {var: FF.sort_deciles},
                                          char_bkpts = {var: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]},
                                          drop_na = False
                                        )
            filename = f'{var}_w-{wt}.csv'
            sorts_df.to_csv(save_directory / filename, index = False)
     '''
    breakpoints = FF.breakpoint_ts(df, DB.DBP.CCM.CHARACTERISTICS, qtiles = 10)
    breakpoints.to_csv(save_directory / 'breakpoints.csv', index = False)


if __name__ == '__main__':
    main()
