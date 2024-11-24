import pandas as pd
from pathlib import Path

def main():
    # read file from Aaron's project
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events_renamed.pickle'
    df = pd.read_pickle(data_fp)

    #df.drop_duplicates()


    df['ageinyear'] = df['ageinyear'].replace('. ', None)
    df['ageinyear'] = df['ageinyear'].astype(float)
   
    df = df[df.ageinyear >= 18] # exclude pediatric cases


    print("N_Cols:", len(df.columns.tolist()))
    print("N_Rows:",  df.shape[0])


    df = df[df.eScene_01 == 9923003] # keep only those units first on scene


    print("N_Cols:", len(df.columns.tolist()))
    print("N_Rows:",  df.shape[0])

    #print(df['eScene_01'].head())
    print(df['ageinyear'].isna().sum())
    print(df['eScene_01'].isna().sum())



if __name__ == "__main__":
    main()
