import pandas as pd
from scipy.stats import chi2_contingency
from pathlib import Path


def main():
    data_fp = Path(__file__).parent.parent / 'data' / 'processed' / 'events_renamed.pickle' #.parent 
    df = pd.read_pickle(data_fp)

    # Remove CPR_Care_Provided_Prior_to_EMS_Arrival rows without an outcome variable
    df = df[df['CPR_Care_Provided_Prior_to_EMS_Arrival'].isin(['Yes', 'No'])]

    # Remove End_of_EMS_Cardiac_Arrest_Event rows other than Dead or Alive
    df = df[df['End_of_EMS_Cardiac_Arrest_Event'].isin(['Dead', 'Alive'])]

    # Remap Urbanicity to two categories
    mapping = {
        "U": "Urban/Suburban",
        "S": "Urban/Suburban",
        "R": "Rural/Wilderness",
        "W": "Rural/Wilderness"
    }
    df['Urbanicity'] = df['Urbanicity'].map(arg=mapping)
    df.rename(columns={"Urbanicity": "Urbanicity_2"}, inplace=True)

    contingency = pd.crosstab(df.Urbanicity_2, df.End_of_EMS_Cardiac_Arrest_Event)
    chi2 = chi2_contingency(observed=contingency, correction=False)

    result_fp = Path(__file__).parent.parent / 'reports' / 'chi-square.txt' #.parent
    with open(result_fp, mode='w') as f:
        print("Contingency table of urbanicity vs outcomes:", file=f)
        print(contingency, file=f)
        print("\n", file=f)
        print("Results of chi-square independence test between using the above contingency table:", file=f)
        print(chi2, file=f)


if __name__ == "__main__":
    main()
