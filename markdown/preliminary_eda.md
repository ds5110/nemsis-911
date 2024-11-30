
# Preliminary EDA

We will review the filtered prepared dataset *selected_events* in order to learn the following:
- What columns were included?
- How many null values are there in each column?
- What is the datatype of each column? 
- What are some descriptive statistics about each column?

This info. will be paired with the [NEMSIS Data Dictionary](https://nemsis.org/media/nemsis_v3/release-3.5.0/DataDictionary/PDFHTML/EMSDEMSTATE/index.html) to better understand how each column should be used in future analyses. 

Table: selected_events.pickle
	Number of Rows: 95735
	Number of Columns: 13

**Column at Index 0: 'PcrKey'**
 - Datatype: object
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 95735

**Column at Index 1: 'eScene_01'**
 - Datatype: object
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 2

**Column at Index 2: 'eArrest_03'**
 - Datatype: object
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 3

**Column at Index 3: 'ePatient_13'**
 - Datatype: object
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 4

**Column at Index 4: 'eResponse_05'**
 - Datatype: object
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 3

**Column at Index 5: 'eDisposition_12'**
 - Datatype: object
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 8

**Column at Index 6: 'Urbanicity'**
 - Datatype: object
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 4

**Column at Index 7: 'ageinyear'**
 - Datatype: int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 94

**Column at Index 8: 'EpinephrineAdministered'**
 - Datatype: int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 2

**Column at Index 9: 'TotalDosesEpinephrine'**
 - Datatype: int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 23

**Column at Index 10: 'EMSDispatchCenterTimeSec'**
 - Datatype: float64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 1334

**Column at Index 11: 'EMSSystemResponseTimeMin'**
 - Datatype: float64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 1990

**Column at Index 12: 'TotalResponseTime'**
 - Datatype: float64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 9672

