import pandas as pd
from pandasql import sqldf
from pathlib import Path
import sqlite3

def main():
    # read file from Aaron's project
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events.pickle'
    df = pd.read_pickle(data_fp)


    #print(df.dtypes)
    #df.drop_duplicates()

    print("N_Cols:", len(df.columns.tolist()))
    print("N_Rows:",  df.shape[0])

    """ print("N_Cols:", len(df.columns.tolist()))
    print("N_Rows:",  df.shape[0])
    df['ageinyear'] = df['ageinyear'].replace('. ', None)
    df['ageinyear'] = df['ageinyear'].astype(float)
    num_pediatric_cases = df[df.ageinyear < 18].shape[0]
    num_missing_age = df['ageinyear'].isna().sum()
    df = df[df.ageinyear >= 18] # exclude pediatric cases, and those missing age """


    


    """ print(f"{num_pediatric_cases} pediatric cases removed.")
    print(f"{num_missing_age} cases with missing age removed.")
    print("N_Cols:", len(df.columns.tolist()))
    print("N_Rows:",  df.shape[0])
    print("Merging in eArrest_03")
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'pcr_arrest_resuscitation.pickle'
    resus_df = pd.read_pickle(data_fp)
    print(resus_df.shape) """


    con = sqlite3.connect('data/NEMSIS.db')

    q = """
    select * from resuscitation
    
    select distinct eArrest_03 from resuscitation


    select q.PcrKey
    , count(q.eArrest_03) as NumCodes
    from resuscitation q
    group by q.PcrKey
    order by count(q.eArrest_03) desc
    """

    
    query = """
    with cte as(
    select e.*
    , q.eArrest_03
    from events e
    left join resuscitation q on q.PcrKey = e.PcrKey
    )
    select 
    c.PcrKey
    , count(c.eArrest_03) as NumCodes
    from cte c
    group by c.PcrKey
    order by count(c.eArrest_03) desc
    """
    test_df = pd.read_sql_query(query, con)
    print(test_df.shape)
    output = test_df.head(10)
    print(output.dtypes)
    #for col in output:
    #    print(type(col))
    #display(test_df)












    """  print(resus_df['eArrest_03'].unique())
    df = pd.merge(left = df, right = resus_df, how = 'left', 
                on='PcrKey', suffixes = (None, '_y')) 
    df.drop_duplicates()
    print("N_Cols:", len(df.columns.tolist()))
    print("N_Rows:",  df.shape[0])
    print(df.head) """

    #print(df.duplicated(subset = 'PcrKey').unique())
    #print(resus_df.duplicated(subset = 'PcrKey').unique())

    #print(resus_df.info(memory_usage="deep"))

    q = """
    with cte as (
    select * from resus_df
    )

    select 
    q.PcrKey
    , count(q.eArrest_03)
    from cte q
    group by q.PcrKey
    """
    #res = sqldf(q, locals())
    #print(res.shape)
    #print(res.head)  
    









    #df = df[df.eScene_01 == 9923003] # keep only those units first on scene


    #print("N_Cols:", len(df.columns.tolist()))
    #print("N_Rows:",  df.shape[0])

    """ #print(df['eScene_01'].head())
    print(df['ageinyear'].isna().sum())
    print(df['eScene_01'].isna().sum())
    print(df['eSituation_13'].isna().sum()) """

    """ df.drop_duplicates()
    print("N_Cols:", len(df.columns.tolist()))
    print("N_Rows:",  df.shape[0]) """


    



if __name__ == "__main__":
    main()
