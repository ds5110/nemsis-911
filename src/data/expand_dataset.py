import pandas as pd
from pandasql import sqldf
from pathlib import Path
import sqlite3

def main():
    
    # --------------------------------------- Connect to SQLite Database to Query Data --------------------------------------- #
    
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

    , cte_epinephrine as (
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
    )

    select 
    e.* 
    , r.ResuscitationAttempted
    , r.ResuscitationNotAttempted
    , r.ResuscitationNumNulls
    , cfr.ePatient_14
    , case when ep.TotalDosesEpinephrine is null then 0 else 1 end as EpinephrineAdministered
    , case when ep.TotalDosesEpinephrine is null then 0 else ep.TotalDosesEpinephrine end as TotalDosesEpinephrine

    from events e
    left join cte_resuscitation r on r.PcrKey = e.PcrKey
    left join cte_filtered_race cfr on cfr.PcrKey = e.PcrKey
    left join cte_epinephrine ep on ep.PcrKey = e.PcrKey
    """

    # store query results in pandas dataframe, print dimensions
    df = pd.read_sql_query(query, con)
    print("\nStarting Table Dimensions:")
    print("\tN_Cols:", len(df.columns.tolist()))
    print("\tN_Rows:",  df.shape[0])

    # ----------------------------------- Remove Pediatric Cases and Cases with Missing Age ---------------------------------- #
    
    # convert age to float, remove null '. ' value
    df['ageinyear'] = df['ageinyear'].replace('. ', None)
    df['ageinyear'] = df['ageinyear'].astype(float)

    # calculate number of pediatric & null cases, then filter out of df
    num_pediatric_cases = df[df.ageinyear < 18].shape[0]
    num_missing_age = df['ageinyear'].isna().sum()
    print("\nRemoving Pediatric Cases:")
    df = df[df.ageinyear >= 18]
    print(f"\t{num_pediatric_cases} pediatric cases removed.")
    print(f"\t{num_missing_age} cases with missing age removed.")
    print("\tN_Rows:",  df.shape[0])

    # --------------------------------------- Remove Cases where CPR was not Attempted --------------------------------------- #
    
    print("\nRemoving Cases with no CPR Provided")
    # calculate number with no attempt and not null, and the number of nulls, then remove
    num_no_cpr = df[(df.ResuscitationAttempted == 0) & (df.ResuscitationNumNulls == 0)].shape[0]
    num_null_cpr = df[df.ResuscitationNumNulls > 0].shape[0]
    num_conflicting_cpr = df[(df.ResuscitationAttempted > 0) & (df.ResuscitationNotAttempted > 0)].shape[0]
    print(f"\t{num_no_cpr} cases where resuscitation was not attempted")
    print(f"\t{num_null_cpr} cases with null resuscitation data")
    print(f"\t{num_conflicting_cpr} with conflicting cpr codes (included)")
    df = df[df.ResuscitationAttempted > 0]
    df = df[df.ResuscitationNumNulls < 1]
    print("\tN_Rows:",  df.shape[0])

    # -------------------------------- Removing Cases with Abnormal or Missing Response Time --------------------------------- #

    df['EMSDispatchCenterTimeSec'] = df['EMSDispatchCenterTimeSec'].replace('. ', None)
    df['EMSDispatchCenterTimeSec'] = df['EMSDispatchCenterTimeSec'].astype(float)
    df['EMSSystemResponseTimeMin'] = df['EMSSystemResponseTimeMin'].replace('. ', None)
    df['EMSSystemResponseTimeMin'] = df['EMSSystemResponseTimeMin'].astype(float)

    # drop rows with null times, unable to tell if response time normal or abnormal
    print("\nRemoving Cases with Missing Response Time:")
    print(f"\t{df['EMSDispatchCenterTimeSec'].isna().sum()} rows w/ null time 1")
    print(f"\t{df['EMSSystemResponseTimeMin'].isna().sum()} rows w/ null time 2")
    df.dropna(subset = ['EMSDispatchCenterTimeSec'], inplace = True)
    df.dropna(subset = ['EMSSystemResponseTimeMin'], inplace = True)
    print("\tN_Rows:",  df.shape[0])

    # remove rows with abnormal response time, > 60 minutes
    print("\nRemove Rows with Abnormal Response Time:")
    df['ResponseTime'] = (df['EMSDispatchCenterTimeSec'] / 60) + df['EMSSystemResponseTimeMin']
    num_abnormal_response_time = df[df.ResponseTime > 60].shape[0]
    print(f"\t{num_abnormal_response_time} records removed w/ response time > 60 minutes.")
    df = df[df.ResponseTime <= 60]
    print("\tN_Rows:",  df.shape[0])

    # ----------------------------------- Removing Cases that were not a 911 Scene Response ---------------------------------- #

    print("\nRemoving Records that are not a 911 Scene Response:")
    num_not_911 = df[(df.eResponse_05 != 2205001) & (df.eResponse_05 != 2205003) & (df.eResponse_05 != 2205009)].shape[0]
    print(f"\t{num_not_911} records removed that are not 911 scene responses.")
    df = df[(df.eResponse_05 == 2205001) | (df.eResponse_05 == 2205003) | (df.eResponse_05 == 2205009)]
    print("\tN_Rows:",  df.shape[0])

    # ------------------------------------- Removing Cases for Traumatic or Null Injuries ------------------------------------ #

    print("\nRemoving Records for Traumatic Injury, Null Injury:")
    num_null_injury = df['eArrest_02'].isna().sum()
    print(f"\t{num_null_injury} records with missing injury info.")
    df = df[df.eArrest_02 == 3002001]
    print("\tN_Rows:",  df.shape[0])

    # ------------------------ Removing Cases where Unit did not Transport or Terminate Resuscitation ------------------------ #

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

    # -------------------------------- Removing Records for Units that were not First on Scene ------------------------------- #
    
    print("\nRemoving Records that were not the First Unit on Scene:")
    num_not_first = df[df.eScene_01 == 9923001].shape[0]
    num_null_onScene = df['eScene_01'].isna().sum()
    print(f"\t{num_not_first} records removed that were not first on scene")
    print(f"\t{num_null_onScene} records with null first on scene")
    df = df[df.eScene_01 == 9923003]
    print("\tN_Rows:",  df.shape[0])

    # ------------------------------------------ Checking Records where Race is Null ----------------------------------------- #
   
    # Note: not removing null race records as this is not a criteria mentioned by the paper
    #       if analysis is done on race, these records should be considered. 
    print("\nChecking Records where Race is Null:")
    print(f"\t{df['ePatient_14'].isna().sum()} records with missing race")
    print(df['ePatient_14'].unique())

    # 73664 total
    print(df['EpinephrineAdministered'].value_counts())
    print(df['TotalDosesEpinephrine'].value_counts())

    # -------------------------------------- Saving Final Pickle File with Cleaned Data -------------------------------------- #




if __name__ == "__main__":
    main()
