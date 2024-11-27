import sqlite3
from pathlib import Path
import pandas as pd

def main():

    # create a new file to store the sqlite db 
    new_file = "./data/NEMSIS.db"

    # connect to db
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

    

    sql = '''
    CREATE TABLE medications(
    PcrKey INTEGER,
    eMedications_03 INTEGER,
    eMedications_03Descr VARCHAR(20),
    eMedications_05 DECIMAL(9, 3),
    eMedications_06 INTEGER
    )
    '''
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'medications.pickle'
    med_df = pd.read_pickle(data_fp)

    print(med_df.dtypes)
    med_df.fillna('-1', inplace=True)

    med_df['eMedications_03'] = med_df['eMedications_03'].replace('Unknown   ', '-1')
    med_df['eMedications_03'] = med_df['eMedications_03'].astype(float)
    med_df['PcrKey'] = med_df['PcrKey'].astype('int64')

    print(med_df.dtypes)
    print(med_df.shape)
    med_df.to_sql('medications', conn, if_exists = 'replace', index = False)


    sql = '''
    CREATE TABLE epinephrine(
    PcrKey INTEGER,
    eMedications_03 INTEGER,
    eMedications_03Descr VARCHAR(20),
    eMedications_05 DECIMAL(9, 3),
    eMedications_06 INTEGER
    )
    '''

    med_df = med_df[
        (med_df.eMedications_03 == 3992) | (med_df.eMedications_03 == 310116) | 
        (med_df.eMedications_03 == 310132) | (med_df.eMedications_03 == 317361) | 
        (med_df.eMedications_03 == 328314) | (med_df.eMedications_03 == 328316) | 
        (med_df.eMedications_03 == 330545) | (med_df.eMedications_03 == 372030) | 
        (med_df.eMedications_03 == 377281) | (med_df.eMedications_03 == 727316) | 
        (med_df.eMedications_03 == 727373) | (med_df.eMedications_03 == 727374) | 
        (med_df.eMedications_03 == 727386) | (med_df.eMedications_03 == 1100194) | 
        (med_df.eMedications_03 == 1233778) | (med_df.eMedications_03 == 1305268) 
    ]

    med_df['eMedications_05'] = med_df['eMedications_05'].astype(float)
    med_df['eMedications_06'] = med_df['eMedications_06'].str.strip()
    med_df['eMedications_06'] = med_df['eMedications_06'].astype(float)

    print(med_df.dtypes)
    print(med_df.shape)

    med_df.to_sql('epinephrine', conn, if_exists = 'replace', index = False)

    conn.commit()
    conn.close

if __name__ == "__main__":
    main()
