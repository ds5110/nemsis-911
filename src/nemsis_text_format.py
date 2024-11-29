import pandas as pd
from pathlib import Path
import os


def main():

    # get all .txt files holding data, store in list
    text_file_path = "./data/interim"
    temp_files = os.listdir(text_file_path)
    all_items = [item for item in temp_files if item != ".gitignore"]

    # iterate over all items to save a view with only the first 10 lines
    for item in all_items:

        out_file = open(f"./reports/text_file_headers/top-10_{item}", 'w')
        in_file = open(f"./data/interim/{item}", 'r')

        for i in range(10):
            temp_line = in_file.readline()
            out_file.write(temp_line)

        in_file.close()
        out_file.close()


if __name__ == "__main__":
    main()
