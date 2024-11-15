import sqlite3
import time
from datetime import datetime

def get_cardiac_arrest_yes_events(conn, values):
    cursor = conn.cursor()
    query = """ SELECT COUNT(*) 
                FROM Pub_PCRevents 
                WHERE eArrest_01 IN (?, ?)"""
    start_time = time.time()
    cursor.execute(query, values) 
    count = cursor.fetchone()[0] 
    end_time = time.time()    
    execution_time = end_time - start_time
    print(f"Number of matching rows for Cardiac Arrest-Yes: {count}")
    print(f"Query execution time: {execution_time:.1f} seconds")


def get_count_by_eArrest_and_age(conn, values, age_limit=[18]):
    cursor = conn.cursor()
    query = """ SELECT COUNT(*)
                FROM Pub_PCRevents AS p
                JOIN ComputedElements AS c ON p.PcrKey = c.PcrKey
                WHERE p.eArrest_01 IN (?, ?) AND c.ageinyear < ?"""
    start_time = time.time()
    cursor.execute(query, values + age_limit) 
    count = cursor.fetchone()[0]
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Number of matching rows for Cardiac Arrest-Yes & < 18 years old: {count}")
    print(f"Query execution time: {execution_time:.1f} seconds")


def get_count_by_eArrest_codes(conn, eArrest_codes_01, eArrest_codes_02):
    cursor = conn.cursor()
    placeholders_01 = ', '.join(['?'] * len(eArrest_codes_01))
    placeholders_02 = ', '.join(['?'] * len(eArrest_codes_02))
    query = f"""  SELECT COUNT(*)
                  FROM PUB_PCREVENTS
                  WHERE eArrest_01 IN ({placeholders_01}) AND eArrest_02 IN ({placeholders_02})"""
    start_time = time.time()
    cursor.execute(query, eArrest_codes_01 + eArrest_codes_02)  # Combine the tuples
    count = cursor.fetchone()[0]
    end_time = time.time()
    execution_time = end_time - start_time
    print("Number of matching records for Cardiac Arrest-Yes & Patient Experienced Trauma-Yes:", count)
    print(f"Query execution time: {execution_time:.1f} seconds")
    return count

def get_count_cardiac_arrest_dispositions(conn, eArrest_codes, eDisposition_codes):
    cursor = conn.cursor()
    eArrest_placeholders = ', '.join(['?'] * len(eArrest_codes))
    eDisposition_placeholders = ', '.join(['?'] * len(eDisposition_codes))
    query = f""" SELECT COUNT(*)
                 FROM PUB_PCREVENTS
                 WHERE eArrest_01 IN ({eArrest_placeholders})
                 AND eDisposition_12 IN ({eDisposition_placeholders})"""
    start_time = time.time()
    cursor.execute(query, eArrest_codes + eDisposition_codes)
    count = cursor.fetchone()[0]
    end_time = time.time()
    execution_time = end_time - start_time
    print("Number of patients where the responding vehicle was not a 911 (scene) respone:", count)
    print(f"Query execution time: {execution_time:.1f} seconds")
    return count

def get_count_cardiac_arrest_dispositions(conn, eArrest_codes, eDisposition_codes):
    cursor = conn.cursor()
    eArrest_placeholders = ', '.join(['?'] * len(eArrest_codes))
    eDisposition_placeholders = ', '.join(['?'] * len(eDisposition_codes))
    query = f""" SELECT COUNT(*)
                 FROM PUB_PCREVENTS
                 WHERE eArrest_01 IN ({eArrest_placeholders})
                 AND eDisposition_12 IN ({eDisposition_placeholders})"""
    start_time = time.time()
    cursor.execute(query, eArrest_codes + eDisposition_codes)
    count = cursor.fetchone()[0]
    end_time = time.time()
    execution_time = end_time - start_time
    print("Number of patients where the responding vehicle was not a 911 (scene) respone:", count)
    print(f"Query execution time: {execution_time:.1f} seconds")
    return count    


def get_count_cardiac_arrest_multiple_vehicles(conn, eArrest_codes_01, eDisposition_codes):
    cursor = conn.cursor()
    eArrest_placeholders = ', '.join(['?'] * len(eArrest_codes))
    eDisposition_placeholders = ', '.join(['?'] * len(eDisposition_codes))
    query = f""" SELECT COUNT(*)
                 FROM PUB_PCREVENTS
                 WHERE eArrest_01 IN ({eArrest_placeholders})
                 AND eDisposition_12 IN ({eDisposition_placeholders})"""
    start_time = time.time()
    cursor.execute(query, eArrest_codes + eDisposition_codes)
    count = cursor.fetchone()[0]
    end_time = time.time()
    execution_time = end_time - start_time
    print("Number of patients where the responding unit did not transport or terminate resuscitation:", count)
    print(f"Query execution time: {execution_time:.1f} seconds")
    return count  


def get_heart_attack_events_excluding_long_ems_response(conn, eArrest_codes, time_threshold=60):
    cursor = conn.cursor()
    eArrest_placeholders = ', '.join(['?'] * len(eArrest_codes))
    total_count_query = f"""SELECT COUNT(DISTINCT T1.PcrKey)
                            FROM PUB_PCREVENTS AS T1
                            WHERE T1.eArrest_01 IN ({eArrest_placeholders})"""
    cursor.execute(total_count_query, eArrest_codes)
    total_count = cursor.fetchone()[0]
    included_count_query = f""" SELECT COUNT(DISTINCT T1.PcrKey)  
                                FROM PUB_PCREVENTS AS T1
                                INNER JOIN ComputedElements AS T2 ON T1.PcrKey = T2.PcrKey 
                                WHERE 
                                    T1.eArrest_01 IN ({eArrest_placeholders})
                                    AND (
                                        T2.EMSSystemResponseTimeMin IS NULL 
                                        OR T2.EMSSystemResponseTimeMin <= ? 
                                    )"""
    start_time = time.time()                        
    cursor.execute(included_count_query, eArrest_codes + [time_threshold]) 
    included_count = cursor.fetchone()[0]
    excluded_count = total_count - included_count
    end_time = time.time()
    print(f"Total number of heart attack events: {total_count}")
    print(f"Number of heart attack events (excluding EMS response > {time_threshold} minutes): {included_count}")
    print(f"Number of events excluded: {excluded_count}")
    print(f"Query execution time: {end_time - start_time:.1f} seconds")
    return included_count

eDisposition_codes_2 = [4212009, 4212011, 4212015, 4212019, 4212021, 4212025, 4212027, 4212029, 4212031]
eDisposition_codes = [4212007, 4212039, 4212041, 4212001, 4212003, 4212005] 
eArrest_codes_01 = [3001003, 3001005]
eArrest_codes_02 = [3002015]  
conn = sqlite3.connect('../db/NEMSIS_PUB.db') 
get_cardiac_arrest_yes_events(conn, eArrest_codes_01)
get_count_by_eArrest_and_age(conn, eArrest_codes_01)
get_count_by_eArrest_codes(conn, eArrest_codes_01, eArrest_codes_02)
get_count_cardiac_arrest_dispositions(conn, eArrest_codes_01, eDisposition_codes)
get_count_cardiac_arrest_multiple_vehicles(conn, eArrest_codes_01, eDisposition_codes_2)
get_heart_attack_events_excluding_long_ems_response(conn, eArrest_codes_01)
conn.close()
