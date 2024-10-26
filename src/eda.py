# Draft of EDA for Final Prioject
# DS 5110 
# Darby, Duggan, Jordan

import pandas as pd
import os

def main():
    # Define file path
    data_path = os.path.join('data', 'nemsis_data.csv') # NEED TO CONFIRM THIS ONCE DATA IS ACCESSABLE

    # Check if data file exists
    if not os.path.exists(data_path):
        print(f"Data file not found at: {data_path}")
        return

    # Load the data
    try:
        df = pd.read_csv(data_path)
        print("Dataset successfully loaded.")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    # Display basic information
    print("\nBasic Information:")
    print(df.info())

    # Display summary statistics
    print("\nSummary Statistics:")
    print(df.describe())

    # Display the first few rows
    print("\nFirst few rows of the dataset:")
    print(df.head())

    # Check for missing values
    print("\nMissing Values Count:")
    print(df.isnull().sum())

if __name__ == "__main__":
    main()
