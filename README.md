### Project Repo for Duggan, Jordan, & Darby

## System & Directory Requirements

## Makefile Instructions for Reproducibility
1) **make environment** - to create a conda environment named `project-duggani` with the required dependencies, from `environment.yml`.
1) **conda activate project-duggani** to activate the conda environment.
1) **make** - running the `make` command will process all data from the ZIP file into txt files, create an sqlite database, filter a prepared dataset using the filters defined in `constants`, and then run EDA & epinephrine analysis files. 

**Optional Makefile Commands**
* **make query** may be used to run the `src/query.py` file, which saves the top few results of a database query into the `reports/query_results` directory. *Note: change the query text and parameters within the python file for subsequent queries*
* **make clean** will remove all data text files, the NEMSIS_PUB.db object, and the generated items in `figs` and `reports` directories

## Project Layout
```
├── environment.yml            <- Conda environment file
├── Makefile                   <- Makefile that extracts processed data from original zip file
├── Plan.md                    <- Detailed project plan including milestones and timelines
├── Proposal.md                <- Project description, intended approach, and EDA support for feasibility
├── README.md                  <- You are here
├── Terms.md                   <- Mandatory disclosure required by the NEMSIS dataset Terms of Use
├── data
│   ├── csv                    <- A relic from Aaron Fihn's project, may be used to store csv files for easier parsing, if desired.
│   ├── interim                <- The unzipped text files
│   ├── processed              <- Stores a copy of the final, filtered dataset for analysis and modeling, selected_events.pickle
│   ├── raw                    <- Place the original zipped dataset "ASCII 2022.zip" from NEMSIS here
│   └── repaired               <- A repaired zip file of the NEMSIS dataset
│
├── figs                       <- Includes png files for plots created in the EDA phase.
├── references                 <- Data dictionaries, manuals, data request instructions, other explanatory materials
│   └── NEMSISDataDictionary_v3.4.0.pdf  <- Data dictionary for columns in original dataset
│
├── reports                    <- Analysis such as HTML, PDF, LaTeX, txt, etc
│   ├── Aaron_Fihn             <- Includes reports from Aaron Fihn's project, kept in for reference.
│   ├── col_locations          <- Stores the table names of desired columns searched for by src/nemsis_find_cols.py
│   ├── query_results          <- Stores the top few rows output by ad hoc queries run with src/query.py
│   ├── text_file_headers      <- Stores the top 10 rows of each text file in the NEMSIS data, for a quick view at what each file looks like. 
│   ├── epinephrine_usage.txt  <- Stores some summary statistics of the filtered data, specifically evaluating the % of cases with epinephrine administered.
│   └── preliminary_eda.txt    <- Stores summary data of each column in the prepared dataset, including # of nulls, unique values, etc.
│
└── src                        <- Source code
    ├── calculate_epinephrine_usage.py <- This script calculates summary statistics around epinephrine usage and urbanicity, to compare to the Peters et al. paper.
    ├── column_info.py                 <- For preliminary EDA, reports on column information in the filtered dataset, e.g., num nulls, unique vals, etc.
    ├── create_NEMSIS_db.py            <- Creates the NEMSIS_PUB.db sqlite database object
    ├── eda_charts.py                  <- Conducts EDA and saves png plots to figs directory. 
    ├── filter_Primary_NEMSIS_cases.py <- Applies all filters in constants to save a pickle file with the selected PCR events. 
    ├── load_data_NEMSIS_db.py         <- Reads text files to load data into the NEMSIS_PUB.db database
    ├── nemsis_find_cols.py            <- Searches header text files to find columns of interest, if there are columns for which we do not know the source table. 
    ├── nemsis_text_format.py          <- Reads all text files to save top 10 rows of each to reports/text_file_headers directory
    ├── query.py                       <- Script for ad hoc querying of NEMSIS_PUB.db database, which saves output headers to reports/query_results directory
    │
    └── constants                      <- Constant values for creating database, and filter criteria for selected PCR events. 
        ├── __init.py__                <- Makes constants a Python module that may be imported by other scripts
        ├── file_column_mapping.py     <- Defines the column mapping for the primary tables of interest that will be added to NEMSIS_PUB.db
        ├── filter_criteria.py         <- Defines the filter criteria to be used to select the curated dataset of relevant PCRs
        ├── paths.py                   <- Defines a couple of path variables that are called multiple times
        └── table_definitions.py       <- Includes SQL statements that are declared while constructing NEMSIS_PUB.db
    
```


## EDA
Links for our EDA can be found below:
- [Preliminary EDA on the Data Available](./markdown/preliminary_eda.md): includes the shape of the dataset, datatypes of each column, number of nulls in each column, and information from NEMSIS' data dictionary about what each column represents. 
- [Additional EDA with Charts](./markdown/EDA.md)

For information about our proposed project, see [Proposed Project Information](./project.md).


## References
Referenced files from Aaron Fihn's initial project include:
- [Aaron Fihn's Readme](./markdown/README_Aaron-Fihn.md)
- [Makefile Information](./markdown/Makefile_overview.md)





**Note Re: Data**:
* For easier replication of our initial EDA by the TA's, we have a small CSV file with a subset of the data in *data_sample/events_renamed_sample.csv*
* *Due to file size concerns, all other data has been gitignored. If you want to work with the full dataset, follow [Aaron Fihn's instructions](./markdown/Makefile_overview.md) for downloading the data, then run his **make** command to prepare the events_renamed.pickle file*

