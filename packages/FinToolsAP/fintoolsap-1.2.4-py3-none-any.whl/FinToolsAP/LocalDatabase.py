from __future__ import annotations

""" Implements a local database.

Implement a local database that can be used to greatly speed up work flow.
The database is meant for financial data but can be used to store any type of
data. The class uses a SQLite3 backend to manage the database via sqlalchemy
and provides a python3 wrapper making the use of the data database very 
quick and efficient by returning a pandas dataframe object that is formatted to
(i.e. correct datatypes, only specified columns, sorted, etc).
Data can be added in two ways: (1) CSV files can be read 
into the database from a local folder and (2) the database also interfaces 
with Whartons Research Data Services to automatically download specified tables.

Typical Usage Example: 

    import FinToolsAP.LocalDatabase

    path_to_database = ...
    name_of_database = ...
    DB = LocalDatabase(path_to_db, name_of_database)
    df = DB.query_DB(DB.DBP.Table, start_date, end_date)
"""

# MIT License
# 
# Copyright (c) 2023 Andrew Maurice Perry
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
 
# standard python imports
import os
import sys
import zlib
import time
import shutil
import pathlib
import datetime
#import connectorx
import subprocess
import sqlalchemy
import numpy as np
import pandas as pd
import pandas.tseries.offsets

class LocalDatabase:

    def __init__(self, 
                 save_directory: pathlib.Path | str,
                 database_name: str = None,
                 update_all_tables: bool = False, 
                 update_created_tables: bool = False,
                 tables_to_update: list = [], 
                 only_use_CSV_files: bool = False):
        
        """ Initalizes the local database.

        Initializing the local database includes downloading data from
        WRDS, reading in CSV files, and making custom user specified
        tables.

        Args: 
            save_directory: Path to the local database.
            database_name: Name of the local database.
            update_all_tables: Upadte all tables or not.
            update_created_tables: Update all created tables.
            tables_to_upadte: Specific tables to update.
            only_use_CSV_files: Only use local CSV files to create database

        Returns: 
            Local database object.
        """

        self._path_to_this_file = pathlib.Path(__file__).parent.resolve()
        # add this files directory to path
        sys.path.append(str(self._path_to_this_file))

        global _config
        global _util_funcs
        # project specific imports
        import _config
        import _util_funcs

        # check for python3.5 or newer (needed fpr subprocess.run)
        if(sys.version_info[0] < 3 and sys.version_info[1] < 5):
            print(_config.ErrorMessage.INVALID_INTERPRETER.format(color = _config.bcolors.FAIL))
            raise _config.Exceptions.InterpreterError

        init_start = time.time()

        # set private class attributes
        self._root_path = pathlib.Path(save_directory)
        if(database_name is not None):
            self._root_path /= database_name
        else:
            self._root_path /= _config.Directories._base_name
    
        self._path_to_db = self._root_path
        if(database_name is not None):
            self._path_to_db /= f'{database_name}.db'
        else:
            self._path_to_db /= f'{_config.Directories._base_name}.db'

        self._path_to_base_files = self._path_to_this_file / _config.Directories._base_files
        self._path_to_CSV_files = self._root_path / _config.Directories.CSVtoSQL
        self._path_to_CreateTables_files = self._root_path / _config.Directories.CreateTables

        # public class attributes
        self.update_all_tables = update_all_tables
        self.update_created_tables = update_created_tables
        self.tables_to_update = tables_to_update
        self.only_use_CSV_files = only_use_CSV_files
        self.today_date = datetime.datetime.now()
        self.min_date = datetime.datetime(1850, 1, 1)
        self.db_modified = False

        # create file structure
        if(not os.path.exists(self._root_path)):
            os.mkdir(self._root_path)
            for sub_dir in _config.Directories._sub_dirs:
                os.mkdir(self._root_path / sub_dir)

            # copy files to directory
            shutil.copy(self._path_to_base_files / 'DatabaseParameters.py', self._root_path)
            shutil.copy(self._path_to_base_files / 'ExampleCreateTable.py', self._path_to_CreateTables_files)

        # add the path to the database parameters
        sys.path.append(str(self._root_path))
        global DBP
        import DatabaseParameters as DBP

        # used to call DB params from script
        self.DBP = DBP

        # used to search DBP params
        DBP_dict = self._db_params_to_dict(DBP)
        [flat_dict] = pd.json_normalize(DBP_dict, sep = '.').to_dict(orient = 'records')
        self._DBP_flat = {}
        for (k, v) in flat_dict.items():
            k = k.replace('.subclasses', '')
            k = k.replace('.attr', '')
            self._DBP_flat[k] = v

        # must specify WRDS username if Tables.WRDS_TABLES is populated
        if(self.DBP.Tables.WRDS_TABLES):
            # wrds tables populated
            self._wrds_username = _util_funcs.rgetattr(self.DBP.Tables, 'WRDS_USERNAME')

        # create sql engine
        self._connectorx_path = 'sqlite:///' + str(self._path_to_db)
        self.sql_engine = sqlalchemy.create_engine('sqlite:///' + str(self._path_to_db))

        #############################################################################################
        # Remove tables from DB

        if(self.update_all_tables or self.update_created_tables or len(self.tables_to_update) > 0):
            # used to update all tables
            if(self.update_all_tables and self._path_to_db.exists()):
                print(_config.ErrorMessage.UPDATING_ALL_TABLES.format(color = _config.bcolors.WARNING))
                inpt = input('Are you sure you want to continue? [y/n]: ')
                if(inpt.strip().lower() == 'y'):
                    print(_config.ErrorMessage.DELETE_DATABASE.format(color = _config.bcolors.INFO))
                    os.remove(self._path_to_db)
                    self.db_modified = True
                else:
                    print(_config.ErrorMessage.ABORT_INIT.format(color = _config.bcolors.FAIL))
                    raise _config.Exceptions.CancelOperation

            # check if any tables that are being updated are origninal tables
            raw_tables = DBP.Tables.WRDS_TABLES + DBP.Tables.CSV_TABLES
            updated_og_tables = [ele for ele in self.tables_to_update if ele in raw_tables]
            if(len(updated_og_tables) != 0):
                print(_config.ErrorMessage.UPDATING_OG_TABLE.format(color = _config.bcolors.WARNING))
                inpt = input(f'Would you like to update all derivative tables? [y/n]: ')
                if(inpt.strip().lower() == 'y'):
                    self.update_created_tables = True

            # create list of tables to delete
            tables_to_delete = self.tables_to_update
            if(self.update_created_tables):
                tables_to_delete += DBP.Tables.CREATED_TABLES

            # list of current tables
            # check to see if all required tables are present, if not load the ones that are missing
            inspect = sqlalchemy.inspect(self.sql_engine)
            self.curr_tables = inspect.get_table_names()

            # delete tables that should be updated
            for table_name in tables_to_delete:
                if(table_name in self.curr_tables):
                    with self.sql_engine.connect() as conn:
                        print(_config.ErrorMessage.DROPPING_TABLE.format(color = _config.bcolors.INFO, 
                                                                         obj = table_name))
                        _ = conn.execute(_config.SQLCommands.DROP_TABLE.format(table = table_name))
                        self.db_modified = True
                        self.curr_tables.remove(table_name)

        ##################################################################################################
        # Add tables to DB

        # reset current tables
        inspect = sqlalchemy.inspect(self.sql_engine)
        self.curr_tables = inspect.get_table_names()
        self.tables_to_clean = []

        # local table names
        local_names_auto_download_tables = [name.replace('.', '_') for name in DBP.Tables.WRDS_TABLES]

        # read in the data from WRDS
        if(self.only_use_CSV_files):
            missing_tables = list(set(local_names_auto_download_tables) - set(self.curr_tables))
            print(_config.ErrorMessage.PLEASE_ADD_CSV.format(
                    color = _config.bcolors.FAIL,
                    obj = missing_tables,
                    path = self._path_to_CSV_files
                )
            )
            raise _config.Exceptions.DatabaseError
        else:
            if(not all(elem in self.curr_tables for elem in local_names_auto_download_tables)):
                missing_tables = list(set(local_names_auto_download_tables) - set(self.curr_tables))
                self.tables_to_clean.extend(missing_tables)
                str_tables = ','.join(missing_tables)
                print(_config.ErrorMessage.MISSING_TABLE.format(
                        color = _config.bcolors.INFO,
                        obj = missing_tables
                    )
                )
                if(not isinstance(DBP.Tables.WRDS_USERNAME, str)):
                    print(_config.ErrorMessage.MISSING_WRDS_USERNAME.format(color = _config.bcolors.FAIL))
                    raise _config.Exceptions.BuildError
                p = subprocess.run(['python3', f'{self._path_to_this_file}/download_script.py', 
                                    self._path_to_db, self._wrds_username, str_tables])
                if(p.returncode == 1):
                    # subprocess crashed
                    print(_config.ErrorMessage.DOWNLOAD_TABLES_CRASH.format(color = _config.bcolors.FAIL))
                    raise _config.Exceptions.BuildError
                self.db_modified = True
                print(_config.ErrorMessage.RAW_WRDS_ADDED.format(color = _config.bcolors.OK))
        
        path_to_zip_folder = self._path_to_CSV_files / f'CSVzip_{self.today_date.date()}_{self.today_date.time()}'

        # check CSV directory for files to include
        directory_contents = os.listdir(self._path_to_CSV_files)
        os.mkdir(path_to_zip_folder)
        with open(path_to_zip_folder / 'README.txt', 'w') as readme:
            readme.write('To unzip files use \'LocalDatabse.LocalDatabase.unzip_csv.')  
            readme.close()
        for csvfile in directory_contents:
            f = os.path.join(self._path_to_CSV_files, csvfile)
            if(os.path.isfile(f)):
                filepath = pathlib.Path(f)
                tablename = filepath.name.strip('.csv')
                comp_file_path = self._path_to_CSV_files / f'{tablename}.zip'
                if(tablename in self.curr_tables): continue
                if(tablename not in DBP.Tables.CSV_TABLES):
                    print(_config.ErrorMessage.UPDATE_DB_PARAMS.format(color = _config.bcolors.WARNING, 
                                                                       obj = tablename))
                    raise _config.Exceptions.BuildError
                s = time.time()
                print(_config.ErrorMessage.CSV_ADD_TABLE.format(color = _config.bcolors.INFO,
                                                               tab = filepath.name,
                                                               db = self._path_to_db.name)
                                                            )
                try:
                    subprocess.call(['sqlite3', f'{self._path_to_db}', 
                                     '.mode csv', 
                                     f'.import {filepath} {tablename}', 
                                     '.mode columns',
                                     '.quit'])
                    self.tables_to_clean.append(tablename)
                except:
                    print(_config.ErrorMessage.CSV_TO_SQL_FAIL.format(color = _config.bcolors.FAIL))
                    raise _config.Exceptions.BuildError

                # compress csv files
                with open(filepath, mode = 'rb') as file_in:
                    with open(comp_file_path, mode = 'wb') as file_out:
                        data = file_in.read()
                        compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
                        file_out.write(compressed_data)
                        file_in.close()
                        file_out.close()
                shutil.copy(comp_file_path, path_to_zip_folder)
                os.remove(filepath)
                os.remove(comp_file_path)
                
                e = time.time()
                print(_config.ErrorMessage.FINISHED_CSV_ADDING_CSV_TABLE.format(
                        color = _config.bcolors.OK,
                        name = filepath.name, 
                        time = str(round(e - s, 3))
                    )
                )
                self.curr_tables.append(tablename)
                self.db_modified = True

        ###########################################################################################################
        # Apply SQL cleaning to all tables

        for table in self.tables_to_clean:
            # apply null to all missing tables
            print(f'Cleaning table: {table}')
            s = time.time()
            df = pd.read_sql(f"""SELECT * FROM {table} LIMIT 1""", con = self.sql_engine)
            columns = list(df.columns)
            for col in columns:
                with self.sql_engine.connect() as conn:
                    _ = conn.execute(_config.SQLCommands.SET_NULL_COL.format(table = table,
                                                                             col = col))
            # apply special cleaning to other tables
            if(table in DBP.Tables.SQL_CLEANING):
                ops_dict = DBP.Tables.SQL_CLEANING[table]
                for (op, cols) in ops_dict.items():
                    if(op not in _config.SQLCommands.SQL_DICT):
                        print(_config.ErrorMessage.INVALID_SQL_CLEANING_OPERATION.format(
                                color = _config.bcolors.FAIL,
                                tab = table
                            ))
                        raise _config.Exceptions.CancelOperation
                    sql_command = _config.SQLCommands.SQL_DICT[op]
                    with self.sql_engine.connect() as conn:
                        for col in cols:
                            _ = conn.execute(sql_command.format(table = table, col = col))
            print(f'{table} clean: {round(time.time() - s, 3)}')

                    

        ###########################################################################################################
        # Add created tables
                        
        for table in DBP.Tables.CREATED_TABLES:
            if(table not in self.curr_tables):
                filename = f'{table}.py'
                s = time.time()
                print(_config.ErrorMessage.BUILDING_TABLE.format(
                        color = _config.bcolors.INFO,
                        tab = table,
                        file = filename
                    )
                )
                p = subprocess.run(['python3', f'{self._path_to_CreateTables_files}/{filename}', self._path_to_db])
                if(p.returncode == 1):
                    # subprocess crashed
                    print(_config.ErrorMessage.CREATE_TABLE_CRASH.format(
                            color = _config.bcolors.FAIL,
                            tab = table
                        )
                    )
                    raise _config.Exceptions.BuildError
                print(_config.ErrorMessage.TABLE_ADDED.format(color = _config.bcolors.OK,
                                                             time = str(round(time.time() - s, 3))
                                                            ))
                self.db_modified = True

        init_end = time.time()
        if(self.db_modified):
            print(_config.ErrorMessage.DATABASE_INITALIZED.format(
                    color = _config.bcolors.OK,
                    time = str(datetime.timedelta(seconds = init_end - init_start))
                )
            )
 
    def __str__(self) -> str:
        #TODO: print tables and columns from loacl database
        return(f"WRDS Username: {self.username}")
        
    def uncompress_csv(path):
        pass

    def raw_sql(self, sql_str):
        """
        Allows the user to use raw SQL on the underlying database.

        Note
        _____
        This can cause irreversible damage to the underlying database that can only be fixed by deleting and reconstructing the database.
        """
        print(_config.ErrorMessage.COMPROMISE_DATABASE.format(color = _config.bcolors.WARNING))
        response = input('Do you wish to continue? [y/n]: ')
        if(response == 'y'):
            raw_df = pd.read_sql(sql_str, con = self.sql_engine)
            return(raw_df)
        else:
            print(_config.ErrorMessage.ABORT_OPERATION.format(
                    color = _config.bcolors.INFO,
                    obj = '<raw_sql>'
                )
            )
            return(None)
        
    def query_DB(self, table_info, **kwargs) -> pd.DataFrame:
        """ Used to query the local database.

        Args: 
            table_info: A DatabaseParameters.Table instance.
            kwargs: Keyword arguments for additional subsetting.

        Returns: 
            A pandas dataframe containg the data quiried from the 
            local database. 
        """

        # dates 
        if('start_date' in kwargs): 
            start_date = kwargs['start_date']
        else:
            start_date = self.min_date

        if('end_date' in kwargs): 
            end_date = kwargs['end_date']
        else:
            end_date = self.today_date

        query_components = self._build_query_components(table_info = table_info, 
                                                        start_date = start_date,
                                                        end_date = end_date,
                                                        kwrd_dict = kwargs
                                                    )
        
        # search for default subsetting
        table_name = str(table_info).replace('<class \'DatabaseParameters.', '')
        table_name = table_name.replace('<class \'DatabaseParameters.', '')
        table_name = table_name.replace('\'>', '')

        reserved_attr = _config.RequiredAttributes.GENERIC_TABLE + _config.RequiredAttributes.RESERVED_ATTR
        additional_defaults = _util_funcs.list_diff(list1 = self._DBP_flat[table_name],
                                                    list2 = reserved_attr
                                                    )
        for default in additional_defaults:
            if('DEFAULT_' in default):
                default_var = default.replace('DEFAULT_', '').lower()
                query_components[default_var] = _util_funcs.rgetattr(table_info, default)
        
        raw_df = self._query_database(query_components)

        # return dataframe
        return(raw_df)

    # done
    def query_IBES(self, 
                   start_date: datetime.datetime, 
                   end_date: datetime.datetime, 
                   **kwargs,
                ) -> pd.DataFrame:
        
        TABLE_INFO = DBP.IBES

        # defualt forecast period indicator
        if(not 'fpi' in kwargs):
            kwargs['fpi'] = TABLE_INFO.DEFAULT_FPI
        else:
            self._check_specific_subset(quiried = kwargs['fpi'], 
                                        valid = TABLE_INFO.VALID_FPI,
                                        func = 'query_IBES'
                                    )
            
        # default meausre
        if(not 'measure' in kwargs):
            kwargs['measure'] = TABLE_INFO.DEFAULT_MEASURES
        else:
            self._check_specific_subset(quiried = kwargs['measure'], 
                                        valid = TABLE_INFO.DEFAULT_MEASURES,
                                        func = 'query_IBES'
                                    )
        
        query_components = self._build_query_components(func = 'query_IBES', 
                                                        table_info = TABLE_INFO, 
                                                        start_date = start_date, 
                                                        end_date = end_date,
                                                        kwrd_dict = kwargs
                                                    )

        dfs_to_concat = []
        for curr_fpi in kwargs['fpi']:
            query_components['fpi'] = curr_fpi
            raw_df = self._query_database(query_components)
            raw_df['fpi'] = curr_fpi
            dfs_to_concat.append(raw_df)
        raw_df = pd.concat(dfs_to_concat)

        # return dataframe
        return(raw_df)

    # done
    def query_riskfree(self, 
                       start_date: datetime.datetime, 
                       end_date: datetime.datetime, 
                       freq: str
                    ) -> pd.DataFrame:
        """
        Query the risk-free rate from the Fama-French library on local WRDS. This rate is equivalent 
        to the 1 month T-Bill rate.

        Parameters
        ___________
        start_date: datetime.datetime\n
            Starting date of the dataset being queried.

        end_date: datetime.datetime\n
            Ending date of the dataset being queried.

        obs_freq: str\n
            The observational frequency of the CRSP database being queried.
                Choices are:
                    * 'D' : daily
                    * 'M' : monthly
                    * 'A' : annually

        Returns
        ________
        full_df: pd.DataFrame\n
            Risk-free rate data.

        Note
        _____
        The dataframe returned makes adjustments for NYSE holidays during compounding.

        Note
        _____
        List of queried CRSP variables:\n
            * date : Date of observation
            * rf   : Risk-free rate
        """
        # Since monthly observations have a date starting on the 1st of each month, then for any 'start_date' that doesn't
        # coincide w/ the 1st of any month, we adjust it so it does and the query pulls the monthly observation of interest.
        if(freq in ['M', 'A'] and start_date != (start_date + pandas.tseries.offsets.MonthBegin(-1)).date()):
            start_date = (start_date + pandas.tseries.offsets.MonthBegin(-1)).date()

        # load in dataframe
        raw_df = pd.read_sql(self._rf1m_SQL_query(start_date, end_date, freq), con = self.sql_engine)

        # convert dates to datetimes
        raw_df['date'] = pd.to_datetime(raw_df['date'])

        # Convert trading dates to end-of-period if 'freq' does not pertain to daily frequency.
        if(freq == 'M'):
            raw_df['date'] = raw_df['date'] + pandas.tseries.offsets.MonthEnd(0)
        elif(freq == 'A'):
            raw_df['date'] = raw_df['date'] + pandas.tseries.offsets.YearEnd(0)

        # return the raw dataframe
        return(raw_df)

    # done
    def query_CRSPCompMap(self) -> pd.DataFrame:
        """
        Query the CRSP/Compustat (CCM) Merged Linking Table needed to merge CRSP securities to
            Compustat companies on permno and gvkey.

        Returns
        ________
        raw_df: pd.DataFrame\n
            The raw dataframe pulled from local WRDS database.

        Note
        _____
        Currently this function only works if a local copy of the WRDS database exits w/ the CCM Linktable.
        """
        sql_str = """
                    SELECT gvkey, lpermno as permno, lpermco as permco, linktype, linkprim, linkdt, linkenddt
                    FROM CRSP_CCMXPF_LINKTABLE
                    WHERE substr(linktype, 1, 1) = 'L'
                    AND (linkprim = 'C' or linkprim = 'P')
                  """

        # read in raw dataframe from local database
        raw_df = pd.read_sql(sql_str, con = self.sql_engine)

        # if linkenddt is missing the set to todays date
        raw_df.linkenddt = raw_df.linkenddt.fillna(pd.to_datetime('today').date())

        # convert to the correct data type
        raw_df = raw_df.astype(DBP.WRDS.CCMLinks.VARS_DATA_TYPE)

        # return the raw dataframe
        return(raw_df)

# ----------------------------------------------------------------------------------------------------------------------------
# INTERNAL METHODS (class <QueryWRDS>)
#
# These are internal methods and should only be called within this class. Functionality and accuracy of these methods cannot
# garunteed if they are called outside of this class.
# ----------------------------------------------------------------------------------------------------------------------------

    def _list_to_sql_str(self, lst: list, table: str = None) -> str:
        res = ''
        for var in lst:
            if(table is None):
                res += f'\'{var}\', '
            else:
                res += f'{table}.{var}, '
        res = res[:-2]
        return(res)
                    
    def _rf1m_SQL_query(self, start_date: datetime.datetime, end_date: datetime.datetime, obs_freq: str) -> str:
        """
        INTERNAL METHOD: Create SQL string used to query the Fama-French risk free rate
                            listed on WRDS CRSP in the FF library. This rate is the
                            1 month T-Bill rate.

        Parameters
        ___________
        start_date: str\n
            Starting date for the data being queried.

        end_date: str\n
            Ending date for the data being queried.

        obs_freq: str\n
            The observational frequency of the CRSP delisting database being queried.
                Choices are:
                    * 'D' : daily
                    * 'M' : monthly
                    * 'A' : annual

        Returns
        ________
        sql_str : str\n
            String containing the SQL code used to query the risk free rate in the
                Fama-French (FF) library on CRSP/WRDS database.

        Note
        _____
        Depending on the observational frequency (obs_freq) given the compounding of the
            risk-free rate changes.
        """
        # convert date time object to strings for the SQL query
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str  = end_date.strftime('%Y-%m-%d')

        # Depending on the frequency supplied the compounding changes
        if(obs_freq == 'D'):
            sql_1 = 'strftime(\'%d\', LEAD(date) OVER (ORDER BY date)) - strftime(\'%d\', date) AS diff'
            sql_2 = 'rf AS cumrf'
            library = 'FF_FACTORS_DAILY'
        elif(obs_freq == 'M'):
            sql_1 = 'strftime(\'%m\', LEAD(date) OVER (ORDER BY date)) - strftime(\'%m\', date) AS diff'
            sql_2 = 'rf AS cumrf'
            library = 'FF_FACTORS_MONTHLY'
        elif(obs_freq == 'A'):
            sql_1 = 'strftime(\'%Y\', LEAD(date) OVER (ORDER BY date)) - strftime(\'%Y\', date) AS diff'
            sql_2 = 'EXP(SUM(LN(1 + rf)) OVER (PARTITION BY strftime(\'%Y\', date))) - 1 AS cumrf'
            library = 'FF_FACTORS_MONTHLY'
        else:
            print(f'{_config.bcolors.FAIL}No valid observational frequency given.{_config.bcolors.ENDC}')
            raise _config.Exceptions.QueryingError

        sql_dic = {'sql_1' : sql_1, 'sql_2' : sql_2, 'library' : library, 'start_date' : '\'' + start_date_str + '\'', 'end_date' : '\'' + end_date_str + '\''}
        sql_str = """
                    SELECT date, rf
                    FROM (
                        SELECT date, {0}, rf, {1}
                        FROM {2}
                        WHERE date BETWEEN {3} AND {4}
                    ) AS crsp_rf
                    WHERE diff != 0 OR diff IS NULL
                  """.format(sql_dic['sql_1'], sql_dic['sql_2'], sql_dic['library'], sql_dic['start_date'], sql_dic['end_date'])
        return(sql_str)
    
    def _build_query_components(self,
                                table_info, 
                                start_date: datetime.datetime, 
                                end_date: datetime.datetime, 
                                kwrd_dict: dict[str:list|int|str|float]
                            ) -> dict[str|list]:
        
        query_components = {'table_info': table_info, 
                            'start_date': start_date, 
                            'end_date': end_date}
        
        # variables to query for
        query_vars = self._format_query_vars(kwrd_dict = kwrd_dict,
                                             table_info = table_info
                                            )
        query_components['vars'] = query_vars
        
        # additional subsetting
        add_subsetting = _util_funcs.list_diff(list(kwrd_dict.keys()), _config.KeywordArguments.QUERY_VARS)
        for kwrd in add_subsetting:
            val = kwrd_dict[kwrd]
            if(isinstance(val, str) or isinstance(val, float) or isinstance(val, int)):
                val = [val]
            elif(isinstance(val, list)):
                pass
            else:
                print(_config.ErrorMessage.INVALID_COMPONENT_TYPE.format(
                        color = _config.bcolors.FAIL,
                        obj = kwrd, 
                    )
                )
                raise _config.Exceptions.QueryingError

            query_components[kwrd] = val

        return(query_components)   
    
    def _format_query_vars(self, 
                           kwrd_dict: dict[str:list|str], 
                           table_info
                           ) -> list[str]:
        
        # get specific table info
        default_id = table_info.DEFAULT_ID
        default_date = table_info.DEFAULT_DATE
        default_vars = table_info.DEFAULT_VARS

        # if not all variables are specified then cannot error check
        valid_vars = None 
        if(_util_funcs.rhasattr(table_info, 'ALL_VARS')):
            if(table_info.ALL_VARS):
                valid_vars = list(table_info.VARS_DATA_TYPE.keys())
        
        # keywrods 'additional_vars' and 'vars' cannot be used simultaneously
        if('vars' in kwrd_dict and ('add_vars' in kwrd_dict or 'sub_vars' in kwrd_dict)): 
            print(_config.ErrorMessage.ADDVARS_VARS_KWRDS.format(color = _config.bcolors.FAIL))
            raise _config.Exceptions.QueryingError
        
        # create list of the variables being quireied 
        query_vars = default_vars
        if('vars' in kwrd_dict):
            # variable arguments to query for
            query_vars = kwrd_dict['vars']

            # check if database has no must have identifier
            if(not default_id is None):
                if(default_id not in query_vars): 
                    query_vars.insert(0, default_id)

            # add date if people forgot
            if(not default_date is None):
                if(default_date not in query_vars): 
                    query_vars.insert(0, default_date)
        else:
            if('add_vars' in kwrd_dict):
                query_vars = default_vars + _util_funcs.convert_to_list(kwrd_dict['add_vars'])

            if('sub_vars' in kwrd_dict):
                sub_vars = _util_funcs.convert_to_list(kwrd_dict['sub_vars'])
                query_vars = _util_funcs.list_diff(default_vars, sub_vars)
            
        if('all_vars' in kwrd_dict): 
            if(kwrd_dict['all_vars']):
                query_vars = valid_vars

        # make sure subsetting vars are also quired for
        if(kwrd_dict):
            query_vars += _util_funcs.list_diff(list1 = list(kwrd_dict.keys()), 
                                               list2 = _config.KeywordArguments.QUERY_VARS
                                            )
            
        # remove deuplicates
        query_vars = list(dict.fromkeys(query_vars))

        # final check of valid query vars
        if(not self._all_valid(query_vars, valid_vars)):
            print(_config.ErrorMessage.VAR_CANNOT_BE_QUERIED.format(
                    color = _config.bcolors.FAIL,
                    obj = str(_util_funcs.list_diff(query_vars, valid_vars)),
                    tab = table_info.TABLE
                )
            )

        return(query_vars)
    
    def _all_valid(self, quiried: list, valid: list | None) -> bool:
        if(valid is None): return(True)
        all_valid = all(elem in valid for elem in quiried)
        return(all_valid)
    
    def _query_database(self, 
                        query_components: dict[str:datetime.datetime|str|float|int|list[str|float|int]|bool]
                    ) -> pd.DataFrame:

        # get table info
        TABLE_INFO = query_components['table_info']
        VARS_DATA_TYPE = TABLE_INFO.VARS_DATA_TYPE
        DEFAULT_ID = TABLE_INFO.DEFAULT_ID
        DEFAULT_DATE = TABLE_INFO.DEFAULT_DATE

        # get data types that are being quired for
        query_vars = query_components['vars']
        query_dtype = {k:v for (k, v) in VARS_DATA_TYPE.items() if k in query_vars}

        # read in raw dataframe from local sql database
        raw_df = pd.read_sql(self._sql_query(query_components),
                             con = self.sql_engine
                            )    

        '''
        # read in raw dataframe from local sql database
        raw_df = connectorx.read_sql(self._internal_db_path, self._sql_query(query_components))
        '''

        # make all columns lower case
        cols = raw_df.columns
        cols = [col.lower() for col in cols]
        raw_df.columns = cols  

        # set data types
        raw_df = raw_df.astype(query_dtype)

        # replace and python objects 'None' to np.nan
        raw_df = raw_df.fillna(value = np.nan)

        # reset to original variables, drop duplicates, and reset the index
        raw_df = raw_df[query_vars]
        raw_df = raw_df.drop_duplicates()
        sorting_dims = []
        if(DEFAULT_ID is not None):
            sorting_dims.append(DEFAULT_ID)
        if(DEFAULT_DATE is not None):
            sorting_dims.append(DEFAULT_DATE)
        raw_df = raw_df.sort_values(by = sorting_dims)
        raw_df = raw_df.reset_index(drop = True)

        return(raw_df)
    
    def _sql_query(self, 
                   query_components: dict[str:datetime.datetime|str|float|int|list[str|float|int]|bool]
                ) -> str:

        REQUIRED_QUERY_COMPONENTS = _config.QueryComponents.COMPONENTS
        
        # check for required components
        missing_required = _util_funcs.list_diff(REQUIRED_QUERY_COMPONENTS, list(query_components.keys()))
        if(len(missing_required) > 0):
            print(_config.ErrorMessage.MISSING_REQUIRED_SQL_COMPONENTS.format(
                    color = _config.bcolors.FAIL,
                    obj = missing_required
                )
            )
            raise _config.Exceptions.QueryingError
        
        table_info, start_date, end_date, vars = list(map(query_components.get, REQUIRED_QUERY_COMPONENTS))

        # get specific table information
        table = table_info.TABLE
        date_var = table_info.DEFAULT_DATE

        # convert date time object to strings for the SQL query
        start_date_str = '\'' + start_date.strftime('%Y-%m-%d') + '\''
        end_date_str  = '\'' + end_date.strftime('%Y-%m-%d') + '\''

        # create argument string
        var_str = self._list_to_sql_str(vars, table)
        sql_str = f'SELECT {var_str} FROM {table} WHERE {date_var} BETWEEN {start_date_str} AND {end_date_str}'

        # additional subsetting
        additonal_sub = _util_funcs.list_diff(list1 = list(query_components.keys()), 
                                             list2 = REQUIRED_QUERY_COMPONENTS)
        for col in additonal_sub:          
            sql_str += f' AND {col} IN ({self._list_to_sql_str(query_components[col])})'

        return(sql_str)
     
    def _db_params_to_dict(self, db_params):
        # Steps:
        # (1) check for mandatory 'Tables' class
        # (2) Iterate through all classes
        name_dic = dict([(name, cls) for name, cls in db_params.__dict__.items() if isinstance(cls, type)])

        # mandatory tables class
        if('Tables' not in name_dic.keys()):
            print(_config.ErrorMessage.NO_TABLES_CLASS_IN_DBP.format(color = _config.bcolors.FAIL))
            raise _config.Exceptions.DatabaseError
        
        # validate that tables has the correct attributes
        table_attr = self._list_class_attr(DBP.Tables)
        if(not all(attr in table_attr for attr in _config.RequiredAttributes.TABLES)):
            missing_required = _util_funcs.list_diff(_config.RequiredAttributes.TABLES, table_attr)
            print(_config.ErrorMessage.REQUIRED_ATTRIBUTES_MISSING.format(
                    color = _config.bcolors.FAIL,
                    tab = 'Tables',
                    attr = missing_required
                )
            )
            raise _config.Exceptions.DatabaseError
        
        # iterate through classes not Tables
        del name_dic['Tables']
        DBP_dict = {}
        for (name, cls) in name_dic.items():
            DBP_dict[name] = self._build_dict(name, cls)
        return(DBP_dict)

    def _build_dict(self, curr_name, curr_cls):
        dic = dict()
        dic['subclasses'] = dict()
        dic['attr'] = self._list_class_attr(curr_cls)
        subclasses = dict([(name, cls) for name, cls in curr_cls.__dict__.items() if isinstance(cls, type)])
        if(subclasses):
            # sublcasses present
            for (cls_name, cls_inst) in subclasses.items():
                dic['subclasses'][cls_name] = self._build_dict(cls_name, cls_inst)
        else:
            # no subclasses, check for required attributes
            if(not all(attr in dic['attr'] for attr in _config.RequiredAttributes.GENERIC_TABLE)):
                missing_required = _util_funcs.list_diff(_config.RequiredAttributes.GENERIC_TABLE, dic['attr'])
                print(_config.ErrorMessage.REQUIRED_ATTRIBUTES_MISSING.format(
                        color = _config.bcolors.FAIL,
                        tab = curr_name,
                        attr = missing_required
                    )
                )
                raise _config.Exceptions.DatabaseError
        return(dic)

    def _list_class_attr(self, cls):
        keys = list(cls.__dict__.keys())
        res = [key for key in keys if not key.startswith('_')]
        return(res)
    




            


