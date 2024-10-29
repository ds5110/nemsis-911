import pandas as pd
from pathlib import Path

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def main():
    # read file from Aaron's project (all available data)
    data_fp = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events_renamed.pickle'
    df = pd.read_pickle(data_fp)

    # replace null values for age in year, then convert to numeric (float for None types)
    df['ageinyear'] = df['ageinyear'].replace('. ', None)
    df['ageinyear'] = df['ageinyear'].astype(float)

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
    sns.countplot(x = df['Urbanicity'], order = ['U', 'S', 'R', 'W'])
    plt.title("Count of Patients by Urbanicity")
    plt.savefig("figs/patient-counts-by-urbanicity.png")
    plt.show()

if __name__ == "__main__":
    main()