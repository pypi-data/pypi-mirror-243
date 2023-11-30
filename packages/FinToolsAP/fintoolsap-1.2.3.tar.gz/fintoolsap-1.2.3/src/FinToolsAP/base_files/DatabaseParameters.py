# every table must have 'TABLE', 'DEFAULT_VARS', 'VARS_DATA_TYPE', 'DEFAULT_ID', 'DEFAULT_DATE'

class Tables:

    WRDS_USERNAME = None

    # list of tables to download from WRDS
    WRDS_TABLES = [] 

    # list of tables to read in from CSV
    CSV_TABLES = []

    # list of created tables using scripts in CreateTables/
    CREATED_TABLES = []
    
    # operations to apply to 
    SQL_CLEANING = {}
    
class YourCustomTableNmaeExample:
    # fille this out with your own table information

    TABLE = None
    DEFAULT_VARS = []
    VARS_DATA_TYPE = {}
    DEFAULT_ID = None
    DEFAULT_DATE = None

class DataVendorExample:

    class VendorTable1Example:
        TABLE = None
        DEFAULT_VARS = []
        VARS_DATA_TYPE = {}
        DEFAULT_ID = None
        DEFAULT_DATE = None


    class VendorTable2Example:
        TABLE = None
        DEFAULT_VARS = []
        VARS_DATA_TYPE = {}
        DEFAULT_ID = None
        DEFAULT_DATE = None