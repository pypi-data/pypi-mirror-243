import os
import sys
import pathlib
import shutil
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, '../src/FinToolsAP/')

import LocalDatabase
import Decorators

# set printing options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', shutil.get_terminal_size()[0])
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# directory for loacl wrds database 

# linux
LOCAL_WRDS_DB = pathlib.Path('/home/andrewperry/Documents')
#LOCAL_WRDS_DB = pathlib.Path('/media/andrewperry/Samsung_T5')


#LOCAL_WRDS_DB = pathlib.Path('/Volumes/Samsung_T5')

# mac
#LOCAL_WRDS_DB = pathlib.Path('/Users/andrewperry/Desktop')

@Decorators.Performance
def query_CRSP_performance(DB):
    return(DB.query_DB(DB.DBP.CRSP.CRSP_M, ticker = 'AAPL'))

def main():
    DB = LocalDatabase.LocalDatabase(save_directory = LOCAL_WRDS_DB, 
                                     database_name = 'WRDS2'
                                    )
    exit()
    df = query_CRSP_performance(DB)
    print(df.head())
    print(df.info())
    

if __name__ == "__main__":
    main()
