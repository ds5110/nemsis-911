import pandas as pd
from pathlib import Path


"""
This script reviews the filtered events data created by filter_primary_NEMSIS_cases.py, and does some
preliminary EDA, saving data to reports/preliminary_eda.txt, including the following for each column of the data;

- Column Name and Index
- Datatype
- Number & % of null values
- Number of Unique values

Example:
**Column at Index 11: 'EMSSystemResponseTimeMin'**
 - Datatype: float64
 - Number of Null Values: 0  |  Percent Null: 0.0%
 - Number of Unique Values: 1990
"""
def main():
    # get selected events
    data_fp = Path(__file__).parent.parent / 'data' / 'processed' / 'selected_events.pickle' 
    df = pd.read_pickle(data_fp)

    # get the columns, and total # of rows
    col_names = df.columns.tolist()
    n_rows = df.shape[0]

    # open a txt file to save info. about each column
    f = open("./reports/preliminary_eda.txt", "w")
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

if __name__ == "__main__":
    main()
