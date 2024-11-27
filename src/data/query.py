import pandas as pd
from pandasql import sqldf
from pathlib import Path
import sqlite3


def main():

    # parameters
    n_rows_save = 20
    file_name = "Medications_Epinephrine_CTE_Test"

    # read file from Aaron's project
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events.pickle'
    df = pd.read_pickle(data_fp)

    con = sqlite3.connect('data/NEMSIS.db')
    
    query = """
    select 
    e.PcrKey
    , count(e.eMedications_03) as TotalDosesEpinephrine  
    , sum(case when e.eMedications_06 = 3706001 then 1 else 0 end) as nGramsCases
    , sum(case when e.eMedications_06 = 3706001 then e.eMedications_05 else 0 end) as gramsDosageTotal
    , sum(case when e.eMedications_06 = 3706003 then 1 else 0 end) as nInchesCases
    , sum(case when e.eMedications_06 = 3706003 then e.eMedications_05 else 0 end) as inchesDosageTotal
    , sum(case when e.eMedications_06 = 3706005 then 1 else 0 end) as nIntUnitCases
    , sum(case when e.eMedications_06 = 3706005 then e.eMedications_05 else 0 end) as iuDosageTotal
    , sum(case when e.eMedications_06 = 3706007 then 1 else 0 end) as nKvoCases
    , sum(case when e.eMedications_06 = 3706007 then e.eMedications_05 else 0 end) as kvoDosageTotal
    , sum(case when e.eMedications_06 = 3706013 then 1 else 0 end) as nMdiCases
    , sum(case when e.eMedications_06 = 3706013 then e.eMedications_05 else 0 end) as mdiDosageTotal
    , sum(case when e.eMedications_06 = 3706009 then 1 else 0 end) as nLitersCases
    , sum(case when e.eMedications_06 = 3706009 then e.eMedications_05 else 0 end) as litersDosageTotal
    , sum(case when e.eMedications_06 = 3706011 then 1 else 0 end) as nLitPerMinCases
    , sum(case when e.eMedications_06 = 3706011 then e.eMedications_05 else 0 end) as litPerMinDosageTotal
    , sum(case when e.eMedications_06 = 3706015 then 1 else 0 end) as nMcgCases
    , sum(case when e.eMedications_06 = 3706015 then e.eMedications_05 else 0 end) as mcgDosageTotal
    , sum(case when e.eMedications_06 = 3706017 then 1 else 0 end) as nMcgPerKgMinCases
    , sum(case when e.eMedications_06 = 3706017 then e.eMedications_05 else 0 end) as mcgPerKgMinDosageTotal
    , sum(case when e.eMedications_06 = 3706021 then 1 else 0 end) as nMgCases
    , sum(case when e.eMedications_06 = 3706021 then e.eMedications_05 else 0 end) as mgDosageTotal
    , sum(case when e.eMedications_06 = 3706025 then 1 else 0 end) as nMlCases
    , sum(case when e.eMedications_06 = 3706025 then e.eMedications_05 else 0 end) as mlDosageTotal
    , sum(case when e.eMedications_06 = 3706037 then 1 else 0 end) as nMcgMinCases
    , sum(case when e.eMedications_06 = 3706037 then e.eMedications_05 else 0 end) as mcgminDosageTotal
    , sum(case when e.eMedications_06 = 3706033 then 1 else 0 end) as nDropsCases
    , sum(case when e.eMedications_06 = 3706033 then e.eMedications_05 else 0 end) as dropsDosageTotal
    , sum(case when e.eMedications_06 = 3706039 then 1 else 0 end) as nMgPerKgCases
    , sum(case when e.eMedications_06 = 3706039 then e.eMedications_05 else 0 end) as mgPerKgDosageTotal
    , sum(case when e.eMedications_06 = 3706047 then 1 else 0 end) as nMcgPerKgCases
    , sum(case when e.eMedications_06 = 3706047 then e.eMedications_05 else 0 end) as mcgPerKgDosageTotal
    , sum(case when e.eMedications_06 = 3706019 then 1 else 0 end) as nMeqCases
    , sum(case when e.eMedications_06 = 3706019 then e.eMedications_05 else 0 end) as meqDosageTotal
    , sum(case when e.eMedications_06 = 3706029 then 1 else 0 end) as nOtherCases
    , sum(case when e.eMedications_06 = 3706029 then e.eMedications_05 else 0 end) as OtherDosageTotal
    , sum(case when e.eMedications_06 = 3706031 then 1 else 0 end) as nCmCases
    , sum(case when e.eMedications_06 = 3706031 then e.eMedications_05 else 0 end) as cmDosageTotal
    , sum(case when e.eMedications_06 = 3706041 then 1 else 0 end) as nMgMinCases
    , sum(case when e.eMedications_06 = 3706041 then e.eMedications_05 else 0 end) as mgMinDosageTotal
    , sum(case when e.eMedications_06 = 3706023 then 1 else 0 end) as nMgPerKgMinCases
    , sum(case when e.eMedications_06 = 3706023 then e.eMedications_05 else 0 end) as mgPerKgMinDosageTotal

    from epinephrine e 

    group by e.PcrKey
    """
    query_df = pd.read_sql_query(query, con)

    print(query_df.dtypes)

    
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
