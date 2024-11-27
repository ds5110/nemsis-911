import pandas as pd
from pandasql import sqldf
from pathlib import Path
import sqlite3


def main():

    # parameters
    n_rows_save = 60
    file_name = "Race_Final_Query"

    # read file from Aaron's project
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events.pickle'
    df = pd.read_pickle(data_fp)

    con = sqlite3.connect('data/NEMSIS.db')

    query = """
    with cte as (
        select
        r.PcrKey
        , count(r.ePatient_14) as NumRecords
        from race r
        group by r.PcrKey
    )

    , interim as (
        select c.* from cte c
        where c.NumRecords < 2
    )
    
    select
    i.PcrKey
    , r.ePatient_14
    from interim i
    left join race r on r.PcrKey = i.PcrKey
    """
    query_df = pd.read_sql_query(query, con)

    query_col_names = query_df.columns.tolist()

    out_file = open(f"./reports/query_results/{file_name}.txt", 'w')

    out_file.write(f"Query:\n'''{query}\n'''\n\n")

    for col in query_col_names:
        out_file.write(f"|  {col}  ")
    out_file.write("|\n")

    if(query_df.shape[0] < n_rows_save):
        n_rows_save = query_df.shape[0]

    for i in range(n_rows_save):
        for col in query_col_names:
            out_file.write(f"|  {query_df[col][i]}  ")
        out_file.write("|\n")
    
    out_file.close()


if __name__ == "__main__":
    main()
