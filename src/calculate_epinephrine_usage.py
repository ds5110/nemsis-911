import pandas as pd
from pandasql import sqldf
from pathlib import Path
import sqlite3


def main():

    file_path = Path(__file__).parent.parent / 'data' / 'processed' / 'expanded_events.pickle' #.parent
    df = pd.read_pickle(file_path)

    print(df.shape)
    
    combined_ep = df['EpinephrineAdministered'].value_counts()
    tot = combined_ep[0] + combined_ep[1]
    tot_no_ep = combined_ep[0]
    tot_ep = combined_ep[1]
    
    #print(df['TotalDosesEpinephrine'].value_counts())

    rural_df = df[(df.Urbanicity == "R") | (df.Urbanicity == "W")]
    urban_df = df[(df.Urbanicity == "U") | (df.Urbanicity == "S")]

    rural_ep = rural_df['EpinephrineAdministered'].value_counts()
    rur_tot = rural_ep[0] + rural_ep[1]
    rur_no_ep = rural_ep[0]
    rur_ep = rural_ep[1]
    
    urban_ep = urban_df['EpinephrineAdministered'].value_counts()
    urb_tot = urban_ep[0] + urban_ep[1]
    urb_no_ep = urban_ep[0]
    urb_ep = urban_ep[1]
    

    tot_gender = df['ePatient_13'].value_counts()
    rur_gender = rural_df['ePatient_13'].value_counts()
    urb_gender = urban_df['ePatient_13'].value_counts()


    print(f"\nAll Incidents - {tot}")
    print(f"\tRural - {rur_tot} ({round(rur_tot / tot * 100 , 2)}%)")
    print(f"\tUrban / Suburban - {urb_tot} ({round(urb_tot / tot * 100, 2)}%)")

    print(f"\nAge in Years, mean (SD) - {round(df['ageinyear'].mean(), 2)} ({round(df['ageinyear'].std(), 2)})")
    print(f"\tRural - {round(rural_df['ageinyear'].mean(), 2)} ({round(rural_df['ageinyear'].std(), 2)})")
    print(f"\tUrban / Suburban - {round(urban_df['ageinyear'].mean(), 2)} ({round(urban_df['ageinyear'].std(), 2)})")

    print(f"\nMale - {tot_gender[9906003]} ({round(tot_gender[9906003] / (tot_gender[9906003] + tot_gender[9906001]) * 100, 2)}%)")
    print(f"\tRural - {rur_gender[9906003]} ({round(rur_gender[9906003] / (rur_gender[9906003] + rur_gender[9906001]) * 100, 2)}%)")
    print(f"\tUrban / Suburban - {urb_gender[9906003]} ({round(urb_gender[9906003] / (urb_gender[9906003] + urb_gender[9906001]) * 100, 2)}%)")

    print("\nEpinephrine Administered - Combined")
    print(f"{tot_ep} cases with epinephrine administered / {tot} total cases = {round(tot_ep / tot * 100, 2)}%")
    
    print("\nEpinephrine Administered - Rural ")
    print(f"{rur_ep} cases with epinephrine administered / {rur_tot} total cases = {round(rur_ep / rur_tot * 100, 2)}%")
    
    print("\nEpinephrine Administered - Urban / Suburban")
    print(f"{urb_ep} cases with epinephrine administered / {urb_tot} total cases = {round(urb_ep / urb_tot * 100, 2)}%")

    print()

if __name__ == "__main__":
    main()
