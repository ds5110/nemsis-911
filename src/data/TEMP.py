import pandas as pd
from pandasql import sqldf
from pathlib import Path
import sqlite3

def main():
    
    #print(df.dtypes)
    #df.drop_duplicates()


    # read file from Aaron's project
    #data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events.pickle'
    #df = pd.read_pickle(data_fp)


    con = sqlite3.connect('data/NEMSIS.db')

    query = """
    with cte_resuscitation as (
        select 
        r.PcrKey
        , sum(case when r.eArrest_03 in ('3003001', '3003003', '3003005') then 1 
            else 0 end) as ResuscitationAttempted
        , sum(case when r.eArrest_03 in ('3003007', '3003009', '3003011') then 1 
            else 0 end) as ResuscitationNotAttempted
        , sum(case when r.eArrest_03 is null then 1 else 0 end) as ResuscitationNumNulls
        from resuscitation r
        group by r.PcrKey
    )

    , cte_race as (
        select
        r.PcrKey
        , count(r.ePatient_14) as NumRecords
        from race r
        group by r.PcrKey
    )

    , cte_race_interim as (
        select q.* from cte_race q
        where q.NumRecords < 2
    )

    , cte_filtered_race as (
        select
        i.PcrKey
        , r.ePatient_14
        from cte_race_interim i
        left join race r on r.PcrKey = i.PcrKey
    )

    select 
    e.* 
    , r.ResuscitationAttempted
    , r.ResuscitationNotAttempted
    , r.ResuscitationNumNulls
    , cfr.ePatient_14

    from events e
    left join cte_resuscitation r on r.PcrKey = e.PcrKey
    left join cte_filtered_race cfr on cfr.PcrKey = e.PcrKey
    """
    df = pd.read_sql_query(query, con)
    print(df.shape)
    #output = test_df.head(10)
    #print(output.dtypes)

    print("\nStarting Table Dimensions:")
    print("\tN_Cols:", len(df.columns.tolist()))
    print("\tN_Rows:",  df.shape[0])



    df['ageinyear'] = df['ageinyear'].replace('. ', None)
    df['ageinyear'] = df['ageinyear'].astype(float)
    
    num_pediatric_cases = df[df.ageinyear < 18].shape[0]
    num_missing_age = df['ageinyear'].isna().sum()

    print("\nRemoving Pediatric Cases:")
    df = df[df.ageinyear >= 18] # exclude pediatric cases, and those missing age 
    print(f"\t{num_pediatric_cases} pediatric cases removed.")
    print(f"\t{num_missing_age} cases with missing age removed.")
    #print("\tN_Cols:", len(df.columns.tolist()))
    print("\tN_Rows:",  df.shape[0])


    print("\nRemoving Cases with no CPR Provided")
    num_no_cpr = df[(df.ResuscitationAttempted == 0) & (df.ResuscitationNumNulls == 0)].shape[0]
    num_null_cpr = df[df.ResuscitationNumNulls > 0].shape[0]
    num_conflicting_cpr = df[(df.ResuscitationAttempted > 0) & (df.ResuscitationNotAttempted > 0)].shape[0]
    print(f"\t{num_no_cpr} cases where resuscitation was not attempted")
    print(f"\t{num_null_cpr} cases with null resuscitation data")
    print(f"\t{num_conflicting_cpr} with conflicting cpr codes (included)")
    #print(df['ResuscitationNumNulls'].unique())
    df = df[df.ResuscitationAttempted > 0]
    df = df[df.ResuscitationNumNulls < 1]
    #print("N_Cols:", len(df.columns.tolist()))
    print("\tN_Rows:",  df.shape[0])


    #print(df['EMSDispatchCenterTimeSec'].unique())
    #print(df['EMSSystemResponseTimeMin'].unique())

    df['EMSDispatchCenterTimeSec'] = df['EMSDispatchCenterTimeSec'].replace('. ', None)
    df['EMSDispatchCenterTimeSec'] = df['EMSDispatchCenterTimeSec'].astype(float)

    df['EMSSystemResponseTimeMin'] = df['EMSSystemResponseTimeMin'].replace('. ', None)
    df['EMSSystemResponseTimeMin'] = df['EMSSystemResponseTimeMin'].astype(float)


    print("\nRemoving Cases with Missing Response Time:")
    print(f"\t{df['EMSDispatchCenterTimeSec'].isna().sum()} rows w/ null time 1")
    print(f"\t{df['EMSSystemResponseTimeMin'].isna().sum()} rows w/ null time 2")

    df.dropna(subset = ['EMSDispatchCenterTimeSec'], inplace = True)
    df.dropna(subset = ['EMSSystemResponseTimeMin'], inplace = True)

    #print("N_Cols:", len(df.columns.tolist()))
    print("\tN_Rows:",  df.shape[0])


    print("\nRemove Rows with Abnormal Response Time:")
    df['ResponseTime'] = (df['EMSDispatchCenterTimeSec'] / 60) + df['EMSSystemResponseTimeMin']
    num_abnormal_response_time = df[df.ResponseTime > 60].shape[0]
    print(f"\t{num_abnormal_response_time} records removed w/ response time > 60 minutes.")
    df = df[df.ResponseTime <= 60]
    #print("N_Cols:", len(df.columns.tolist()))
    print("\tN_Rows:",  df.shape[0])


    print("\nRemoving Records that are not a 911 Scene Response:")


    num_not_911 = df[(df.eResponse_05 != 2205001) & (df.eResponse_05 != 2205003) & (df.eResponse_05 != 2205009)].shape[0]
    print(f"\t{num_not_911} records removed that are not 911 scene responses.")
    df = df[(df.eResponse_05 == 2205001) | (df.eResponse_05 == 2205003) | (df.eResponse_05 == 2205009)]
    print("\tN_Rows:",  df.shape[0])


    print("\nRemoving Records for Traumatic Injury, Null Injury:")
    num_null_injury = df['eArrest_02'].isna().sum()
    print(f"\t{num_null_injury} records with missing injury info.")
    df = df[df.eArrest_02 == 3002001]
    print("\tN_Rows:",  df.shape[0])


    print("\nRemoving Records where Unit did not Transport or Terminate Resuscitation:")
    
    num_no_transport = df[
        (df.eDisposition_12 != 4212001) & (df.eDisposition_12 != 4212003) & 
        (df.eDisposition_12 != 4212005) & (df.eDisposition_12 != 4212017) &
        (df.eDisposition_12 != 4212019) & (df.eDisposition_12 != 4212027) & 
        (df.eDisposition_12 != 4212029) & (df.eDisposition_12 != 4212033) 
    ].shape[0]
    print(f"\t{num_no_transport} records with excluded eDisposition_12 codes")

    df = df[
        (df.eDisposition_12 == 4212001) | (df.eDisposition_12 == 4212003) | 
        (df.eDisposition_12 == 4212005) | (df.eDisposition_12 == 4212017) |
        (df.eDisposition_12 == 4212019) | (df.eDisposition_12 == 4212027) | 
        (df.eDisposition_12 == 4212029) | (df.eDisposition_12 == 4212033) 
    ]

    print("\tN_Rows:",  df.shape[0])


    print("\nRemoving Records that were not the First Unit on Scene:")
    num_not_first = df[df.eScene_01 == 9923001].shape[0]
    num_null_onScene = df['eScene_01'].isna().sum()
    print(f"\t{num_not_first} records removed that were not first on scene")
    print(f"\t{num_null_onScene} records with null first on scene")
    df = df[df.eScene_01 == 9923003]
    print("\tN_Rows:",  df.shape[0])



    print("\nChecking Records where Race is Null:")
    print(f"\t{df['ePatient_14'].isna().sum()} records with missing race")
    print(df['ePatient_14'].unique())


    #print(df['eDisposition_12'].unique())
    #con = sqlite3.connect('data/NEMSIS.db')

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
    """ test_df = pd.read_sql_query(query, con)
    print(test_df.shape)
    output = test_df.head(10)
    print(output.dtypes) """
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
