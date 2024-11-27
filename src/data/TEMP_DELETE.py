import pandas as pd
from pandasql import sqldf
from pathlib import Path
import sqlite3


def main():

    file_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'expanded_events.pickle'
    df = pd.read_pickle(file_path)

    print(df.shape)
    print(df['EpinephrineAdministered'].value_counts())
    print(df['TotalDosesEpinephrine'].value_counts())


if __name__ == "__main__":
    main()
