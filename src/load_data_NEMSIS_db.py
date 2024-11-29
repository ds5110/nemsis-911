import sqlite3
import os
from constants import file_column_mapping as file_map
from constants import paths

conn = sqlite3.connect(paths.db_path)
cursor = conn.cursor()

def create_and_load_table(file_path, column_names_str):
    try:
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        column_names = [col.strip("'") for col in column_names_str.split("'~|~'")]
        primary_key = 'PcrMedicationKey' if table_name == 'FACTPCRMEDICATION' else 'PcrKey'
        create_table_sql = f""" CREATE TABLE IF NOT EXISTS {table_name} (
                                {", ".join([f"{col} TEXT" for col in column_names])},
                                PRIMARY KEY ({primary_key}))"""
        cursor.execute(create_table_sql)
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

    

    for file_name, column_names in file_map.file_column_mapping.items():
        file_path = os.path.join(paths.interim_path, file_name)
        create_and_load_table(file_path, column_names)

if __name__ == "__main__":
    main()
