import pandas as pd
from pathlib import Path


def main():
    # read file from Aaron's project
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events_renamed.pickle'
    df = pd.read_pickle(data_fp)

    # get the columns, and total # of rows
    col_names = df.columns.tolist()
    n_rows = df.shape[0]

    # print out some info. about each column
    for i in range(len(col_names)):
        col_name = col_names[i]
        num_nulls = n_rows - (df[df.columns[i]].count()) 
        print(f"Column at Index {i}: '{col_name}'\n\tDatatype: {df[col_name].dtype}")
        print(f"\tNumber of Null Values: {num_nulls}\n\tPercent Null: {round(num_nulls / n_rows * 100, 2)}%\n")




if __name__ == "__main__":
    main()