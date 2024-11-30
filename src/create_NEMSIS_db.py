import sqlite3
from constants import table_definitions as tbl_defs
from constants import paths


"""
This script creates the data/NEMSIS_PUB.db sqlite database to store
data for further analysis. 

See constants/table_definitions.py for the SQL used to create each table
"""
def main():
    # create sqlite .db object to store database
    conn = sqlite3.connect(paths.db_path) 
    cursor = conn.cursor()

    # iterate over each item in the table_definitions, create table
    for table_name, create_table_sql in tbl_defs.table_definitions.items():
        cursor.execute(create_table_sql)
    
    # commit changes then close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
