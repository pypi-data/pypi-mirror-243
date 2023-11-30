# DO NOT MODIFY

import sys
import pathlib
import sqlalchemy

PATH_TO_DB = sys.argv[1]
WRDS_USERN = sys.argv[2]
STR_TABLES = sys.argv[3]

sys.path.append(str(pathlib.Path(PATH_TO_DB).parent))
import DatabaseParameters as DBP

sql_engine = sqlalchemy.create_engine('sqlite:///' + str(PATH_TO_DB))

############################################################################
# Your Code Below

import wrds
import time

missing_tables = STR_TABLES.split(',')
WRDS_db = wrds.Connection(username = WRDS_USERN)
for table_name in missing_tables:
    table = table_name.replace('_', '.', 1)
    print(f'Downloading {table} from WRDS')
    s = time.time()
    sql_str = f"""SELECT * FROM {table}"""
    # download the data to a dataframe
    df = WRDS_db.raw_sql(sql_str)
    # write the dataframe to the local sql database
    df.to_sql(table_name, con = sql_engine, if_exists = 'replace', index = False)
    e = time.time()
    print(f'Finished {table_name}: {round(e - s, 3)}s')
