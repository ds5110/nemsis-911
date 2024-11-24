import pandas as pd
from pathlib import Path
import os


def main():

    cols_of_interest = [
        "ePatient_01",
        "ePatient_14",
        "eArrest_04",
        "eArrest_12",
        "eMedications_03",
        "eMedications_05",
        "eMedications_06", 
        "eAirway_01", 
        "eAirway_02", 
        "eAirway_03", 
        "eAirway_08", 
        "eAirway_10"
    ]

    # get all .txt files holding data, store in list
    text_file_path = "./reports/text_file_headers"
    temp_files = os.listdir(text_file_path)
    all_items = [item for item in temp_files if item != ".gitignore"]

    out_file = open(f"./reports/col_locations/cols_of_interest.txt", 'w')

    for item in all_items:

        # open file, get first line, then close
        in_file = open(f"./reports/text_file_headers/{item}", 'r')
        first_line = in_file.readline()
        in_file.close()

        # split into list of components on ascii delimiter, then remove \n and "'" chars
        first_line_list = first_line.split("~|~")
        first_line_list = [s.replace("\n", "") for s in first_line_list]
        first_line_list = [s.replace("'", "") for s in first_line_list]

        for col_name in first_line_list:
            if col_name in cols_of_interest:
                out_file.write(f"{col_name} - table location: {item.replace("top-10_", "")}\n")

    out_file.close()


if __name__ == "__main__":
    main()
