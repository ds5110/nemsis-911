import sqlite3
import time
import pandas as pd
from datetime import datetime
from constants import filter_criteria as filters
from constants import paths



def main():

    conn = sqlite3.connect(paths.db_path)


    query = f"""
    select pcr.PcrKey, resus.eArrest_03, count(pcr.PcrKey) as NumRecords from Pub_PCRevents pcr
    inner join FACTPCRARRESTRESUSCITATION resus on pcr.PcrKey = resus.PcrKey 
    where pcr.eArrest_01 in ({', '.join([str(x) for x in filters.eArrest_codes_01])})
    and pcr.eArrest_02 in ({', '.join([str(x) for x in filters.eArrest_codes_02])})
    and resus.eArrest_03 in ({', '.join([str(x) for x in filters.eArrest_codes_03])})
    group by pcr.PcrKey, resus.eArrest_03
    order by count(pcr.PcrKey) desc
    """
    
    print(query)
    query_df = pd.read_sql_query(query, conn)

    print(query_df.shape)
    print(query_df.dtypes)
    print(query_df.head)
if __name__ == "__main__":
    main()
