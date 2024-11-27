import sqlite3
from pathlib import Path
import pandas as pd

def main():
    new_file = "./data/NEMSIS.db"

    conn = sqlite3.connect(new_file)

    cursor = conn.cursor()

    sql = '''
    CREATE TABLE resuscitation(
    PcrKey INTEGER, 
    eArrest_03 INTEGER
    )
    '''

    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'pcr_arrest_resuscitation.pickle'
    resus_df = pd.read_pickle(data_fp)
    resus_df.to_sql('resuscitation', conn, if_exists = 'replace', index = False)

    sql = '''
    CREATE TABLE events(
    PcrKey INTEGER,
    eDispatch_01 INTEGER,
    eDispatch_02 INTEGER,
    eArrest_01 INTEGER,
    eArrest_02 INTEGER,
    eArrest_05 INTEGER,
    eArrest_07 INTEGER,
    eArrest_11 INTEGER,
    eArrest_16 INTEGER,
    eArrest_18 INTEGER,
    eDisposition_12 INTEGER,
    eDisposition_19 INTEGER,
    eDisposition_16 INTEGER,
    eDisposition_21 INTEGER,
    eDisposition_22 INTEGER,
    eDisposition_23 INTEGER,
    eOutcome_01 INTEGER,
    eOutcome_02 INTEGER,
    ePatient_13 INTEGER,
    ePatient_15 INTEGER,
    ePatient_16 INTEGER,
    ePayment_01 INTEGER,
    ePayment_50 INTEGER,
    eResponse_05 INTEGER,
    eResponse_07 INTEGER,
    eResponse_15 INTEGER,
    eResponse_23 INTEGER,
    eScene_01 INTEGER,
    eScene_06 INTEGER,
    eScene_07 INTEGER,
    eScene_08 INTEGER,
    eSituation_02 INTEGER,
    eSituation_07 INTEGER,
    eSituation_08 INTEGER,
    eSituation_13 INTEGER,
    eDisposition_17 INTEGER,
    Urbanicity VARCHAR(20),
    ageinyear INTEGER
    )
    '''
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events.pickle'
    events_df = pd.read_pickle(data_fp)
    events_df.to_sql('events', conn, if_exists = 'replace', index = False)



    sql = '''
    CREATE TABLE race(
    PcrKey INTEGER, 
    ePatient_14 INTEGER
    )
    '''

    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'race.pickle'
    race_df = pd.read_pickle(data_fp)
    race_df.to_sql('race', conn, if_exists = 'replace', index = False)



    conn.commit()
    conn.close

if __name__ == "__main__":
    main()
