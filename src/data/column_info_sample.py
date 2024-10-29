import pandas as pd
from pathlib import Path

def main():
    # read temp CSV file
    data_fp = Path(__file__).parent.parent.parent / 'data_sample'  / 'events_renamed_sample.csv'
    df = pd.read_csv(data_fp)

    # get the columns, and total # of rows
    col_names = df.columns.tolist()
    n_rows = df.shape[0]

    # open a txt file to save info. about each column
    f = open("./reports/preliminary_eda_sample.txt", "w")
    f.write("Table: events_renamed.pickle\n")
    f.write(f"\tNumber of Rows: {n_rows}\n")
    f.write(f"\tNumber of Columns: {len(col_names)}\n\n")

    # print out some info. about each column
    for i in range(len(col_names)):
        col_name = col_names[i]
        num_nulls = n_rows - (df[df.columns[i]].count()) 
        num_unique = df[df.columns[i]].nunique()

        print(f"Column at Index {i}: '{col_name}'\n\tDatatype: {df[col_name].dtype}")
        print(f"\tNumber of Null Values: {num_nulls}  |  Percent Null: {round(num_nulls / n_rows * 100, 2)}%")
        print(f"\tNumber of Unique Values: {num_unique}\n")
        
        f.write(f"**Column at Index {i}: '{col_name}'**\n - Datatype: {df[col_name].dtype}")
        f.write(f"\n - Number of Null Values: {num_nulls}  |  Percent Null: {round(num_nulls / n_rows * 100, 2)}%")
        f.write(f"\n - Number of Unique Values: {num_unique}\n\n")

    f.close() # make sure to close the text file

    # print(df['ageinyear'].head(5)) # may be uncommented to see some example data from a col


if __name__ == "__main__":
    main()