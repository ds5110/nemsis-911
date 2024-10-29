import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def main():
    data_fp = Path(__file__).parent.parent.parent / 'data_sample'  / 'events_renamed_sample.csv'
    df = pd.read_csv(data_fp)

    # replace null values for age in year, then convert to numeric (float for None types)
    df["ageinyear"] = df["ageinyear"].replace(". ", None)
    df["ageinyear"] = df["ageinyear"].astype(float)
    df['age_group'] = pd.cut(df['ageinyear'], 
                        bins=[0, 18, 35, 50, 65, 75, 100],  
                        labels=['0-18', '19-35', '36-50', '51-65', '65-75', '75+'])
    
    g = sns.histplot(data=df, x="ageinyear", binwidth=5)
    plt.title("Patient Age Distribution (Bin Width = 5 Years)")
    plt.savefig("figs/fig_samples/age-histogram_sample.png")
    plt.show()

    # hue-mapped histogram of age by urbanicity
    plt.figure(figsize=(7, 5))
    sns.histplot(data=df, x="ageinyear", hue="Urbanicity", multiple="dodge", element="step", stat="density",
                 common_norm=False, binwidth=5, alpha=0.2)
    plt.title("Patient Age Distribution by Urbanicity (Bin Width = 5 years)")
    plt.xlabel("Age (years)")
    plt.ylabel("Density")
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles, labels, title="Urbanicity")
    plt.savefig("figs/fig_samples/age-histogram-by-urbanicity_sample.png")
    plt.show()

    # bar plot with count of patient #s by urbanicity
    plt.figure(figsize=(7, 5))
    sns.countplot(x="Urbanicity", hue="age_group", data=df, order=["U", "S", "R", "W"], palette="viridis", 
                  hue_order=['0-18', '19-35', '36-50', '51-65', '65-75', '75+']) #age groups
    plt.xticks(range(4), ['Urban', 'Suburban', 'Rural', 'Wilderness'], rotation=0)
    plt.title("Count of Patients by Urbanicity")
    plt.xticks(rotation=0)
    plt.legend(title="Age Groups", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig("figs/fig_samples/patient-counts-by-urbanicity_sample.png", bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
