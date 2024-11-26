import pandas as pd
from pandasql import sqldf
from pathlib import Path
import sqlite3


def main():

    # parameters
    n_rows_save = 20
    file_name = "Multiple_eArrest_03_Groupings_Values"

    # read file from Aaron's project
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events.pickle'
    df = pd.read_pickle(data_fp)

    con = sqlite3.connect('data/NEMSIS.db')

    query = """
    select e.PcrKey
    , q.eArrest_03
    from events e
    left join resuscitation q on q.PcrKey = e.PcrKey
    where e.PcrKey in ('169828180', '170223060', '170767469', '170928978', '171106211')
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
