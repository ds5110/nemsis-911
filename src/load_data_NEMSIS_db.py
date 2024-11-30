import sqlite3
import os
from constants import file_column_mapping as file_map
from constants import paths


"""
This method loads a given table to the NEMSIS_PUB.db sqlite database

@param - file_path, the file path for the interim text file being reviewed
@param - column_names_str, the string with all column names, from constants/file_column_mapping.py
@param - conn, connection to sqlite database
@param - cursor, cursor to sqlite database connection
"""
def load_table(file_path, column_names_str, conn, cursor):
    try:
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        column_names = [col.strip("'") for col in column_names_str.split("'~|~'")]
        primary_key = 'PcrMedicationKey' if table_name == 'FACTPCRMEDICATION' else 'PcrKey'

        with open(file_path, 'r', encoding='utf-8') as file:
            next(file, None)
            for line in file:
                line = line.strip()
                row = [field.strip() for field in line.split('~|~')]
                if len(row) != len(column_names):
                    print(f"Skipping row with mismatched columns in {table_name}: {row}")
                    continue
                placeholders = ', '.join(['?'] * len(column_names))
                update_columns = ', '.join([f"{col} = excluded.{col}" for col in column_names if col != primary_key])
                insert_sql = f""" INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})
                                  ON CONFLICT ({primary_key}) DO UPDATE SET {update_columns}"""
                cursor.execute(insert_sql, row)
        conn.commit()
        print(f"Data from '{file_path}' loaded into table '{table_name}'")
    except Exception as e:
        print(f"Error processing '{file_path}': {e}")


def main():
    # create connection and cursor for sqlite database
    conn = sqlite3.connect(paths.db_path)
    cursor = conn.cursor()

    # iterate over each file in constant map, adding into database
    for file_name, column_names in file_map.file_column_mapping.items():
        file_path = os.path.join(paths.interim_path, file_name)
        load_table(file_path, column_names, conn, cursor)

    # close connection
    conn.close()

if __name__ == "__main__":
    main()
