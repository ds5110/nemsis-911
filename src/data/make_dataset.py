import logging
import numpy as np
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p',
                        level=logging.DEBUG)

    logger.info("Running make_dataset.py")
    df = cardiac_arrest_case_definition_pcr()

    # figure out which rows to keep from the original
    event_fp = Path(__file__).parent.parent.parent / 'data' / 'csv' / 'Pub_PCRevents.csv'
    with open(event_fp) as f:
        num_rows = sum(1 for _ in f)
    all_rows = np.arange(1, num_rows)
    keep_rows = np.asarray(df['LineNum'])

    logger.debug("Calculating which rows in Pub_PCRevents.txt to skip...")
    skip_rows = set(np.setdiff1d(all_rows, keep_rows))
    logger.debug(f"Skipping {len(skip_rows)} rows, saving {keep_rows.size}.")
    del all_rows
    del keep_rows
    events_df = events_df_filtered_rows(skip_rows)
    logger.debug("Dropping irrelevant columns")
    column_names_to_drop = ['eArrest_14', 'eScene_09', 'eSituation_01', 'eTimes_01', 'eTimes_03', 'eTimes_05',
                            'eTimes_06', 'eTimes_07', 'eTimes_09', 'eTimes_11', 'eTimes_12', 'eTimes_13']
    events_df.drop(columns=column_names_to_drop, inplace=True)

    # join with ComputedElements.csv to bring in Urbanicity
    comp_elements_df = computed_elements()
    events_df = events_df.merge(comp_elements_df, on='PcrKey', suffixes=(None, '_y'))






    # ---------------------- TJ 11/10 - add in new csvs to join ---------------------------- #
  
    arrest_rosc_df = fact_pcr_arrest_rosc()
    arrest_rosc_df = arrest_rosc_df.replace(to_replace=[7701001, 7701003, 7701005], value=pd.NA)  # replace NEMSIS NOT values
    logger.debug("Save arrest_rosc.pickle")
    save_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'arrest_rosc.pickle'
    arrest_rosc_df.to_pickle(path=save_path)
    #events_df = events_df.merge(arrest_rosc_df, on='PcrKey', suffixes=(None, '_y'))

    pcr_arrest_witness = fact_pcr_arrest_witness()
    pcr_arrest_witness = pcr_arrest_witness.replace(to_replace=[7701001, 7701003, 7701005], value=pd.NA)  # replace NEMSIS NOT values
    logger.debug("Save arrest_witness.pickle")
    save_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'arrest_witness.pickle'
    pcr_arrest_witness.to_pickle(path=save_path)
    #events_df = events_df.merge(pcr_arrest_witness, on='PcrKey', suffixes=(None, '_y'))

    medications_df = fact_pcr_medication() 
    medications_df = medications_df.replace(to_replace=[7701001, 7701003, 7701005], value=pd.NA)  # replace NEMSIS NOT values
    logger.debug("Save medications.pickle")
    save_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'medications.pickle'
    medications_df.to_pickle(path=save_path)
    #events_df = events_df.merge(medications_df, on='PcrKey', suffixes=(None, '_y'))

    race_df = pcr_patient_race_group()
    race_df = race_df.replace(to_replace=[7701001, 7701003, 7701005], value=pd.NA)  # replace NEMSIS NOT values
    logger.debug("Save race.pickle")
    save_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'race.pickle'
    race_df.to_pickle(path=save_path)
    #events_df = events_df.merge(race_df, on='PcrKey', suffixes=(None, '_y'))


    resus_df = fact_pcr_arrest_resuscitation()
    resus_df = resus_df.replace(to_replace=[7701001, 7701003, 7701005], value=pd.NA)  # replace NEMSIS NOT values
    logger.debug("Save pcr_arrest_resuscitation.pickle")
    save_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'pcr_arrest_resuscitation.pickle'
    resus_df.to_pickle(path=save_path)


    # -------------------------------------------------------------------------------------- #

    events_df = events_df.convert_dtypes()
    events_df = events_df.replace(to_replace=[7701001, 7701003, 7701005], value=pd.NA)  # replace NEMSIS NOT values
    logger.debug("Save events.pickle")
    save_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events.pickle'
    events_df.to_pickle(path=save_path)
    logger.info("Finished make_dataset.py")


def events_df_with_key_filtering_columns() -> pd.DataFrame:
    """Return a DataFrame from Pub_PCRevents.txt with index PcrKeyIndex with columns PcrKey, eArrest_01, eArrest_02, and LineNum.

    Quotes are removed from column names. LineNum is the zero-indexed original line number (header is line zero).
    Limiting the DataFrame to just these columns makes it small enough to fit in-memory. These columns can be used with
    other data to determine which patient care records meet the NEMSIS v3 case definition of cardiac arrest.
    """
    logger.info("Reading key filtering columns from Pub_PCRevents.txt. Takes 5-10 minutes, there's ~51MM rows.")

    # read_csv() must use the python parsing engine because the separator is multi-character. This means the low_memory
    # argument doesn't work. Instead, do chunking and column filtering manually.
    fp = _get_interim_path() / 'Pub_PCRevents.txt'
    text_file_reader = pd.read_csv(fp,
                                   sep=r'~\|~',
                                   usecols=["'PcrKey'", "'eArrest_01'", "'eArrest_02'"],
                                   dtype=np.int32,
                                   engine='python',
                                   chunksize=1_000_000)
    with text_file_reader as reader:
        dataframe_chunks: list[pd.DataFrame] = []
        lines_read = 0
        for chunk in reader:
            dataframe_chunks.append(chunk)
            lines_read += chunk.shape[0]
            logger.info(f'Pub_PCRevents.txt lines read (millions): {lines_read // 1_000_000}')
    events_df = pd.concat(dataframe_chunks)

    # Remove the quotes from the column names
    mapper = {quoted: _unquote_column_names(quoted) for quoted in events_df.columns.to_list()}
    events_df.rename(mapper=mapper, inplace=True, axis='columns')

    # Save the line number; we'll need this later when we filter by rows
    events_df['LineNum'] = events_df.index + 1

    # Use PcrKey as the index
    events_df['PcrKeyIndex'] = events_df['PcrKey']
    events_df.set_index(keys='PcrKeyIndex', inplace=True)
    logger.info("Finished reading key filtering columns from Pub_PCRevents.txt")
    return events_df


def filter_to_i46() -> pd.DataFrame:
    """Returns a DataFrame of all patient care record keys with a symptom/impression of cardiac arrest.

    A patient care record has a symptom or impression of cardiac arrest when at least one of elements
    eSituation.09, eSituation.10, eSituation.11, or eSituation.12 are an ICD code that begins with
    'I46'. For further information, see
    https://nemsis.org/media/nemsis_v3/master/CaseDefinitions/CardiacArrest.pdf.

    PcrKey is used for both the index and the column name.
    """
    logger.info("Reading from FACTPCRPRIMARYSYMPTOM.txt")
    primary_symptom_filepath = _get_interim_path() / 'FACTPCRPRIMARYSYMPTOM.txt'
    primary_symptom_df = read_nemsis_file_to_df(primary_symptom_filepath)
    primary_symptom_df = primary_symptom_df[primary_symptom_df.eSituation_09.str.startswith('I46')]
    primary_symptom_df = primary_symptom_df[['PcrKey']].set_index(keys='PcrKey')
    logger.info("Finished reading from FACTPCRPRIMARYSYMPTOM.txt")

    logger.info("Reading from FACTPCRADDITIONALSYMPTOM.txt")
    other_symptoms_filepath = _get_interim_path() / 'FACTPCRADDITIONALSYMPTOM.txt'
    other_symptoms_df = read_nemsis_file_to_df(other_symptoms_filepath)
    other_symptoms_df = other_symptoms_df[other_symptoms_df.eSituation_10.str.startswith('I46')]
    other_symptoms_df = other_symptoms_df[['PcrKey']].set_index(keys='PcrKey')
    logger.info("Finished reading from FACTPCRADDITIONALSYMPTOM.txt")

    logger.info("Reading from FACTPCRPRIMARYIMPRESSION.txt")
    primary_impression_filepath = _get_interim_path() / 'FACTPCRPRIMARYIMPRESSION.txt'
    primary_impression_df = read_nemsis_file_to_df(primary_impression_filepath)
    primary_impression_df = primary_impression_df[primary_impression_df.eSituation_11.str.startswith('I46')]
    primary_impression_df = primary_impression_df[['PcrKey']].set_index(keys='PcrKey')
    logger.info("Finished reading from FACTPCRPRIMARYIMPRESSION.txt")

    logger.info("Reading from FACTPCRSECONDARYIMPRESSION.txt")
    secondary_impression_filepath = _get_interim_path() / 'FACTPCRSECONDARYIMPRESSION.txt'
    secondary_impression_df = read_nemsis_file_to_df(secondary_impression_filepath)
    secondary_impression_df = secondary_impression_df[secondary_impression_df.eSituation_12.str.startswith('I46')]
    secondary_impression_df = secondary_impression_df[['PcrKey']].set_index(keys='PcrKey')
    logger.info("Finished reading from FACTPCRSECONDARYIMPRESSION.txt")

    relevant_pcr_df = [primary_symptom_df,
                       other_symptoms_df,
                       primary_impression_df,
                       secondary_impression_df]
    pcr_key_df = pd.concat(relevant_pcr_df).drop_duplicates().astype('int32')
    return pcr_key_df


def events_df_filtered_rows(skip_rows: set[int]) -> pd.DataFrame:
    """Returns a dataframe of PUB_PCREvents.txt filtered to just rows that have the specified PCR keys.

    Keyword arguments:
    skip_rows: array of rows to skip. (0-indexed, starting with the header)
    """
    fp = Path(__file__).parent.parent.parent / 'data' / 'csv' / 'Pub_PCRevents.csv'

    logger.info("Reading only cardiac arrest rows from Pub_PCRevents.csv. Takes 5-10 minutes, there's ~51MM rows.")
    text_file_reader = pd.read_csv(fp,
                                   skiprows=lambda row: row in skip_rows,
                                   chunksize=1_000_000)
    logger.debug("creating a text_file_reader")
    with text_file_reader as reader:
        logger.debug("successfully created a text_file_reader")
        dataframe_chunks: list[pd.DataFrame] = []
        lines_saved = 0
        chunks_read = 0
        logger.debug("Trying to read a chunk")
        for chunk in reader:  # it breaks here.
            logger.debug("Successfully read a chunk")
            dataframe_chunks.append(chunk)
            chunks_read += 1
            logger.debug(f"Pub_PCRevents.txt chunks read: {chunks_read}")
            lines_saved += chunk.shape[0]
            logger.info(f"Pub_PCRevents.txt lines saved: {lines_saved}")
    logger.info("Finished reading only cardiac arrest rows from Pub_PCRevents.txt")

    events_df = pd.concat(dataframe_chunks)
    mapper = {quoted: _unquote_column_names(quoted) for quoted in events_df.columns.to_list()}
    events_df.rename(mapper=mapper, inplace=True, axis='columns')
    logger.info("exiting events_df_filtered_rows()")
    return events_df


def cardiac_arrest_case_definition_pcr() -> pd.DataFrame:
    """Return patient care reports that satisfy the NEMSIS v3 case definition of cardiac arrest.

    Returns: DataFrame with the following columns:
        PcrKey -- The PCR id
        LineNum -- The 0-indexed line number of that PCR in Pub_PCRevents.txt (excluding the header row)
    """
    logger.debug("entering cardiac_arrest_case_definition()")
    df = events_df_with_key_filtering_columns()  # PcrKey index, eArrest_01/02, LineNum

    # Get patient care reports where any symptom or impression is cardiac arrest
    cardiac_arrest_symptom_or_impression_df = filter_to_i46()

    # Get relevant NEMSIS code values for eArrest_01 and eArrest_02
    yes_prior_to_ems_arrival_code = 3001003
    yes_after_any_ems_arrival_code = 3001005
    etiology_cardiac_code = 3002001
    etiology_cardiac_or_blank_codes = [3002001, 7701001, 7701003]

    logging.info("Identifying records where cardiac arrest occurred prior to EMS arrival and "
                 "etiology is presumed cardiac or blank")
    occurred_prior_to_ems_arrival = df[df['eArrest_01'] == yes_prior_to_ems_arrival_code][['PcrKey', 'LineNum']]
    etiology_cardiac_or_blank = df[df['eArrest_02'].isin(etiology_cardiac_or_blank_codes)][['PcrKey', 'LineNum']]
    option_1_pcr_key = occurred_prior_to_ems_arrival.merge(etiology_cardiac_or_blank,
                                                           on='PcrKey',
                                                           suffixes=(None, '_y'))
    option_1_pcr_key = option_1_pcr_key[['PcrKey', 'LineNum']]

    logging.info("Identifying records where cardiac arrest occurred after EMS arrival and "
                 "etiology is presumed cardiac")
    occurred_after_ems_arrival = df[df['eArrest_01'] == yes_after_any_ems_arrival_code][['PcrKey', 'LineNum']]
    etiology_cardiac = df[df['eArrest_02'] == etiology_cardiac_code][['PcrKey', 'LineNum']]
    option_2_pcr_key = occurred_after_ems_arrival.merge(etiology_cardiac,
                                                        on='PcrKey',
                                                        suffixes=(None, '_y'))
    option_2_pcr_key = option_2_pcr_key[['PcrKey', 'LineNum']]

    logging.info("Finding the union of those two options")
    either_option = pd.concat([option_1_pcr_key, option_2_pcr_key]).drop_duplicates()

    # Get patient care reports that satisfy the cardiac arrest case definition
    results = either_option.merge(cardiac_arrest_symptom_or_impression_df,
                                  on='PcrKey',
                                  suffixes=(None, '_y'))
    results = results[['PcrKey', 'LineNum']].drop_duplicates()
    logger.debug("exiting cardiac_arrest_case_definition()")
    return results


def computed_elements() -> pd.DataFrame:
    """Read relevant columns from ComputedElements.csv into a DataFrame.

    Relevant columns are PcrKey, Urbanicity, and ageinyear."""
    logger.debug("entering computed_elements()")
    fp = Path(__file__).parent.parent.parent / 'data' / 'csv' / 'ComputedElements.csv'
    usecols = ["'PcrKey'", "'Urbanicity'", "'ageinyear'", "'EMSDispatchCenterTimeSec'", "'EMSSystemResponseTimeMin'"]
    df = pd.read_csv(fp, usecols=usecols)

    # Remove quotes from column names
    mapper = {quoted_col: _unquote_column_names(quoted_col) for quoted_col in usecols}
    df.rename(mapper=mapper, axis='columns', inplace=True)

    # rename Urban/Suburban/Rural/Wilderness to U/S/R/W
    df['Urbanicity'] = df['Urbanicity'].map(lambda s: s[0])

    # drop rows with a missing Urbanicity value
    df = df[df['Urbanicity'].isin(['U', 'S', 'R', 'W'])]

    logger.debug("exiting computed_elements()")
    return df


def _get_interim_path() -> Path:
    """Return an absolute path to the directory PROJECT_ROOT/data/interim."""
    return Path(__file__).parent.parent.parent / 'data' / 'interim'


def read_nemsis_file_to_df(filepath: Path, *, usecols: str | list[str] | None = None) -> pd.DataFrame:
    """Import an original NEMSIS text file to a DataFrame.

    Keyword arguments:
    filepath -- an absolute path to the file
    usecols -- the unquoted column name or names to import (default is all columns)
    """
    quoted_cols = _quote_column_names(usecols)
    dtype = None
    if usecols is not None:
        dtype = {}
        for col in quoted_cols:
            dtype[col] = np.int32
    df = pd.read_csv(filepath,
                     sep=r'~\|~',      # treated as a regular expression, so the pipe must be escaped
                     usecols=quoted_cols,
                     dtype=dtype,
                     engine='python')  # prevents warning messages when using multi-character separators
    # Column names are wrapped in extraneous single quotes. Remove them.
    df.rename(mapper=lambda n: _unquote_column_names(n), axis='columns', inplace=True)
    return df































def fact_pcr_arrest_rosc() -> pd.DataFrame:
    """
    Read relevent columns from FACTPCRARRESTROSC.csv into a DataFrame.

    Relevant columns are PcrKey, eArrest_12
    """
    logger.debug("entering fact_pcr_arrest_rosc()")
    fp = Path(__file__).parent.parent.parent / 'data' / 'csv' / 'FACTPCRARRESTROSC.csv'
    usecols = ["'PcrKey'", "'eArrest_12'"]
    df = pd.read_csv(fp, usecols = usecols)

    # Remove quotes from column names
    mapper = {quoted_col: _unquote_column_names(quoted_col) for quoted_col in usecols}
    df.rename(mapper=mapper, axis='columns', inplace=True)

    #TODO: unclear if NAs need to be removed like Aaron did in computed_elements()

    logger.debug("exiting fact_pcr_arrest_rosc()")
    return df


def fact_pcr_arrest_resuscitation() -> pd.DataFrame:
    """
    Read relevent columns from FACTPCRARRESTRESUSCITATION.csv into a DataFrame.

    Relevant columns are PcrKey, eArrest_12
    """
    logger.debug("entering fact_pcr_arrest_resuscitation()")
    fp = Path(__file__).parent.parent.parent / 'data' / 'csv' / 'FACTPCRARRESTRESUSCITATION.csv'
    usecols = ["'PcrKey'", "'eArrest_03'"] 
    df = pd.read_csv(fp, usecols = usecols)

    # Remove quotes from column names
    mapper = {quoted_col: _unquote_column_names(quoted_col) for quoted_col in usecols}
    df.rename(mapper=mapper, axis='columns', inplace=True)

    #TODO: unclear if NAs need to be removed like Aaron did in computed_elements()

    logger.debug("exiting fact_pcr_arrest_resuscitation()")
    return df



def fact_pcr_arrest_witness() -> pd.DataFrame:
    """
    Read relevent columns from FACTPCRARRESTWITNESS.csv into a DataFrame.

    Relevant columns are 'PcrKey', 'eArrest_04'
    """
    logger.debug("entering fact_pcr_arrest_witness()")
    fp = Path(__file__).parent.parent.parent / 'data' / 'csv' / 'FACTPCRARRESTWITNESS.csv'
    usecols = ["'PcrKey'", "'eArrest_04'"]
    df = pd.read_csv(fp, usecols = usecols)

    # Remove quotes from column names
    mapper = {quoted_col: _unquote_column_names(quoted_col) for quoted_col in usecols}
    df.rename(mapper=mapper, axis='columns', inplace=True)

    #TODO: unclear if NAs need to be removed like Aaron did in computed_elements()

    logger.debug("exiting fact_pcr_arrest_witness()")
    return df


def fact_pcr_medication() -> pd.DataFrame:
    """
    Read relevant columns from FACTPCRMEDICATION.csv into a DataFrame.

    Relevant columns are 'PcrKey', 'eMedications_03', 'eMedications_03Descr', 
                        'eMedications_05', 'eMedications_06'
    """
    logger.debug("entering fact_pcr_medication()")
    fp = Path(__file__).parent.parent.parent / 'data' / 'csv' / 'FACTPCRMEDICATION.csv'
    usecols = ["'PcrKey'", "'eMedications_03'", "'eMedications_03Descr'", 
        "'eMedications_05'", "'eMedications_06'"
    ]
    df = pd.read_csv(fp, usecols = usecols)

    # Remove quotes from column names
    mapper = {quoted_col: _unquote_column_names(quoted_col) for quoted_col in usecols}
    df.rename(mapper=mapper, axis='columns', inplace=True)

    #TODO: unclear if NAs need to be removed like Aaron did in computed_elements()

    logger.debug("exiting fact_pcr_medication()")
    return df


def pcr_patient_race_group() -> pd.DataFrame:
    """
    Read relevent columns from PCRPATIENTRACEGROUP.csv into a DataFrame.

    Relevant columns are 'PcrKey', 'ePatient_14'
    """
    logger.debug("entering pcr_patient_race_group()")
    fp = Path(__file__).parent.parent.parent / 'data' / 'csv' / 'PCRPATIENTRACEGROUP.csv'
    usecols = ["'PcrKey'", "'ePatient_14'"]
    df = pd.read_csv(fp, usecols = usecols)

    # Remove quotes from column names
    mapper = {quoted_col: _unquote_column_names(quoted_col) for quoted_col in usecols}
    df.rename(mapper=mapper, axis='columns', inplace=True)

    #TODO: unclear if NAs need to be removed like Aaron did in computed_elements()

    logger.debug("exiting pcr_patient_race_group()")
    return df
























def _quote_column_names(col: str | list[str] | None) -> str | list[str] | None:
    """Return the column name or names, but wrapped in single quotes."""
    error_message = 'col must be of type list or list[str]'
    if col is None:
        return None
    elif isinstance(col, str):
        return "'" + col + "'"
    elif isinstance(col, list):
        quoted_list = []
        for c in col:
            if not (isinstance(c, str)):
                raise ValueError(error_message)
            quoted_list.append("'" + c + "'")
        return quoted_list
    else:
        raise ValueError(error_message)


def _unquote_column_names(col: str | list[str]) -> str | list[str]:
    """Return the column name or names, but with the first and last characters stripped out."""
    error_message = 'col must be of type list or list[str]'
    if isinstance(col, str):
        return col[1:-1]
    elif isinstance(col, list):
        unquoted_list = []
        for c in col:
            if not (isinstance(c, str)):
                raise ValueError(error_message)
            unquoted_list.append(c[1:-1])
        return unquoted_list
    else:
        raise ValueError(error_message)


if __name__ == "__main__":
    main()
