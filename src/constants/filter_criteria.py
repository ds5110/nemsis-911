import sys
sys.path.insert(0, '/constants/filter_criteria')

# exclude pediatric cases
age_lower_limit = 18 

# should abnormally high ages be capped, were there really 120 year olds?
age_upper_limit = 115 

# abnormal response time per Peters et al. defined as > 60 minutes.
abnormal_response_time_min = 60

"""
eDisposition_12 - Type of disposition treatment and/or 
                transport of the patient by this EMS Unit

Rationale - These included codes were chosen due to the rationale in the 
            Peters et al. paper: 
    
    "Finally, we only included incidents in which one EMS unit provided 
    treatment until the end of the event, either until the patient was 
    transported to a receiving facility or if resuscitative efforts were
    attempted but terminated by the responding unit prior to transport."

            Some codes, like 'Assist' are vague. Typically we included 
            codes where treatment was provided, and transported by one unit,
            and excluded codes where either treatment was not provided, 
            or it was likely that transport happened with more than one unit.

Included Codes:
"4212001" - Assist, Agency
"4212003" -	Assist, Public
"4212005" - Assist, Unit
"4212017" -	Patient Dead at Scene-Resuscitation Attempted (With Transport)
"4212019" -	Patient Dead at Scene-Resuscitation Attempted (Without Transport)
"4212027" -	Patient Treated, Released (AMA)
"4212029" -	Patient Treated, Released (per protocol)
"4212033" -	Patient Treated, Transported by this EMS Unit

Excluded Codes:
"4212007" - Canceled (Prior to Arrival At Scene)
"4212009" - Canceled on Scene (No Patient Contact)
"4212011" -	Canceled on Scene (No Patient Found)
"4212013" -	Patient Dead at Scene-No Resuscitation Attempted (With Transport)
"4212015" -	Patient Dead at Scene-No Resuscitation Attempted (Without Transport)
"4212021" -	Patient Evaluated, No Treatment/Transport Required
"4212023" -	Patient Refused Evaluation/Care (With Transport)
"4212025" -	Patient Refused Evaluation/Care (Without Transport)
"4212031" -	Patient Treated, Transferred Care to Another EMS Unit
"4212035" -	Patient Treated, Transported by Law Enforcement
"4212037" -	Patient Treated, Transported by Private Vehicle
"4212039" -	Standby-No Services or Support Provided
"4212041" -	Standby-Public Safety, Fire, or EMS Operational Support Provided
"4212043" -	Transport Non-Patient, Organs, etc.
"""
eDisposition_12_codes = [
    4212001, 4212003, 4212005, 4212017,
    4212019, 4212027, 4212029, 4212033
]


"""
eArrest_01 - Indication of the presence of a cardiac arrest 
                at any time during this EMS event.

Included:
3001003	- Yes, Prior to Any EMS Arrival (includes Transport EMS & Medical First Responders)
3001005	- Yes, After Any EMS Arrival (includes Transport EMS & Medical First Responders)
"""
eArrest_01_codes = [3001003, 3001005] 


"""
eArrest_02 - Indication of the etiology or cause of the cardiac arrest 
                (classified as cardiac, non-cardiac, etc.).

Rationale: other codes are excluded as the Peters et al. paper filtered
                other cardiac events from 'traumatic cause'

Included:
3002001	- Cardiac (Presumed)
"""
eArrest_02_codes = [3002001]  


"""
eArrest_03 - Indication of an attempt to resuscitate the patient who is in 
                cardiac arrest (attempted, not attempted due to DNR, etc.).

Rationale: other codes are excluded as they are cases where resuscitation
                was not attempted.

Included: 
3003001	- Attempted Defibrillation
3003003	- Attempted Ventilation
3003005	- Initiated Chest Compressions
"""
eArrest_03_codes = [3003001, 3003003, 3003005]


"""
eResponse_05 - The type of service or category of service requested of 
                the EMS Agency responding for this specific EMS event.

Rationale: response codes included, other codes not for scene response.

Included:
2205001 - Emergency Response (Primary Response Area)
2205003	- Emergency Response (Intercept)
2205009	- Emergency Response (Mutual Aid)
"""
eResponse_05_codes = [2205001, 2205003, 2205009]


"""
eScene_01 - Documentation that this EMS Unit was the first EMS Unit 
                among all EMS Agencies on the Scene.

Rationale: ambiguous, should only the first unit on scene be included?

Included (Null codes excluded):
9923001 - No
9923003	- Yes
"""
eScene_01_codes = [9923003, 9923001]


"""
eMedications_03 - List of medications based on RxNorm (RXCUI) code 
                    and SNOMED-CT codes for blood products. 

Rationale: the following codes were included as they are various
            codes in the medications database where eMedications_03Descr
            is for pure epinephrine, with no mixes of epinephrine and other
            drugs. 

Included:
3992 - Epinephrine  
310116 - Epinephrine 0.1 MG/ML Injectable Solution 
310132 - EPINEPHrine 1 MG/ML Injectable Solution 
317361 - EPINEPHrine 0.1 MG/ML  
328314 - Epinephrine 10 MG/ML  
328316 - Epinephrine 1 MG/ML  
330545 - EPINEPHrine 0.01 MG/ML  
372030 - Epinephrine Injectable Solution   
377281 - Epinephrine Inhalant Solution 
727316 - 0.3 ML Epinephrine 0.5 MG/ML Prefilled Syringe 
727373 - 10 ML Epinephrine 0.1 MG/ML Prefilled Syringe  
727374 - 1 ML Epinephrine 1 MG/ML Prefilled Syringe  
727386 - 0.3 ML Epinephrine 0.5 MG/ML Prefilled Syringe [Epipen]
1100194 - 10 ML EPINEPHrine 0.016 MG/ML Prefilled Syringe 
1233778 - 10 ML EPINEPHrine 0.01 MG/ML Prefilled Syringe 
1305268 - 0.15 ML Epinephrine 1 MG/ML Prefilled Syringe [Auvi-Q] 
"""
epinephrine_medication_codes = [
    3992, 310116, 310132, 317361, 
    328314, 328316, 330545, 372030, 
    377281, 727316, 727373, 727374,
    727386, 1100194, 1233778, 1305268
]
