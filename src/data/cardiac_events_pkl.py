import pandas as pd
import matplotlib.pyplot as plt
import os
from cardiac_events_w_filter import calc_urbanicity

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
db_path = os.path.join(project_root, "data", "interim", "filtered_cardiac_events_df.pkl")
filtered_df = pd.read_pickle(db_path)
print(filtered_df.head())
print(filtered_df.shape)
# table_data = {
#     'Characteristic': ['Total Included'],
#     'All Incidents': [len(filtered_df)], 
#     'Rural': [filtered_df['urbanicity'].isin(['rural', 'wilderness']).sum()],
#     'Urban/Suburban': [filtered_df['urbanicity'].isin(['suburban', 'urban'].sum())],
#     'P-Value': [] # You'll need to calculate p-values separately 
#     }

# # Create the plot
# fig, ax = plt.subplots(figsize=(10, 4))
# ax.axis('off')

# # Create table
# table = ax.table(cellText=df.values, 
#                   colLabels=df.columns, 
#                   cellLoc = 'center',
#                   loc='center')
# table.auto_set_font_size(False)
# table.set_fontsize(12)
# table.scale(1.2, 1.2)


# plt.title('Table 1. Characteristics of EMS-treated OHCA incidents in rural versus urban/suburban prehospital settings. \nP-value calculated using chi-square test, unless otherwise noted.', fontsize=14)
# plt.savefig('../../data/interim/OHCA_characteristics_table.png', bbox_inches='tight') 
# plt.show() 

