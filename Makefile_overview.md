# Makefile Overview

This file contains a description of the steps performed by the Makefile, as well as the rationale behind them. The
actual file is simple titled "Makefile".

As a prerequisite, the NEMSIS file "ASCII 2022.zip" must be placed in inside `PROJECTDIR/data/raw/` before running
make.

## Makefile Steps

### Step 0 (Optional): Cleaning Prior Runs

Data generated in prior runs can be deleted using the following command in the terminal:

`make clean`

This will delete all generated data files in the subdirectories inside `PROJECTDIR/data/raw/` using the "find" utility,
while leaving the original ZIP file alone. This is rarely required; even if make is interrupted halfway, it should pick
up where it left off when run again.

This executes the following code block from the Makefile:

    clean:
    	find ./data/processed/ -type f -not -name '.gitignore' -delete
    	find ./data/csv/ -type f -not -name '.gitignore' -delete
    	find ./data/interim/ -type f -not -name '.gitignore' -delete
    	find ./data/repaired/ -type f -not -name '.gitignore' -delete

### Step 1: Repairing the Corrupted ZIP

This step and all later steps are executed by running the following command in the terminal:

`make`

This first copies the NEMSIS-provided ZIP to `PROJECTDIR/data/repaired/ASCII 2022_repaired.zip` and repairs it using the
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

### Step 3: Filter Key Table to CSVs

This step copies a couple important files to `PROJECTDIR/data/csv/`, replaces the delimiter `~|~` with a comma, and
changes the file extension from txt to csv.

Why bother with this when pandas lets you specify the delimiter during data imports? This is because of a
[bug](https://github.com/pandas-dev/pandas/issues/55677) related to the python parsing engine used by pandas. This is a
secondary parsing engine, but the primary parsing engine can only handle comma delimiters. The bug caused data imports
to fail; this conversion allowed me to bypass that problem. (The bug I reported was verified and eventually fixed by
pandas contributors, but not in time for this project.)

This step is performed in the following code block, which uses sed to replace the delimiters and write a new file:

    ./data/csv/Pub_PCRevents.csv: $(unzipped_csvs)
    	sed 's/~|~/,/g' ./data/interim/Pub_PCRevents.txt > ./data/csv/Pub_PCRevents.csv
    
    ./data/csv/ComputedElements.csv: $(unzipped_csvs)
    	sed 's/~|~/,/g' ./data/interim/ComputedElements.txt > ./data/csv/ComputedElements.csv

### Step 4: Filter Dataset to Cardiac Arrests

The entire dataset contains 51MM records, which is too many to hold in-memory. This step filters the dataset down to
only the cardiac arrest records, identified using the
[NEMSIS cardiac arrest case definition](https://nemsis.org/case-definitions/). This is performed by the code block
below, which simply runs the python script `PROJECTDIR/src/data/make_dataset.py`:

    # Convert the CSV to a pickle of a pandas dataframe
    ./data/processed/events.pickle: ./data/csv/Pub_PCRevents.csv ./data/csv/ComputedElements.csv
    	python ./src/data/make_dataset.py

This script took a significant amount of development time. Pandas is not optimized for working with very large datasets.
The first challenge is that some files were too large to be held in memory in their entirety. I handled this by making
multiple passes through the data. First I read all rows, saving only the fields necessary to determine whether the
record was for a cardiac arrest. This reduced the dataset from 51MM records to 291K. Then I made another pass, saving
all columns from those eligible rows.

But simply reading the dataset took some trial-and-error. Pandas offers a chunksize parameter to the
[read_csv](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) method that allows the user
to grab only a specified number of rows at a time; it also has a skiprows parameter that accepts a list of line numbers
to skip, which would be needed for the second pass. Unfortunately, pandas checks whether each of the 51MM rows is
present in the skiprows list by performing a linear search. Because most records are not cardiac arrest records, the
skiprows list *also* contains approximately 51MM entries. This means the total number of comparisons necessary to check
for skipped rows was proportional to 51MM^2, causing the process to crash. I tried to resolve this by changing the
skiprows parameter to a callable that used a hashmap for lookups, but this led to the discovery of the
[bug](https://github.com/pandas-dev/pandas/issues/55677) mentioned earlier. I was only able to resolve it by adding step
3 to the build process, which allowed me to sidestep the bug by using pandas' c parsing engine instead of its python
parsing engine.

The results are saved as `PROJECTDIR/data/processed/events.pickle`, and can be read as a pandas dataframe. This is the
file that would likely be of most use for future research.

### Step 5: Rename Columns

To avoid awkward column names like "eArrest_05" for the urbanicity/cardiac survivability analysis, I mapped a few
relevant columns and their values to have English-readable names. This step runs the python script
`PROJECTDIR/src/data/rename_columns.py` using the following code block:

    ./data/processed/events_renamed.pickle: ./data/processed/events.pickle
    	python ./src/data/rename_columns.py

### Step 6: Perform Chi-Square Test

While step 4 limited the dataset to only cardiac arrests, this project was interested in the relationship
between urbanicity and cardiac survival. To explore this, I had to filter the dataset to remove records where either of
those variables were blank and then run a chi-square analysis. This step runs the script
`PROJECTDIR/src/data/analysis.py` and saves the result to `PROJECTDIR/reports/chi-square.txt` using the following code
block:

    build: ./reports/chi-square.txt
    
    ./reports/chi-square.txt: ./data/processed/events_renamed.pickle
    	python ./src/data/analysis.py

