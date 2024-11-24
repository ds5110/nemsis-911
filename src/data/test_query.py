import sqlite3
import time
from datetime import datetime

def get_nulls(conn):
    cursor = conn.cursor()
    query = f""" SELECT COUNT(*) 
    FROM ComputedElements
    WHERE Urbanicity IS NULL; """
    start_time = time.time()
    cursor.execute(query)  # Combine values and eArrest_codes_03
    count = cursor.fetchone()[0]
    end_time = time.time()
    execution_time = end_time - start_time
    return count, execution_time

# Connect to the database
conn = sqlite3.connect('../db/NEMSIS_PUB.db') 
# Get the null count and execution time
null_count, execution_time  = get_nulls(conn)

# Print the results
print(f"Number of NULL values in Urbanicity: {null_count}")
print(f"Query execution time: {execution_time:.2f} seconds")
conn.close() 

