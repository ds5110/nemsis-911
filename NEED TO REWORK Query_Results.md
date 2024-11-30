# Query Results

Tristan Jordan - 11/26/24

## Background

The python file `src/data/query.py` can be used to query the NEMSIS database, and it will save text files with the query results, for iterative investigation into the data available in NEMSIS. For the script:
* `n_rows_save` can be changed to specify how many rows to save, defaults to 20.
* `file_name` must be changed to specify the name of the .txt file saved to `reports/query_results`
* `query` here is where you type your query to the NEMSIS.db file, an sqlite database.

## NEMSIS.db table names
The `data/NEMSIS.db` file is created by the `src/data/db_setup.py` script. This database includes the following tables: 
* `events` includes all of the cardiac events identified in Aaron Fihn's `events.pickle` file
* `resuscitation` - equivalent to the table in text file FACTPCRARRESTRESUSCITATION

## Question 1 - why does eArrest_03 create duplicate rows? 

For `eArrest.03 - Resuscitation Attempted By EMS`, we can see that some Pcrs have multiple codes listed per key: 

```
Query:
'''
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
    
'''

|  PcrKey  |  NumCodes  |
|  236146666  |  3  |
|  236113284  |  3  |
|  236113187  |  3  |
|  236085543  |  3  |
|  236082857  |  3  |
|  236047812  |  3  |
```

The relevant codes are: 
* `3003001` - Attempted Defibrillation
* `3003003` - Attempted Ventilation
* `3003005` - Initiated Chest Compressions
* `3003007` - Not Attempted-Considered Futile
* `3003009` - Not Attempted-DNR Orders
* `3003011` - Not Attempted-Signs of Circulation

It makes sense that multiple attempted codes (1, 3, or 5) may appear together, but we can double check if not-attempted codes overlap with attempted codes: 

```
Query:
'''
    with cte as(
        select e.*
        , q.eArrest_03
        from events e
        left join resuscitation q on q.PcrKey = e.PcrKey
    )
    
    , aggregated as (
        select 
        c.PcrKey
        , count(c.eArrest_03) as NumCodes
        , sum(case when c.eArrest_03 in ('3003007', '3003009', '3003011') then 1 
            else 0 end) as NumNotAttemptedCodes
        , sum(case when c.eArrest_03 in ('3003001', '3003003', '3003005') then 1 
            else 0 end) as NumAttemptedCodes
        from cte c
        group by c.PcrKey
    )

    select * from aggregated
    where NumNotAttemptedCodes <> 0
    and NumAttemptedCodes <> 0
    
'''

|  PcrKey  |  NumCodes  |  NumNotAttemptedCodes  |  NumAttemptedCodes  |
|  169828180  |  2  |  1  |  1  |
|  170223060  |  2  |  1  |  1  |
|  170767469  |  2  |  1  |  1  |
|  170928978  |  2  |  1  |  1  |
|  171106211  |  3  |  1  |  2  |
```

Then, looking at a few of these cases:

```
Query:
'''
    select e.PcrKey
    , q.eArrest_03
    from events e
    left join resuscitation q on q.PcrKey = e.PcrKey
    where e.PcrKey in ('169828180', '170223060', '170767469', '170928978', '171106211')
    
'''

|  PcrKey  |  eArrest_03  |
|  169828180  |  3003005  |
|  169828180  |  3003007  |
|  170223060  |  3003005  |
|  170223060  |  3003007  |
|  170767469  |  3003005  |
|  170767469  |  3003009  |
|  170928978  |  3003005  |
|  170928978  |  3003009  |
```

We can see that occasionally the code `3003005 - Initiated Chest Compressions` occurs with other not attempted codes. Just in case, we will include any Pcrs where chest compressions were initiated. This should be verified, however, and is one area where the definitions of what to include or exclude for a feature are vague. 

**Note:** after querying, there were only 410 cases which had an attempted and not/attempted code together, so including these either way does not greatly impact the final number of rows.

## Response Time > 60 minutes

For response time we want to know how long it took from the 911 call to unit arrival on scene. Referring to the manual, we can calculate this by taking `EMSDispatchCenterTimeSec / 60` + `EMSSystemResponseTimeMin`


## Unit Did Not Transport or Terminate Resuscitation

The paper authors note that *"...Finally, we only included incidents in which one EMS unit provided treatment until the end of the event, either until the patient was transported to a receiving facility or if resuscitative efforts were attempted but terminated by the responding unit prior to transport."* 

A few filtering criteria are mentioned:
* one EMS unit provided treatment (no transfers)
* records where the patient die may still be included, as long as one unit provided treatment

Reviewing the data dictionary for `eDisposition_12` codes, there are multiple codes which look like they should be removed by the above criteria: 
* "4212007"  Canceled (Prior to Arrival At Scene) - *no treatment occurred*
* "4212009"  Canceled on Scene (No Patient Contact) - *no treatment occurred*
* "4212011"  Canceled on Scene (No Patient Found) - *no treatment occurred*
* "4212013"  Patient Dead at Scene-No Resuscitation Attempted (With Transport) - *although transport occurred, no resuscitation was attempted*
* "4212015"  Patient Dead at Scene-No Resuscitation Attempted (Without Transport) - *no resuscitation attempted*
* "4212021"  Patient Evaluated, No Treatment/Transport Required - *resuscitation would not be attempted if not treatment required*
* "4212023"  Patient Refused Evaluation/Care (With Transport) - *no resuscitation if patient refuses*
* "4212025"  Patient Refused Evaluation/Care (Without Transport) - *no resuscitation if patient refuses*
* "4212031"  Patient Treated, Transferred Care to Another EMS Unit - *if transferred to another unit, fails the criteria that only one unit provide care*
* "4212035"  Patient Treated, Transported by Law Enforcement - *assuming law enforcement means multiple units*
* "4212037"  Patient Treated, Transported by Private Vehicle - *assuming private vehicle means multiple units*
* "4212039"  Standby-No Services or Support Provided - *no treatment*
* "4212041"  Standby-Public Safety, Fire, or EMS Operational Support Provided - *services outside of resuscitation*
* "4212043"  Transport Non-Patient, Organs, etc. - *unclear, but does not mention treatment of any kind*

To check the impact on records of potentially removing these codes, we can count PcrKeys by code:

```
Query:
'''
    select 
    e.eDisposition_12
    , count(e.PcrKey) as NumRecords
    from events e
    group by e.eDisposition_12
    order by count(e.PcrKey) desc
    
'''

|  eDisposition_12  |  NumRecords  |
|  4212033  |  116877  |
|  4212019  |  82561  |
|  4212015  |  59167  |
|  4212031  |  18342  |
|  4212005  |  3382  |
|  4212001  |  3308  |
|  4212017  |  2274  |
|  4212029  |  1544  |
|  4212013  |  842  |
|  4212021  |  685  |
|  4212025  |  553  |
|  4212003  |  256  |
|  4212027  |  208  |
|  4212035  |  186  |
|  4212041  |  111  |
|  4212009  |  104  |
|  4212037  |  54  |
|  4212007  |  51  |
|  4212039  |  29  |
|  4212011  |  17  |
```

* "4212007"  Canceled (Prior to Arrival At Scene) - 51
* "4212009"  Canceled on Scene (No Patient Contact) - 104
* "4212011"  Canceled on Scene (No Patient Found) - 17
* "4212013"  Patient Dead at Scene-No Resuscitation Attempted (With Transport) - 842
* "4212015"  Patient Dead at Scene-No Resuscitation Attempted (Without Transport) - 59167
* "4212021"  Patient Evaluated, No Treatment/Transport Required - 685
* "4212023"  Patient Refused Evaluation/Care (With Transport) - *not present in dataset*
* "4212025"  Patient Refused Evaluation/Care (Without Transport) - 553
* "4212031"  Patient Treated, Transferred Care to Another EMS Unit - 18342
* "4212035"  Patient Treated, Transported by Law Enforcement - 186
* "4212037"  Patient Treated, Transported by Private Vehicle - 54
* "4212039"  Standby-No Services or Support Provided - 29
* "4212041"  Standby-Public Safety, Fire, or EMS Operational Support Provided - 111
* "4212043"  Transport Non-Patient, Organs, etc. - *not present in dataset*

Removing these codes would result in a total of **80,141** rows being excluded. The largest impacts on this number are for codes `4212015 - Patient Dead at Scene-No Resuscitation Attempted`, and `4212031 - Patient Treated, Transferred Care to Another EMS Unit`. Both of these seem relatively straightforward to exclude, because each respectively fails a test of the paper authors: 4212015 is a code where no resuscitation was attempted, and 4212031 implies multiple units treating. We should keep this in mind in case results vary wildly from the paper's results - future researches should double check which codes should be included or excluded. 

**Note:** after running the code, only 17,670 records had to be excluded given the above filter choices. There was some overlap where the majority of records noted in the above count were already filtered for different reasons. 