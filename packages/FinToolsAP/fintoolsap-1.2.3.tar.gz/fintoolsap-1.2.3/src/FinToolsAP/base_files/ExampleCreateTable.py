"""
This is an example file that is used to create a table in
the database. Everything above the pound-line should not be modified.
Insert your code below the line to create a table. Remeber to update 
DatabaseParamters.py file with every new table that you create. 
"""

# DO NOT MODIFY

import sys
import pathlib
import sqlalchemy

PATH_TO_DB = sys.argv[1]

sys.path.append(str(pathlib.Path(PATH_TO_DB).parent))
import DatabaseParameters as DBP

sql_engine = sqlalchemy.create_engine('sqlite:///' + str(PATH_TO_DB))

############################################################################
# Your Code Below

import pandas as pd

# read data from the database using sql, for example
#df = pd.read_sql("""SQL QUERY""", con = sql_engine)


#df.to_sql(Tablename, con = sql_engine, if_exists = 'replace', index = False)