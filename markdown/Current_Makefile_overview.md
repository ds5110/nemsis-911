# Makefile Overview

This file contains a description of the steps performed by the `Makefile`.
As a prerequisite, the NEMSIS file "ASCII 2022.zip" must be placed in inside `./data/raw/` before running make.

## Makefile Steps

### Step 0 (Optional): Cleaning Prior Runs

Data generated in prior runs can be deleted using the following command in the terminal:

`make clean`

This will delete all generated data files in the subdirectories inside `./data/`, the `NEMSIS_PUB.db` file, and additional files inside the `figs` and `reports` directories. It will leave the original ZIP file alone. This executes the following code block from the Makefile:

    clean:
    	find ./data/processed/ -type f -not -name '.gitignore' -delete
        find ./data/csv/ -type f -not -name '.gitignore' -delete
        find ./data/interim/ -type f -not -name '.gitignore' -delete
        find ./data/repaired/ -type f -not -name '.gitignore' -delete
        rm -f data/NEMSIS_PUB.db
        rm -f figs/*
        rm -f reports/col_locations/cols_of_interest.txt 
        rm -f reports/preliminary_eda.txt
        rm -f reports/text_file_headers/*
        rm -f reports/epinephrine_usage.txt

### Step 1: Repairing the Corrupted ZIP

This step and all later steps are executed by running the following command in the terminal:

`make`

This first copies the NEMSIS-provided ZIP to `./data/repaired/ASCII 2022_repaired.zip` and repairs it using the
GNU zip utility. Trying to unzip the original ZIP fails and warns that the file is corrupted; this step uses the -FF
flag to repair it and the -f flag to skip the copy process if the file has already been repaired successfully.

This step corresponds with the following code block from the Makefile:

    # The zip file from NEMSIS is corrupted and must be repaired before unzipping
    ./data/repaired/ASCII\ 2022_repaired.zip: ./data/raw/ASCII\ 2022.zip
    	zip -FFfz "./data/raw/ASCII 2022.zip" --out "./data/repaired/ASCII 2022_repaired.zip"

### Step 2: Unzip

This step unzips the repaired ZIP and places the resulting 42 text files in `PROJECTDIR/data/interim/`. These
collectively take up 175 GB. Each file is in a tabular text format using an odd tilde-pipe-tilde delimiter.

In the Makefile, the output files are first defined using a variable. A snippet is shown below:

    unzipped_csvs = ./data/interim/ComputedElements.txt \
                    ./data/interim/EINJURY_01REF.txt \
                    ./data/interim/EPROCEDURES_03REF.txt \
                    # etc

The actual unzip instructions occur in the code block below:

    $(unzipped_csvs) &: ./data/repaired/ASCII\ 2022_repaired.zip
    	unzip -jo "./data/repaired/ASCII 2022_repaired.zip" -d ./data/interim
    	touch -c ./data/interim/*

The separator "&:" causes this command to be run only once, instead of once for each output file. The unzip utility uses
the -j flag to prevent making another nested subdirectory, the -o flag to overwrite any existing files without
complaint, and the -d flag to specify the output directory. The touch utility simply updates the timestamps of the
unzipped files to the current time instead of the time they were originally created; this is necessary because make
uses timestamp comparisons to determine which steps of the build process should be performed.

### Step 3: Create Databse, and Write Key Text Files to NEMSIS_PUB.db

This step copies a couple important text files from `./data/interim/`, and writes them into the `NEMSIS_PUB.db` file. See `src/constants/file_column_mapping.py`, `src/constants/table_definitions.py`, `src/create_NEMSIS_db.py`, and `src/load_data_NEMSIS_db.py` to see how this is done. 

If more tables are ever added to the constant files, and you wish to update the `NEMSIS_PUB.db` file, you can run the command `make rebuild_databse`, which will execute the following code:

rebuild_database:
	rm -f data/NEMSIS_PUB.db
	python ./src/create_NEMSIS_db.py
	python ./src/load_data_NEMSIS_db.py

### Step 4: Filter Dataset to Relevant Cardiac Arrests

This step queries the data in `NEMSIS_PUB.db`, filtering down to the relevant cases as selected using `src/constants/filter_criteria.py`. 

The results are saved as `./data/processed/selected_events.pickle`, which can be read as a pandas dataframe. If additional data fields are desired for future research, the command `make reselect_events` can be run, which executes the following code:

reselect_events:
	python ./src/filter_primary_NEMSIS_cases.py

### Step 5: Subsequent Analysis

After the `selected_events.pickle` file is prepared, additional scripts are run for analysis, including EDA on the data in this file, and a review of epinephrine usage. The code blocks that are run include:

./reports/preliminary_eda.txt: ./data/processed/selected_events.pickle
	python ./src/column_info.py

eda_charts: ./data/processed/selected_events.pickle
	python ./src/eda_charts.py

calculate_epinephrine_usage: ./data/processed/selected_events.pickle
	python ./src/calculate_epinephrine_usage.py

find_cols: col_headers
	python ./src/nemsis_find_cols.py

col_headers: ./data/repaired/ASCII\ 2022_repaired.zip
	python ./src/nemsis_text_format.py