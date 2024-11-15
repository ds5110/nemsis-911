import sqlite3
import csv

table_definitions = {
    "Pub_PCRevents": """
        CREATE TABLE Pub_PCRevents (
            PcrKey TEXT PRIMARY KEY,
            eDispatch_01 TEXT,
            eDispatch_02 TEXT,
            eArrest_14 TEXT,
            eArrest_01 TEXT,
            eArrest_02 TEXT,
            eArrest_05 TEXT,
            eArrest_07 TEXT,
            eArrest_11 TEXT,
            eArrest_16 TEXT,
            eArrest_18 TEXT,
            eDisposition_12 TEXT,
            eDisposition_19 TEXT,
            eDisposition_16 TEXT,
            eDisposition_21 TEXT,
            eDisposition_22 TEXT,
            eDisposition_23 TEXT,
            eOutcome_01 TEXT,
            eOutcome_02 TEXT,
            ePatient_13 TEXT,
            ePatient_15 TEXT,
            ePatient_16 TEXT,
            ePayment_01 TEXT,
            ePayment_50 TEXT,
            eResponse_05 TEXT,
            eResponse_07 TEXT,
            eResponse_15 TEXT,
            eResponse_23 TEXT,
            eScene_01 TEXT,
            eScene_06 TEXT,
            eScene_07 TEXT,
            eScene_08 TEXT,
            eScene_09 TEXT,
            eSituation_02 TEXT,
            eSituation_07 TEXT,
            eSituation_08 TEXT,
            eSituation_13 TEXT,
            eSituation_01 TEXT,
            eTimes_01 TEXT,
            eTimes_03 TEXT,
            eTimes_05 TEXT,
            eTimes_06 TEXT,
            eTimes_07 TEXT,
            eTimes_09 TEXT,
            eTimes_11 TEXT,
            eTimes_12 TEXT,
            eTimes_13 TEXT,
            eDisposition_17 TEXT
        )
    """,
    "ComputedElements": """
        CREATE TABLE ComputedElements (
            PcrKey TEXT PRIMARY KEY,
            USCensusRegion TEXT,
            USCensusDivision TEXT,
            NasemsoRegion TEXT,
            Urbanicity TEXT,
            ageinyear INTEGER, 
            EMSDispatchCenterTimeSec INTEGER,
            EMSChuteTimeMin INTEGER,
            EMSSystemResponseTimeMin INTEGER,
            EMSSceneResponseTimeMin INTEGER,
            EMSSceneTimeMin INTEGER,
            EMSSceneToPatientTimeMin INTEGER,
            EMSTransportTimeMin INTEGER,
            EMSTotalCallTimeMin INTEGER,
            FOREIGN KEY (PcrKey) REFERENCES Pub_PCRevents(PcrKey)
        )
    """,
    "FACTPCRARRESTROSC": """
        CREATE TABLE FACTPCRARRESTROSC (
            PcrKey TEXT PRIMARY KEY,
            eArrest_12 TEXT,
            FOREIGN KEY (PcrKey) REFERENCES Pub_PCRevents(PcrKey) 
        )
    """,
    "FACTPCRARRESTWITNESS": """
        CREATE TABLE FACTPCRARRESTWITNESS (
            PcrKey TEXT PRIMARY KEY, 
            eArrest_04 TEXT,
            FOREIGN KEY (PcrKey) REFERENCES Pub_PCRevents(PcrKey) 
        )
    """,
    "FACTPCRMEDICATION": """
        CREATE TABLE FACTPCRMEDICATION (
            eMedications_01 TEXT,
            PcrMedicationKey TEXT PRIMARY KEY,
            PcrKey TEXT, 
            eMedications_03 TEXT,
            eMedications_03Descr TEXT, 
            eMedications_05 TEXT,
            eMedications_06 TEXT,
            eMedications_07 TEXT, 
            eMedications_10 TEXT,
            eMedications_02 TEXT,
            FOREIGN KEY (PcrKey) REFERENCES Pub_PCRevents(PcrKey)
        )
    """
}

conn = sqlite3.connect('../db/NEMSIS_PUB.db') 
cursor = conn.cursor()

for table_name, create_table_sql in table_definitions.items():
    cursor.execute(create_table_sql)
conn.commit()
conn.close()
print("SQLite database 'NEMSIS_PUB.db' created with tables.")
