import pandas as pd
import numpy as np
from pathlib import Path

pickle_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'events_renamed.pickle'

# load df / create sample file
df = pd.read_pickle(pickle_path)
df.loc[df["ageinyear"].isna(), "ageinyear"] = ". "
df.to_csv(Path(__file__).parent.parent.parent / 'data_sample' / 'events_renamed_sample.csv', index=False)

# change sample size or fields here
n_samples = 10000
df_sample = df[['ageinyear', 'Urbanicity']].sample(n=n_samples, random_state=17)

# save it
output_path = Path(__file__).parent.parent.parent / 'data_sample' / 'events_renamed_sample.csv'
df_sample.to_csv(output_path, index=False)

print("Sample data preview:")
print(df.head(10))

print("\nValue counts for Urbanicity:")
print(df["Urbanicity"].value_counts())

print("\nAge statistics (excluding null values):")
print(df[df["ageinyear"] != ". "]["ageinyear"].describe())
