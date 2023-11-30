class Directories:

    CreateTables = 'CreateTables'
    CSVtoSQL = 'CSVtoSQL'

    _base_name = 'Database'
    _sub_dirs = [CSVtoSQL, CreateTables]
    _base_files = 'base_files'

class RequiredAttributes:

    TABLES = ['WRDS_TABLES', 'CREATED_TABLES', 'CSV_TABLES', 'WRDS_USERNAME']

    GENERIC_TABLE = ['TABLE', 'VARS_DATA_TYPE', 'DEFAULT_VARS', 'DEFAULT_DATE', 'DEFAULT_ID']

    RESERVED_ATTR = ['ALL_VARS', 'DEFAULT_STOCK_ID']

class KeywordArguments:

    QUERY_VARS = ['vars', 'add_vars', 'sub_vars', 'all_vars', 'start_date', 'end_date']

class QueryComponents:

    COMPONENTS = ['table_info', 'start_date', 'end_date', 'vars']

class SQLCommands:

    DROP_TABLE = """DROP TABLE {table}"""

    DROP_NULL_ROW = """DELETE FROM {table} WHERE {col} IS NULL OR trim({col}) = ''"""

    UPPER_CASE_COLUMN = """UPDATE {table} SET {col} = UPPER({col})"""

    SET_NULL_COL = """UPDATE {table} SET {col} = NULLIF({col}, '')"""

    SQL_DICT = {'drop_null_row': DROP_NULL_ROW, 'upper_col': UPPER_CASE_COLUMN}

class bcolors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OK = '\033[92m'
    INFO = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ErrorMessage:
    """ Defines custom error messages
    """

    MISSING_WRDS_USERNAME = ('{color}Wharton Research Data Services (WRDS) username not given in <DatabaseParameters.Tables>. Please update your WRDS username to download files from WRDS.'\
                            'If you do not want to download tables from WRDS set the attribute <DatabaseParameters.Tables.WRDS_TABLES> to the empty list.') + bcolors.ENDC

    DATABASE_INITALIZED = '{color}Databse has been initalized! {time}s' + bcolors.ENDC

    DOWNLOAD_TABLES_CRASH = '{color}An error has occured while downloading tables form WRDS. Normally this is a result of a lack of memory resources.' + bcolors.ENDC

    CREATE_TABLE_CRASH = '{color}The subporcess used to create table {tab} has failed.' + bcolors.ENDC

    NO_TABLES_CLASS_IN_DBP = '{color}\'Tables\' must be included in the \'DatabaseParameters.py\' file.' + bcolors.ENDC

    REQUIRED_ATTRIBUTES_MISSING = '{color}Class \'{tab}\' is missing the required attributes {attr}.' + bcolors.ENDC

    DROP_NULL_ROWS_FAIL = '{color}An error occured wile removing null rows for table {obj} and column {col}' + bcolors.ENDC

    IDTYPE_AND_IDS = '{color}When querying for a specific asset both keyword arguments \'id_type\' and \'ids\' must be specified.' + bcolors.ENDC

    IDS_EMPTY = '{color}\'ids\' keyowrd argument given an empty list.' + bcolors.ENDC

    ADDVARS_VARS_KWRDS = '{color}Keywrod Arguments \'add_vars\' or \'sub_vars\' and \'vars\' cannot be used simultaneously' + bcolors.ENDC

    UPDATING_ALL_TABLES = '{color}Updating all of the tables in the local database. This process could take a long time...' + bcolors.ENDC

    MISSING_TABLE = '{color}The following tables are missing from the local database: {obj}. Querying WRDS to add them to the local database.' + bcolors.ENDC

    CCM_NOT_ALL_VARS = '{color}Variables {obj} cannot be queried from the combined CRSP/Compustat merged table. The CCM table does not contain all of the variables that are in CRSP and Compustat.' + bcolors.ENDC

    VAR_CANNOT_BE_QUERIED = '{color}Variables {obj} cannot be queried/used for subsetting from {tab}. Check to make sure all varibales are correct.' + bcolors.ENDC

    INVALID_FREQ = '{color}Invlaid frequency {freq} given to {func}' + bcolors.ENDC

    ABORT_INIT = '{color}Aborting database initalization' + bcolors.ENDC

    RAW_WRDS_ADDED = '{color}Raw WRDS files have been added to the local databse.' + bcolors.ENDC

    TABLE_ADDED = '{color}Table added: {time}s' + bcolors.ENDC

    BUILDING_TABLE = '{color}Creating table {tab} using {file}...' + bcolors.ENDC

    PLEASE_ADD_CSV = ('{color}The following tables are missing from the local database: {obj}.'\
                       'Please add the corresponding .csv files into the folder {path}') + bcolors.ENDC

    UPDATE_DB_PARAMS = ('{color}Please make sure that you update the \'database_parameters.py\' file.'\
                        '{obj} is not in the list of csv tables under <class WRDSTables.CSV_TABLES>.') + bcolors.ENDC

    DROPPING_TABLE = '{color}Dropping table {obj} from database' + bcolors.ENDC

    DELETE_DATABASE = '{color}Deleting database' + bcolors.ENDC

    CSV_TO_SQL_FAIL = '{color}Adding CSV to SQL database has failed' + bcolors.ENDC

    ABORT_OPERATION = '{color}{obj} operation aborted' + bcolors.ENDC

    COMPROMISE_DATABASE = ('{color}The operation that you are about to perform might compromise the local database.'\
                           'Operation of the <QueryWRDS> class might be affected.') + bcolors.ENDC
    
    ADD_TABLE_TO_DB_FAIL = '{color}While adding table ({obj}) to the database an error occured. Aborting database initialization.' + bcolors.ENDC
    
    UPDATING_CREATED_TABLES = '{color}Updating derivative tables...' + bcolors.ENDC

    UPDATING_OG_TABLE = '{color}You are updating a original data file used to make some derivative tables.' + bcolors.ENDC

    CONFIRM_DELETE = '{color}Are you sure you want to delete the following tables {obj}' + bcolors.ENDC

    MISSING_REQUIRED_SQL_COMPONENTS = '{color}The following required sql component is missing. {obj}' + bcolors.ENDC

    INVALID_COMPONENT_TYPE = '{color}Only objects of type \'int\', \'float\', \'str\', or \'list\' can be passed as a component. Check subsetting for value {obj}' + bcolors.ENDC

    INVALID_INTERPRETER = '{color}Must use a version of python3.' + bcolors.ENDC

    INVALID_SQL_CLEANING_OPERATION = '{color}The table {tab} has been givne an invlaid operation in \'DatabaseParameters.Tables.SQL_CLEANING\'.' + bcolors.ENDC

    CSV_ADD_TABLE = '{color}Adding {tab} to SQL database {db}...' + bcolors.ENDC

    FINISHED_CSV_ADDING_CSV_TABLE = '{color}Finished {name}: {time}s' + bcolors.ENDC

class Exceptions:

    class QueryingError(Exception):
        pass

    class DatabaseError(Exception):
        pass

    class CancelOperation(Exception):
        pass

    class TestingError(Exception):
        pass

    class BuildError(Exception):
        pass

    class InterpreterError(Exception):
        pass