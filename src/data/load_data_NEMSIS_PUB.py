import sqlite3
import csv
import os
import re


conn = sqlite3.connect('../db/NEMSIS_PUB.db')
cursor = conn.cursor()

file_column_mapping = {
    'ComputedElements.txt': "PcrKey'~|~'USCensusRegion'~|~'USCensusDivision'~|~'NasemsoRegion'~|~'Urbanicity'~|~'ageinyear'~|~'EMSDispatchCenterTimeSec'~|~'EMSChuteTimeMin'~|~'EMSSystemResponseTimeMin'~|~'EMSSceneResponseTimeMin'~|~'EMSSceneTimeMin'~|~'EMSSceneToPatientTimeMin'~|~'EMSTransportTimeMin'~|~'EMSTotalCallTimeMin'",
    'FACTPCRARRESTROSC.txt': "PcrKey'~|~'eArrest_12'",
    'FACTPCRARRESTWITNESS.txt': "PcrKey'~|~'eArrest_04'",
    'FACTPCRMEDICATION.txt': "eMedications_01'~|~'PcrMedicationKey'~|~'PcrKey'~|~'eMedications_03'~|~'eMedications_03Descr'~|~'eMedications_05'~|~'eMedications_06'~|~'eMedications_07'~|~'eMedications_10'~|~'eMedications_02'",
    'Pub_PCRevents.txt': "PcrKey'~|~'eDispatch_01'~|~'eDispatch_02'~|~'eArrest_14'~|~'eArrest_01'~|~'eArrest_02'~|~'eArrest_05'~|~'eArrest_07'~|~'eArrest_11'~|~'eArrest_16'~|~'eArrest_18'~|~'eDisposition_12'~|~'eDisposition_19'~|~'eDisposition_16'~|~'eDisposition_21'~|~'eDisposition_22'~|~'eDisposition_23'~|~'eOutcome_01'~|~'eOutcome_02'~|~'ePatient_13'~|~'ePatient_15'~|~'ePatient_16'~|~'ePayment_01'~|~'ePayment_50'~|~'eResponse_05'~|~'eResponse_07'~|~'eResponse_15'~|~'eResponse_23'~|~'eScene_01'~|~'eScene_06'~|~'eScene_07'~|~'eScene_08'~|~'eScene_09'~|~'eSituation_02'~|~'eSituation_07'~|~'eSituation_08'~|~'eSituation_13'~|~'eSituation_01'~|~'eTimes_01'~|~'eTimes_03'~|~'eTimes_05'~|~'eTimes_06'~|~'eTimes_07'~|~'eTimes_09'~|~'eTimes_11'~|~'eTimes_12'~|~'eTimes_13'~|~'eDisposition_17'"
}

def create_and_load_table(file_path, column_names_str):
    try:
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        column_names = [col.strip("'") for col in column_names_str.split("'~|~'")]
        create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {", ".join([f"{col} TEXT" for col in column_names])},
                PRIMARY KEY (PcrKey) 
            )
        """
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
                update_columns = ', '.join([f"{col} = excluded.{col}" for col in column_names if col != 'PcrKey'])
                insert_sql = f"""
                    INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})
                    ON CONFLICT (PcrKey) DO UPDATE SET 
                        {update_columns}
                """
                cursor.execute(insert_sql, row)
        conn.commit()
        print(f"Data from '{file_path}' loaded into table '{table_name}'")
    except Exception as e:
        print(f"Error processing '{file_path}': {e}")

for file_name, column_names in file_column_mapping.items():
    file_path = os.path.join('~/../../work/DS5110-911/911/', file_name)
    expanded_file_path = os.path.expanduser(file_path)
    create_and_load_table(expanded_file_path, column_names)
conn.close()
