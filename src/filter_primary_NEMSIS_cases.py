import sqlite3
import time
import pandas as pd
from datetime import datetime
from constants import filter_criteria as filters
from constants import paths
from pathlib import Path



def main():

    conn = sqlite3.connect(paths.db_path)


    query = f"""

    with cte_medications_filtered as (
        select m.PcrKey
        , m.eMedications_01
        , m.eMedications_03
        , m.eMedications_03Descr
        , m.eMedications_05 
        , m.eMedications_06
        , m.eMedications_07
        from FACTPCRMEDICATION m
        where m.eMedications_03 in ({', '.join([str(x) for x in filters.epinephrine_medication_codes])})
    )

    , cte_epinephrine as (
        select e.PcrKey
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

        from cte_medications_filtered e
        group by e.PcrKey
    )

    select 
    pcr.PcrKey
    , pcr.eScene_01
    , resus.eArrest_03
    , pcr.ePatient_13
    , pcr.eResponse_05
    , pcr.eDisposition_12
    , comp_el.Urbanicity
    , cast(comp_el.ageinyear as int) as ageinyear
    , case when ep.TotalDosesEpinephrine is null then 0 else 1 end as EpinephrineAdministered
    , case when ep.TotalDosesEpinephrine is null then 0 else ep.TotalDosesEpinephrine end as TotalDosesEpinephrine
    , cast(comp_el.EMSDispatchCenterTimeSec as float) as EMSDispatchCenterTimeSec
    , cast(comp_el.EMSSystemResponseTimeMin as float) as EMSSystemResponseTimeMin
    , (cast(comp_el.EMSDispatchCenterTimeSec as float) / 60) + cast(comp_el.EMSSystemResponseTimeMin as float) as TotalResponseTime
    
    from Pub_PCRevents pcr

    inner join FACTPCRARRESTRESUSCITATION resus on  resus.PcrKey = pcr.PcrKey 
    inner join ComputedElements comp_el on comp_el.PcrKey = pcr.PcrKey
    left join cte_epinephrine ep on ep.PcrKey = pcr.PcrKey

    where pcr.eArrest_01 in ({', '.join([str(x) for x in filters.eArrest_01_codes])})
    and pcr.eArrest_02 in ({', '.join([str(x) for x in filters.eArrest_02_codes])})
    and pcr.eResponse_05 in ({', '.join([str(x) for x in filters.eResponse_05_codes])})
    and pcr.eDisposition_12 in ({', '.join([str(x) for x in filters.eDisposition_12_codes])})
    and pcr.eScene_01 in ({', '.join([str(x) for x in filters.eScene_01_codes])})
    and resus.eArrest_03 in ({', '.join([str(x) for x in filters.eArrest_03_codes])})
    and cast(comp_el.ageinyear as int) >= {filters.age_lower_limit}
    and cast(comp_el.ageinyear as int) <= {filters.age_upper_limit}
    and cast(comp_el.EMSDispatchCenterTimeSec as float) > 0
    and cast(comp_el.EMSSystemResponseTimeMin as float) > 0
    and ((cast(comp_el.EMSDispatchCenterTimeSec as float) / 60) + cast(comp_el.EMSSystemResponseTimeMin as float)) < {filters.abnormal_response_time_min}
    and comp_el.Urbanicity <> ''

    order by comp_el.ageinyear
    """
    
    print(query)
    query_df = pd.read_sql_query(query, conn)

    print(query_df.shape)
    print(query_df.dtypes)
    print(query_df.head)

    print(query_df['eArrest_03'].unique())
    print(query_df['TotalResponseTime'].min(), query_df['TotalResponseTime'].max())
    print(query_df['eResponse_05'].unique())
    print(query_df['eDisposition_12'].unique())
    print(query_df['eScene_01'].unique())
    
    print(query_df['EpinephrineAdministered'].value_counts())

    save_path = Path(__file__).parent.parent / 'data' / 'processed' / 'selected_events.pickle' 
    query_df.to_pickle(path=save_path) 


if __name__ == "__main__":
    main()
