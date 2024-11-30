import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


"""
This script does some EDA with plotting for patient age and urbanicity of the filtered cardiac events.
See figs directory for saved plots
"""
def main():
    # read filtered events from database query
    data_fp = Path(__file__).parent.parent / 'data' / 'processed' / 'selected_events.pickle' 
    df = pd.read_pickle(data_fp)

    # create bins for age groups
    df['age_group'] = pd.cut(df['ageinyear'], 
                        bins=[18, 35, 50, 65, 75, 100],  
                        labels=['18-35', '36-50', '51-65', '65-75', '75+'])
    
    # age distribution across all patients
    g = sns.histplot(data = df, x = "ageinyear", binwidth = 5)
    plt.title("Patient Age Distribution (Bin Width = 5 Years)")
    plt.savefig("figs/age-histogram.png")
    plt.show()

    # hue-mapped histogram of age by urbanicity
    sns.histplot(data = df, x = "ageinyear", hue = "Urbanicity", element = "step", stat = "density", common_norm = False, binwidth = 5)
    plt.title("Patient Age Distribution by Urbanicity (Bin Width = 5 years)")
    plt.savefig("figs/age-histogram-by-urbanicity.png")
    plt.show()

    # bar plot with count of patient #s by urbanicity
    sns.countplot(x = df['Urbanicity'], order = ['Urban', 'Suburban', 'Rural', 'Wilderness'])
    plt.title("Count of Patients by Urbanicity")
    plt.savefig("figs/patient-counts-by-urbanicity.png")
    plt.show()

    # bar plot with count of patient #s by urbanicity and age
    plt.figure(figsize=(7, 5))
    sns.countplot(x="Urbanicity", hue="age_group", data=df, order=["Urban", "Suburban", "Rural", "Wilderness"], palette="viridis", 
                  hue_order=['18-35', '36-50', '51-65', '65-75', '75+']) #age groups
    plt.xticks(range(4), ['Urban', 'Suburban', 'Rural', 'Wilderness'], rotation=0)
    plt.title("Count of Patients by Urbanicity and Age")
    plt.xticks(rotation=0)
    plt.legend(title="Age Groups", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("figs/patient-counts-by-urbanicity-age.png", bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()
