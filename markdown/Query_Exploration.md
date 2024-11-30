# Script for Querying NEMSIS_PUB Database
Tristan Jordan - 11/26/24

## Background

The python file `src/data/query.py` can be used to query the NEMSIS_PUB.db database, and it will save text files with the query results, for iterative investigation into the data available in NEMSIS. For the script:
* `n_rows_save` can be changed to specify how many rows to save, defaults to 30.
* `file_name` must be changed to specify the name of the .txt file saved to `reports/query_results`
* `query` here is where you write your query to the NEMSIS_PUB.db file, an sqlite database.

Once all parameters are entered, **make query** can be used in the console to run the script.

## NEMSIS_PUB.db table names
The `data/NEMSIS_PUB.db` file is created by the scripts `create_NEMSIS_db.py` and `load_data_NEMSIS_db.py`. To view what tables are available by default, see:
* `constants/table_definitions.py`
* `constants/file_column_mapping.py`

If you want to add more tables to the database that aren't available by default, you may add the appropriate values into the above constant files, and then run **make rebuild_database** to remove the db object, and rebuild the database (*this option exists so that instead of running make clean and re-running make, you can avoid unpacking the interim/txt files again if they are already present.*)

# Example Questions Investigated with Query

## Question 1 - do any PcrKeys from FACTPCRARRESTRESUSCITATION have multiple eArrest_03 values?

Running the following query shows us that there is only one `eArrest_03` value per PcrKey
```
Query:
'''
    select PcrKey, count(eArrest_03) as NumRecords
    from FACTPCRARRESTRESUSCITATION
    group by PcrKey order by count(eArrest_03) desc
    
'''
|  PcrKey  |  NumRecords  |
|  100167527  |  1  |
|  105483868  |  1  |
|  107118510  |  1  |
|  108876112  |  1  |
|  109453969  |  1  |
```

## Question 2 - what medication descriptions contain the word 'epinephrine'?

The stakeholder identified treatment patterns of epinephrine administration as a key area of interest. To correctly identify epinephrine usage, we need to learn which `eMedication_03` codes should be included:

```
Query:
'''
    select distinct m.eMedications_03, m.eMedications_03Descr from FACTPCRMEDICATION m 
    where m.eMedications_03Descr like '%epinephrine%'
    order by m.eMedications_03
'''

|  eMedications_03  |  eMedications_03Descr  |
|  1010751  |  Epinephrine 0.01 MG/ML / Lidocaine Hydrochloride 10 MG/ML Injectable Solution  |
|  1010759  |  EPINEPHrine 0.01 MG/ML / Lidocaine Hydrochloride 20 MG/ML Injectable Solution  |
|  1010767  |  Epinephrine / Lidocaine Injectable Solution [Xylocaine with Epinephrine]  |
|  1011648  |  Articadent 4 % with Epinephrine 1:100,000 Injectable Solution  |
|  1011809  |  Lignospan 2/1:100000 (lidocaine hydrochloride / epinephrine (as epinephrine bitartrate) ) Injectable  |
|  1012792  |  Epinephrine 0.01 MG/ML / Mepivacaine Hydrochloride 20 MG/ML Injectable Solution  |
|  107602  |  Epinephrine / Lidocaine  |
|  107606  |  Bupivacaine / Epinephrine  |
|  1100194  |  10 ML EPINEPHrine 0.016 MG/ML Prefilled Syringe  |
|  1100200  |  50 ML Norepinephrine 0.016 MG/ML Prefilled Syringe  |
|  1150120  |  1 ML Epinephrine 0.01 MG/ML / Lidocaine Hydrochloride 10 MG/ML Prefilled Syringe  |
|  1150987  |  epinephrine 32 MCG/ML Injectable Solution  |
|  1163887  |  Epinephrine Injectable Product  |
|  1233582  |  Bupivacaine / Epinephrine / Fentanyl  |
|  1233778  |  10 ML EPINEPHrine 0.01 MG/ML Prefilled Syringe  |
|  1245692  |  Epinephrine 0.0016 MG/ML  |
|  1293190  |  EPINEPHrine 0.004 MG/ML  |
|  1293191  |  epinephrine 4 MCG/ML Injectable Solution  |
|  1293648  |  1.7 ML Epinephrine 0.01 MG/ML / Lidocaine Hydrochloride 20 MG/ML Prefilled Syringe  |
|  1305268  |  0.15 ML Epinephrine 1 MG/ML Prefilled Syringe [Auvi-Q]  |
|  1375913  |  Epinephrine 0.01 MG/ML Injectable Solution  |
|  1375969  |  Epinephrine / Lidocaine / Tetracaine  |
|  209217  |  Norepinephrine 1 MG/ML Injectable Solution [Levophed]  |
|  214545  |  Epinephrine / Etidocaine  |
|  214547  |  EPINEPHrine / Prilocaine  |
|  242969  |  Norepinephrine 1 MG/ML Injectable Solution  |
|  284622  |  Articaine / Epinephrine  |
|  310116  |  Epinephrine 0.1 MG/ML Injectable Solution  |
|  310132  |  EPINEPHrine 1 MG/ML Injectable Solution  |
|  310133  |  Racepinephrine 22.5 MG/ML Inhalant Solution  |
```

We can see that there are some medications such as *Norepinephrine* or *Racepinephrine* which contain the search word, but should not be included. Out of caution, combined medications such as *Bupivacaine / Epinephrine* were excluded, in case they serve a different purpose from pure epinephrine. Ideally a stakeholder and/or someone with medical knowledge should confirm which medication codes are relevant to treatment of cardiac events. 

## Question 3 - What dosage units are reported with the selected epinephrine medications?

To better analyze treatment patterns, the number of doses given, and total dosage across treatment / PCR should be reviewed. However, this poses a problem because medications are reported with a wide variety of dosage units. After filtering down the codes to relevant epinephrine codes from Question 3, we can see there are many different dosage units that appear in the data. This would be an interesting area for future study, clarifying which medications should be used, verifying the dosage units reported, and if possible, coming up with a way to standardize dosage for comparison across all PCRs. 

```
Query:
'''
    select distinct m.eMedications_06 from FACTPCRMEDICATION m 
    where m.eMedications_03 in (3992, 310116, 310132, 
    317361, 328314, 328316, 330545, 372030, 377281,
    727316, 727373, 727374, 727386, 1100194, 1233778, 1305268)
    order by m.eMedications_06
    
'''

|  eMedications_06  |
|  3706001  | -- Grams (gms)
|  3706003  | -- Inches (in) 
|  3706005  | -- International Units (IU)
|  3706007  | -- Keep Vein Open (kvo)
|  3706009  | -- Liters (l)
|  3706011  | -- may be deprecated, liters / minute (l/min fluid)
|  3706013  | -- Metered Dose (MDI)
|  3706015  | -- Micrograms (mcg)
|  3706017  | -- Micrograms per Kilogram per Minute (mcg/kg/min)
|  3706019  | -- Milliequivalents (mEq)
|  3706021  | -- Milligrams (mg)
|  3706023  | -- Milligrams per Kilogram Per Minute (mg/kg/min)
|  3706025  | -- Milliliters (ml)
|  3706027  | -- Milliliters per Hour (ml/hr)
|  3706029  | -- Other
|  3706031  | -- Centimeters (cm)
|  3706033  | -- Drops (gtts)
|  3706035  | -- Liters Per Minute (LPM [gas])
|  3706037  | -- Micrograms per Minute (mcg/min)
|  3706039  | -- Milligrams per Kilogram (mg/kg)
|  3706041  | -- Milligrams per Minute (mg/min)
|  3706045  | -- Units per Hour (units/hr)
|  3706047  | -- Micrograms per Kilogram (mcg/kg)
|  3706049  | -- Units
|  3706051  | -- Units per Kilogram per Hour (units/kg/hr)
|  3706053  | -- Units per Kilogram (units/kg)
|  7701001  | -- Not Applicable
|  7701003  | -- Not Recorded
```

## Question 4 - Counts of eDisposition_12 - Unit Did Not Transport or Terminate Resuscitation?

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
    eDisposition_12
    , count(PcrKey) as NumRecords
    from Pub_PCRevents
    group by eDisposition_12
    order by count(PcrKey) desc
    
'''

|  eDisposition_12  |  NumRecords  |
|  4212033  |  34369554  |
|  4212007  |  2903388  |
|  4212031  |  2624918  |
|  4212025  |  2537741  |
|  4212027  |  2139435  |
|  4212009  |  1952058  |
|  4212011  |  1405484  |
|  4212021  |  1161616  |
|  4212029  |  982886  |
|  4212005  |  823999  |
|  4212003  |  559061  |
|  4212001  |  449661  |
|  4212041  |  388619  |
|  4212015  |  323265  |
|  4212039  |  225978  |
|  4212019  |  140326  |
|  4212037  |  65404  |
|  4212035  |  52357  |
|  4212023  |  41597  |
|  4212043  |  18015  |
|  4212013  |  9779  |
|  4212017  |  4351  |
```
Not all of these codes would be on PCRs for cardiac events, but it is good to know that counts can be checked for evaluating the codes to be included / excluded.
