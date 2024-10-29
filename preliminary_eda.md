
# Preliminary EDA

We will review Aaron Fihn's prepared dataset *events_renamed* in order to learn the following:
- What columns are available?
- How many null values are there in each column?
- What is the datatype of each column? 
- What are some descriptive statistics about each column?

This info. will be paired with the [NEMSIS Data Dictionary](https://nemsis.org/media/nemsis_v3/release-3.5.0/DataDictionary/PDFHTML/EMSDEMSTATE/index.html) to better understand how each column should be used in future analyses. 

## *events_renamed*
**Rows:** 290559
**Columns:** 38

**Column at Index 0: 'PcrKey'**
 - Datatype: Int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 290559
 - Primary key, unique identifier for Patient Care Report (PCR)

**Column at Index 1: 'eDispatch_01'**
 - Datatype: Int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 42
 - Integer key for *"The dispatch reason reported to the responding unit."*

**Column at Index 2: 'eDispatch_02'**
 - Datatype: Int64
 - Number of Null Values: 135314  |  Percent Null: 46.57%
 - Number of Unique Values: 4
 - Integer key for *"Indication of whether Emergency Medical Dispatch was performed for this EMS event."*

**Column at Index 3: 'eArrest_01'**
 - Datatype: Int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 2
 - Integer key for *"Indication of the presence of a cardiac arrest at any time during this EMS event."*

**Column at Index 4: 'eArrest_02'**
 - Datatype: Int64
 - Number of Null Values: 11912  |  Percent Null: 4.1%
 - Number of Unique Values: 1
 - Integer key for *"Indication of the etiology or cause of the cardiac arrest (classified as cardiac, non-cardiac, etc.)."*

**Column at Index 5: 'CPR_Care_Provided_Prior_to_EMS_Arrival'**
 - Datatype: category
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 3
 - Categorical indicator for whether CPR care received: {"No", "Yes", "Unknown"}

**Column at Index 6: 'eArrest_07'**
 - Datatype: Int64
 - Number of Null Values: 14395  |  Percent Null: 4.95%
 - Number of Unique Values: 3
 - Integer key for *"Documentation of AED use Prior to EMS Arrival."*

**Column at Index 7: 'eArrest_11'**
 - Datatype: Int64
 - Number of Null Values: 38374  |  Percent Null: 13.21%
 - Number of Unique Values: 6
 - Integer key for *"Documentation of what the first monitored arrest rhythm which was noted."*

**Column at Index 8: 'eArrest_16'**
 - Datatype: Int64
 - Number of Null Values: 134937  |  Percent Null: 46.44%
 - Number of Unique Values: 6
 - Integer key for *"The reason that CPR or the resuscitation efforts were discontinued."*

**Column at Index 9: 'End_of_EMS_Cardiac_Arrest_Event'**
 - Datatype: category
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 4
 - Categorical indicator for the end of the cardiac event: {"Alive", "Dead", "Ongoing", "Unknown"}

**Column at Index 10: 'eDisposition_12'**
 - Datatype: Int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 22
 - Integer key for *"Type of disposition treatment and/or transport of the patient by this EMS Unit."*

**Column at Index 11: 'eDisposition_19'**
 - Datatype: Int64
 - Number of Null Values: 161193  |  Percent Null: 55.48%
 - Number of Unique Values: 4
 - Integer key for *"The acuity of the patient's condition after EMS care."*

**Column at Index 12: 'eDisposition_16'**
 - Datatype: Int64
 - Number of Null Values: 139442  |  Percent Null: 47.99%
 - Number of Unique Values: 9
 - Integer key for *"The method of transport by this EMS Unit."*

**Column at Index 13: 'eDisposition_21'**
 - Datatype: Int64
 - Number of Null Values: 145961  |  Percent Null: 50.23%
 - Number of Unique Values: 12
 - Integer key for *"The type of destination the patient was delivered or transferred to."*

**Column at Index 14: 'eDisposition_22'**
 - Datatype: Int64
 - Number of Null Values: 267949  |  Percent Null: 92.22%
 - Number of Unique Values: 20
 - Integer key for *"The location within the hospital that the patient was taken directly by EMS (e.g., Cath Lab, ICU, etc.)."*

**Column at Index 15: 'eDisposition_23'**
 - Datatype: Int64
 - Number of Null Values: 200647  |  Percent Null: 69.06%
 - Number of Unique Values: 16
 - Integer key for *"The primary hospital capability associated with the patient's condition for this transport (e.g., Trauma, STEMI, Peds, etc.)."*

**Column at Index 16: 'eOutcome_01'**
 - Datatype: category
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 3
 - Category for patient's outcome: {"Alive", "Dead", "Unknown"}

**Column at Index 17: 'eOutcome_02'**
 - Datatype: Int64
 - Number of Null Values: 288052  |  Percent Null: 99.14%
 - Number of Unique Values: 15
 - Integer key for "*The known disposition of the patient from the hospital, if admitted.*"

**Column at Index 18: 'ePatient_13'**
 - Datatype: Int64
 - Number of Null Values: 1236  |  Percent Null: 0.43%
 - Number of Unique Values: 3
 - Integer key for *"The patient's gender."*

**Column at Index 19: 'ePatient_15'**
 - Datatype: Int64
 - Number of Null Values: 2537  |  Percent Null: 0.87%
 - Number of Unique Values: 118
 - *"The patient's age (either calculated from date of birth or best approximation)."*

**Column at Index 20: 'ePatient_16'**
 - Datatype: Int64
 - Number of Null Values: 2363  |  Percent Null: 0.81%
 - Number of Unique Values: 5
 - Integer key for *"The unit used to define the patient's age."* (e.g., Days, Months, Years, etc.)

**Column at Index 21: 'ePayment_01'**
 - Datatype: Int64
 - Number of Null Values: 177345  |  Percent Null: 61.04%
 - Number of Unique Values: 12
 - Integer key for *"The primary method of payment or type of insurance associated with this EMS encounter."*

**Column at Index 22: 'ePayment_50'**
 - Datatype: Int64
 - Number of Null Values: 198583  |  Percent Null: 68.35%
 - Number of Unique Values: 9
 - Integer key for *"The CMS service level for this EMS encounter."*

**Column at Index 23: 'eResponse_05'**
 - Datatype: Int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 7
 - Integer key for *"The type of service or category of service requested of the EMS Agency responding for this specific EMS event."*

**Column at Index 24: 'eResponse_07'**
 - Datatype: Int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 6
 - Integer key for *"The transport and equipment capabilities of the EMS Unit which responded to this specific EMS event."*

**Column at Index 25: 'eResponse_15'**
 - Datatype: Int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 12
 - Integer key for *"The level of care (BLS or ALS) the unit is able to provide based on the units' treatment capabilities for this EMS response."*

**Column at Index 26: 'eResponse_23'**
 - Datatype: Int64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 4
 - Integer key for *"The indication whether the response was emergent or non-emergent. An emergent response is an immediate response."*

**Column at Index 27: 'eScene_01'**
 - Datatype: Int64
 - Number of Null Values: 79846  |  Percent Null: 27.48%
 - Number of Unique Values: 2
 - Integer key for *"Documentation that this EMS Unit was the first EMS Unit among all EMS Agencies on the Scene."*

**Column at Index 28: 'eScene_06'**
 - Datatype: Int64
 - Number of Null Values: 13571  |  Percent Null: 4.67%
 - Number of Unique Values: 3
 - Integer key for *"Indicator of how many total patients were at the scene."*

**Column at Index 29: 'eScene_07'**
 - Datatype: Int64
 - Number of Null Values: 63418  |  Percent Null: 21.83%
 - Number of Unique Values: 2
 - Integer key for *"...if this event would be considered a mass casualty incident (overwhelmed existing EMS resources)."*

**Column at Index 30: 'eScene_08'**
 - Datatype: Int64
 - Number of Null Values: 287468  |  Percent Null: 98.94%
 - Number of Unique Values: 5
 - Integer key for *"The color associated with the initial triage assessment/classification of the MCI patient."*

**Column at Index 31: 'eSituation_02'**
 - Datatype: Int64
 - Number of Null Values: 15342  |  Percent Null: 5.28%
 - Number of Unique Values: 3
 - Integer key for *"Indication whether or not there was an injury."*

**Column at Index 32: 'eSituation_07'**
 - Datatype: Int64
 - Number of Null Values: 99806  |  Percent Null: 34.35%
 - Number of Unique Values: 9
 - Integer key for *"The primary anatomic location of the chief complaint as identified by EMS personnel."*

**Column at Index 33: 'eSituation_08'**
 - Datatype: Int64
 - Number of Null Values: 97053  |  Percent Null: 33.4%
 - Number of Unique Values: 11
 - Integer key for *"The primary organ system of the patient injured or medically affected."*

**Column at Index 34: 'eSituation_13'**
 - Datatype: Int64
 - Number of Null Values: 71141  |  Percent Null: 24.48%
 - Number of Unique Values: 4
 - Integer key for *"The acuity of the patient's condition upon EMS arrival at the scene."*

**Column at Index 35: 'eDisposition_17'**
 - Datatype: Int64
 - Number of Null Values: 162723  |  Percent Null: 56.0%
 - Number of Unique Values: 4
 - Integer key for *"Indication whether the transport was emergent or non-emergent."*

**Column at Index 36: 'Urbanicity'**
 - Datatype: string
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 4
 - String for the patient's Urbanicity: {"R": "Rural", "U": "Urban", "S": "Suburban", "W": "Wilderness"}

**Column at Index 37: 'ageinyear'**
 - Datatype: string
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 120
 - Column with the patient's age in years. Note: stored in string, needs conversion to int. 