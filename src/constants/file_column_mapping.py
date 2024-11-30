import sys
sys.path.insert(0, '/constants/file_column_mapping')

"""
This dictionary defines the column mapping for the primary tables of interest. To add tables to hte NEMSIS_PUB.db, 
add the table name(s) as key(s) and column mapping as a value string.
"""
file_column_mapping = {
    'ComputedElements.txt': "PcrKey'~|~'USCensusRegion'~|~'USCensusDivision'~|~'NasemsoRegion'~|~'Urbanicity'~|~'ageinyear'~|~'EMSDispatchCenterTimeSec'~|~'EMSChuteTimeMin'~|~'EMSSystemResponseTimeMin'~|~'EMSSceneResponseTimeMin'~|~'EMSSceneTimeMin'~|~'EMSSceneToPatientTimeMin'~|~'EMSTransportTimeMin'~|~'EMSTotalCallTimeMin'",
    'FACTPCRARRESTROSC.txt': "PcrKey'~|~'eArrest_12'",
    'FACTPCRARRESTRESUSCITATION.txt': "PcrKey'~|~'eArrest_03'",
    'FACTPCRARRESTWITNESS.txt': "PcrKey'~|~'eArrest_04'",
    'FACTPCRARRESTCPRPROVIDED.txt': "PcrKey'~|~'eArrest_09'",
    'FACTPCRMEDICATION.txt': "eMedications_01'~|~'PcrMedicationKey'~|~'PcrKey'~|~'eMedications_03'~|~'eMedications_03Descr'~|~'eMedications_05'~|~'eMedications_06'~|~'eMedications_07'~|~'eMedications_10'~|~'eMedications_02'",
    'Pub_PCRevents.txt': "PcrKey'~|~'eDispatch_01'~|~'eDispatch_02'~|~'eArrest_14'~|~'eArrest_01'~|~'eArrest_02'~|~'eArrest_05'~|~'eArrest_07'~|~'eArrest_11'~|~'eArrest_16'~|~'eArrest_18'~|~'eDisposition_12'~|~'eDisposition_19'~|~'eDisposition_16'~|~'eDisposition_21'~|~'eDisposition_22'~|~'eDisposition_23'~|~'eOutcome_01'~|~'eOutcome_02'~|~'ePatient_13'~|~'ePatient_15'~|~'ePatient_16'~|~'ePayment_01'~|~'ePayment_50'~|~'eResponse_05'~|~'eResponse_07'~|~'eResponse_15'~|~'eResponse_23'~|~'eScene_01'~|~'eScene_06'~|~'eScene_07'~|~'eScene_08'~|~'eScene_09'~|~'eSituation_02'~|~'eSituation_07'~|~'eSituation_08'~|~'eSituation_13'~|~'eSituation_01'~|~'eTimes_01'~|~'eTimes_03'~|~'eTimes_05'~|~'eTimes_06'~|~'eTimes_07'~|~'eTimes_09'~|~'eTimes_11'~|~'eTimes_12'~|~'eTimes_13'~|~'eDisposition_17'"
}
