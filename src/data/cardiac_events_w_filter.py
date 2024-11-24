import pandas as pd
import sqlite3
import time
from datetime import datetime
import os

def analyze_cardiac_arrest_events(conn, eArrest_codes_01, eArrest_codes_02, eArrest_codes_03, eResponse_codes, eDisposition_codes):
    cursor = conn.cursor()
    query = """ SELECT 
                    T1.PcrKey,                      -- unique identifier
                    T1.eArrest_01,                  -- Cardiac Arrest Event
                    T2.eArrest_02,                  -- Injury Reported
                    T2.eResponse_05,                -- Not a 911 Scene
                    T2.eDisposition_12,             -- Did not Trans or Terminate
                    T3.eArrest_03,                  -- CPR Performed by EMS
                    T4.ageinyear,                   -- Patient < 18
                    T4.EMSSystemResponseTimeMin,    -- EMS Reponse Time > 60 Min
                    T4.Urbanicity                   -- Where homeboy lives
                FROM Pub_PCRevents AS T1
                JOIN Pub_PCRevents AS T2 ON T1.PcrKey = T2.PcrKey 
                LEFT JOIN FACTPCRARRESTRESUSCITATION AS T3 ON T1.PcrKey = T3.PcrKey
                LEFT JOIN ComputedElements AS T4 ON T1.PcrKey = T4.PcrKey 
                WHERE T1.eArrest_01 IN (?, ?)"""

    cursor.execute(query, eArrest_codes_01)
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    print(df.shape)
    print(df.columns)
    print(df.dtypes)
    removed = {
        'missing_data': 0,
        'cpr': 0,
        'age': 0,
        'response_time': 0,
        'not_911': 0,
        'transport': 0,
        'injury': 0
    }
    filtered_df = {}
    total_cardiac_arrests = len(df)
    df_filtered = df.copy()
    cols_to_convert = ['PcrKey', 'eArrest_01', 'eArrest_02', 'eResponse_05', 'eDisposition_12', 'eArrest_03',
       'ageinyear', 'EMSSystemResponseTimeMin']

    for col in cols_to_convert:
        df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce')
    print(df.dtypes)
    
    # CPR Performed by EMS
    removed['cpr'] = len(df_filtered) - len(df_filtered[df_filtered['eArrest_03'].isin(eArrest_codes_03)]) 
    df_filtered = df_filtered[df_filtered['eArrest_03'].isin(eArrest_codes_03)] # Keep CPR records
    filtered_df['cpr'] = len(df_filtered)

    # Age < 18
    removed['age'] = len(df_filtered) - len(df_filtered[df_filtered['ageinyear'] >= 18])
    df_filtered = df_filtered[df_filtered['ageinyear'] >= 18]
    filtered_df['age'] = len(df_filtered) 

    # EMS Response Time > 60 Minutes
    removed['response_time'] = len(df_filtered) - len(df_filtered[df_filtered['EMSSystemResponseTimeMin'] <= 60])
    df_filtered = df_filtered[df_filtered['EMSSystemResponseTimeMin'] <= 60] 
    filtered_df['response_time'] = len(df_filtered)

    # Not a 911 (Scene) Response 
    removed['not_911'] = len(df_filtered) - len(df_filtered[df_filtered['eResponse_05'].isin(eResponse_codes)])
    df_filtered = df_filtered[df_filtered['eResponse_05'].isin(eResponse_codes)] 
    filtered_df['not_911'] = len(df_filtered) 

    # Unit Did Not Transport or Terminate Resuscitation
    removed['transport'] = len(df_filtered) - len(df_filtered[df_filtered['eDisposition_12'].isin(eDisposition_codes)])
    df_filtered = df_filtered[df_filtered['eDisposition_12'].isin(eDisposition_codes)]
    filtered_df['transport'] = len(df_filtered)

    # Injury Reported
    removed['injury'] = len(df_filtered) - len(df_filtered[~df_filtered['eArrest_02'].isin(eArrest_codes_02)])
    df_filtered = df_filtered[~df_filtered['eArrest_02'].isin(eArrest_codes_02)] # Keep records NOT in the list
    filtered_df['injury'] = len(df_filtered)

    # Missing Data Removal - Apply this last
    missing_data_mask = (
    df_filtered[['eArrest_03', 'ageinyear', 'eResponse_05', 'eDisposition_12', 'eArrest_02', 'EMSSystemResponseTimeMin', 'Urbanicity']].isnull() 
    | df_filtered[['eArrest_03', 'ageinyear', 'eResponse_05', 'eDisposition_12', 'eArrest_02', 'EMSSystemResponseTimeMin', 'Urbanicity']].eq('') 
    | df_filtered[['eArrest_03', 'ageinyear', 'eResponse_05', 'eDisposition_12', 'eArrest_02', 'EMSSystemResponseTimeMin', 'Urbanicity']].eq('          ')
    | df_filtered[['eArrest_03', 'ageinyear', 'eResponse_05', 'eDisposition_12', 'eArrest_02', 'EMSSystemResponseTimeMin', 'Urbanicity']].isin([7701001, 7701003]) 
    ).any(axis=1)
    removed['missing_data'] = len(df_filtered[missing_data_mask])
    df_filtered = df_filtered[~missing_data_mask] 
    filtered_df['missing_data'] = len(df_filtered) 

    print("Cardiac Arrest Analysis:")
    print(f"1. Total Cardiac Arrest Events: {total_cardiac_arrests}")
    print(f"2. Removed without CPR by EMS: {removed['cpr']} (Remaining: {filtered_df['cpr']})")
    print(f"3. Removed with Age < 18: {removed['age']} (Remaining: {filtered_df['age']})")
    print(f"4. Removed with Response Time > 60 min: {removed['response_time']} (Remaining: {filtered_df['response_time']})")
    print(f"5. Removed as NOT 911 (Scene) Responses: {removed['not_911']} (Remaining: {filtered_df['not_911']})")
    print(f"6. Removed WITHOUT Transport or Termination: {removed['transport']} (Remaining: {filtered_df['transport']})")
    print(f"7. Removed with Injury Reported: {removed['injury']} (Remaining: {filtered_df['injury']})")
    print(f"8. Removed due to missing data: {removed['missing_data']} (Remaining: {filtered_df['missing_data']})")
    print(f"9. Final Count: {len(df_filtered)}")
    print('*******************')
    return df_filtered


def calc_urbanicity(df):
    """Calculates the number of patients for each Urbanicity type."""
    print(df['Urbanicity'].value_counts()) 

conn = sqlite3.connect('../db/NEMSIS_PUB.db') 
eArrest_codes_01 = [3001003, 3001005]
eArrest_codes_02 = [3002015] 
eArrest_codes_03 = [3003001, 3003003, 3003005]
eResponse_codes = [2205001, 2205003, 2205009]
eDisposition_codes = [4212019, 4212033] 
final_df = analyze_cardiac_arrest_events(conn, eArrest_codes_01, eArrest_codes_02, eArrest_codes_03, eResponse_codes, eDisposition_codes)
calc_urbanicity(final_df)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) 
file_path = os.path.join(project_root, "src", "db", "filtered_cardiac_events_df.pkl")
final_df.to_pickle(file_path) 

conn.close()
