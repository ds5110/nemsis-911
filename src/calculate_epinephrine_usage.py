import pandas as pd
from pandasql import sqldf
from pathlib import Path
import sqlite3


"""
This script reviews filtered PCR events (see constants/filter_criteria.py), to calculate epinephrine
administered figures for 2022. Filter criteria and methodology are inspired by the Peters et al paper. 
"""
def main():
    # load the filtered events pickle created by filter_primary_NEMSIS_cases.py, store as pandas df
    file_path = Path(__file__).parent.parent / 'data' / 'processed' / 'selected_events.pickle' 
    df = pd.read_pickle(file_path)

    # get counts by class of EpinephrineAdministered
    combined_ep = df['EpinephrineAdministered'].value_counts()
    tot = combined_ep[0] + combined_ep[1]
    tot_no_ep = combined_ep[0]
    tot_ep = combined_ep[1]
    
    # split dataframe into rural and urban subsets for figures by urbanicity
    rural_df = df[(df.Urbanicity == "Rural") | (df.Urbanicity == "Wilderness")]
    urban_df = df[(df.Urbanicity == "Urban") | (df.Urbanicity == "Suburban")]

    # calculate figures for epinephrine by urbanicity
    rural_ep = rural_df['EpinephrineAdministered'].value_counts()
    rur_tot = rural_ep[0] + rural_ep[1]
    rur_no_ep = rural_ep[0]
    rur_ep = rural_ep[1]
    
    urban_ep = urban_df['EpinephrineAdministered'].value_counts()
    urb_tot = urban_ep[0] + urban_ep[1]
    urb_no_ep = urban_ep[0]
    urb_ep = urban_ep[1]
    
    # get patient count by gender across urbanicity
    tot_gender = df['ePatient_13'].value_counts()
    rur_gender = rural_df['ePatient_13'].value_counts()
    urb_gender = urban_df['ePatient_13'].value_counts()

    # format string with summary data
    report_message = f"""\nAll Incidents - {tot} 
    \tRural - {rur_tot} ({round(rur_tot / tot * 100 , 2)}%)
    \tUrban / Suburban - {urb_tot} ({round(urb_tot / tot * 100, 2)}%)
    \nAge in Years, mean (SD) - {round(df['ageinyear'].mean(), 2)} ({round(df['ageinyear'].std(), 2)})
    \tRural - {round(rural_df['ageinyear'].mean(), 2)} ({round(rural_df['ageinyear'].std(), 2)})
    \tUrban / Suburban - {round(urban_df['ageinyear'].mean(), 2)} ({round(urban_df['ageinyear'].std(), 2)})
    \nMale - {tot_gender['9906003']} ({round(tot_gender['9906003'] / (tot_gender['9906003'] + tot_gender['9906001']) * 100, 2)}%)
    \tRural - {rur_gender['9906003']} ({round(rur_gender['9906003'] / (rur_gender['9906003'] + rur_gender['9906001']) * 100, 2)}%)
    \tUrban / Suburban - {urb_gender['9906003']} ({round(urb_gender['9906003'] / (urb_gender['9906003'] + urb_gender['9906001']) * 100, 2)}%)
    \nEpinephrine Administered - Combined
    {tot_ep} cases with epinephrine administered / {tot} total cases = {round(tot_ep / tot * 100, 2)}%
    \nEpinephrine Administered - Rural 
    {rur_ep} cases with epinephrine administered / {rur_tot} total cases = {round(rur_ep / rur_tot * 100, 2)}%
    \nEpinephrine Administered - Urban / Suburban
    {urb_ep} cases with epinephrine administered / {urb_tot} total cases = {round(urb_ep / urb_tot * 100, 2)}%
    """
    
    # print message and save to reports folder
    print(report_message) 
    out_file = open(f"./reports/epinephrine_usage.txt", 'w')
    out_file.write(report_message)
    out_file.close()

if __name__ == "__main__":
    main()
