import sqlite3
from constants import table_definitions as tbl_defs
from constants import paths

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
