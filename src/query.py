import pandas as pd
from pathlib import Path
import sqlite3
import time
from constants import paths

def main():

    # parameters
    n_rows_save = 30
    file_name = "Distinct_eArrest_03"

    # query database, store result in pandas df
    start_time = time.time()
    print("Querying NEMSIS_PUB.db...")

    conn = sqlite3.connect(paths.db_path) 
    query = """
    select distinct eArrest_03
    from FACTPCRARRESTRESUSCITATION
    """
    query_df = pd.read_sql_query(query, conn)
    
    # open text file to store results
    out_file = open(f"./reports/query_results/{file_name}.txt", 'w')
    print(f"Writing to file: ./reports/query_results/{file_name}.txt...")

    # get column names for printing prior to df rows
    query_col_names = query_df.columns.tolist()

    # write the query that was run
    out_file.write(f"Query:\n'''{query}\n'''\n\n")

    # write each column header
    for col in query_col_names:
        out_file.write(f"|  {col}  ")
    out_file.write("|\n")

    # if our result has less rows than parameter, update parameter
    if(query_df.shape[0] < n_rows_save):
        n_rows_save = query_df.shape[0]

    # write each row to text file
    for i in range(n_rows_save):
        for col in query_col_names:
            out_file.write(f"|  {query_df[col][i]}  ")
        out_file.write("|\n")

    # close then print resulting time    
    out_file.close()
    end_time = time.time()
    print(f"Completed in {round(end_time - start_time, 2)} seconds")

if __name__ == "__main__":
    main()
