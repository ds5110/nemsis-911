import pandas as pd
import sqlite3
import time
from datetime import datetime

conn = sqlite3.connect('../db/NEMSIS_PUB.db') 
eArrest_codes_01 = [3001003, 3001005]
eArrest_codes_02 = [3002015] 
eArrest_codes_03 = [3003001, 3003003, 3003005]
eResponse_codes = [2205001, 2205003, 2205009]
eDisposition_codes = [4212019, 4212033] 

# Create a sample DataFrame similar to your df_filtered
data = {'eDisposition_12': [1, 2, 3, 4212019, 5]} 
df_test = pd.DataFrame(data)
# The problematic line
result = df_test[df_test['eDisposition_12'].isin(eDisposition_codes)]

removed['transport'] = len(df_filtered) - len(df_filtered[df_filtered['eDisposition_12'].isin(eDisposition_codes)])
print(result)

conn.close()