### Project Repo for Duggan, Jordan, & Darby

## System & Directory Requirements
Request a copy of the NEMSIS Public-Release Research Dataset for 2022 from NEMSIS in ASCII (pipe-delimited) format. You
can currently find the request form [here](https://nemsis.org/using-ems-data/request-research-data/). When you receive
the file, verify that it has the following characteristics:
  - filename: "ASCII 2022.zip"
  - size: 18,021,941,320 bytes
  - sha256 hash: 2fc87b18edf2e762be2d723c44413cb98064bcbc3e6a46468e3b42f25f521898
**Note:** if analysis is extended to a different year, file and data properties may vary.

Use a computer with at least 300 GB of available storage to hold the dataset. This work was done on a
computer with 32 GB of RAM; less RAM may work, but is not advised as some analysis files if written inefficiently (multiple pandas dfs),
may exceed 16 GB of RAM.

Discovery may also be used to leverage cloud computing if personal computers do not meet the requirements 
- [Discovery Access and Setup Instructions](./markdown/DiscoveryRC.md)

Utilities:
* [make](https://www.gnu.org/software/make/) installed, along with other GNU utilities. *(Windows may require WSL)*
* [miniconda](https://docs.conda.io/projects/miniconda) to create reproducible environments for Python dependencies
* [git](https://git-scm.com/) for version control.

## Makefile Instructions for Reproducibility
1) **make environment** - to create a conda environment named `project-duggani` with the required dependencies, from `environment.yml`.
1) **conda activate project-duggani** to activate the conda environment.
1) Drop the zipped NEMSIS dataset into `data/raw/`.
1) **make text_files** - to clean the ZIP file, and unpack all text files into `data/interim`.
1) **make setup_database** - to create the `data/NEMSIS_PUB.db` and populate it with data by running `create_NEMSIS_db.py` and `load_data_NEMSIS_db.py`
1) **make select_events** - to query the database and create the `data/processed/selected_events.pickle` file by applying the filters in `src/constants` to the NEMSIS data.
1) **make ./reports/preliminary_eda.txt** - to run text EDA on the columns in `data/processed/selected_events.pickle` 
1) **make eda_charts** - to run visual EDA and generate some plots.
1) **make calculate_epinephrine_usage** - to run another script, calculating some figures around epinephrine usage (an example of trying to replicate a part of the Peters et al. paper).

**Or, alternatively...**
1) **make** - running the `make` command will run the whole pipeline from start to finish: processing all data from the ZIP file into txt files, creating an sqlite database, filtering a prepared dataset using the filters defined in `constants`, and then running EDA & epinephrine analysis files. 

**Optional Makefile Commands**
* **make query** may be used to run the `src/query.py` file, which saves the top few results of a database query into the `reports/query_results` directory. *Note: change the query text and parameters within the python file for subsequent queries*. For more information on how this works, see [here](./markdown/Query_Exploration.md)
* **make clean** will remove all data text files, the NEMSIS_PUB.db object, and the generated items in `figs` and `reports` directories
* **make rebuild_database** will remove the NEMSIS_PUB.db file, and rebuild the database. This option exists in case you update the constant files, and want to rebuild the database without unpacking the text files again.
* **make reselect_events** will re-run the query in `src/filter_primary_NEMSIS_cases.py`, and update the `data/processed/selected_events.pickle`, for when the filter criteria in constants are updated and the data needs to be refreshed.

## Project Layout
```
├── environment.yml            <- yml file with dependencies for conda 
├── Makefile                   <- Makefile that extracts processed data from original zip file
├── README.md                  <- You are here
├── Terms.md                   <- Mandatory disclosure required by the NEMSIS dataset Terms of Use
├── markdown                   <- this directory contains additional markdown files for reference
│   ├── Proposal.md            <- Project description, intended approach, and EDA support for feasibility
│   ├── Plan.md                <- Project plan and timeline.
│   ├── etc...                 <- Additional markdown files include EDA resuls, detailed Makefile instructions, etc.
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
│   ├── viz                    <- Stores visualizations for our project presentation.
│   ├── epinephrine_usage.txt  <- Stores some summary statistics of the filtered data, specifically evaluating the % of cases with epinephrine administered.
│   └── preliminary_eda.txt    <- Stores summary data of each column in the prepared dataset, including # of nulls, unique values, etc.
│
└── src                                <- Source code
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

## Approach to Reproducibility - Filtering / Selecting Relevant Cardiac Arrest Cases
One of the challenges of working with this data set is selecting the relevant cardiac arrest cases for analysis. The NEMSIS data itself has > 51 million 
Patient Care Reports (PCRs), of which only a fraction are for cardiac arrest events. In their study of 2018 data, [Peters et al.](https://doi.org/10.1080/10903127.2021.2018076) filtered the data down to
approximately 65,000 records. NEMSIS's case definition of a cardiac arrest event includes the data fields (`eArrest_01`, `eArrest_02`, and various `eSituation` fields).
Within these fields, different codes must be used to appropriately select a cardiac arrest case. 

Furthermore, additional data fields, and/or combined features must be filtered for accurate analysis. Some of the criteria Peters et al. filtered the data on included:
* Pediatric patients < 18 years of age were excluded.
* Cases which were not a 911 scene response were excluded.
* Cases in which more than one EMS unit responded were excluded.
* Cases in which the unit did not transport or attempt resuscitation were excluded.
* Cases from other causes of traumatic injury besides a cardiac event were excluded.
* Cases with abnormal response time (> 60 minutes from initial dispatch to arrival on scene) were excluded.
* Cases with missing data required for the above decisions were also excluded.

Some of these features involve multiple NEMSIS fields, within which judgement calls have to be made about what codes for each field should be included or excluded. 
Documentation for these decisions was not present at the time we undertook this project, so we decided to develop a new framework for filtering and documenting what
criteria and features are used to select the relevant cardiac arrest cases. Our framework includes:
* A `constants` module within the `src` code directory, that outlines which fields were used to filter on, and what relevant codes for each field were included / excluded.
* A feature tracking spreadsheet **LINK TO BENS SPREADSHEET HERE**, with organizes the required features, what codes are needed for each, the confirmation status, and other details about how features are selected and confirmed to be accurate. 

Being methodical about selecting these features and implementing the filters is required, because the inclusion or exclusion of certain codes may add or remove thousands of PCRs, which can 
have a large impact on the results of any analysis. Our methodology resulted in a relevant case count of 95,000 PCRs. For the starting features and filters our group implemented:
* We adapted the same filters described by Peters et al. above.
* Additionally, we did not explore the imputation of null values. Rows that were missing data for features used to filter the data were excluded, rather than introducing a bias through unclear imputation. A question for further study is if imputing values should be done for any of the feature(s) defined.

See `src/constants/filter_criteria.py` for full documentation of how our filters were implemented. These feed into `src/filter_primary_NEMSIS_cases.py`, which produces a pickle file that can be easily read to a pandas dataframe: `data/processed/selected_events.pickle`. This pickle file is meant to store the relevant cardiac arrest cases for future analysis. Once additional features are confirmed, or if filters need to be changed, they may be updated in the constants module, and **make reselect_events** can be run to re-query the database and rebuild the `selected_events.pickle`, with the updated features & filter criteria applied.

## Review of Epinephrine Administered
After filtering down to the relevant PCR cases (see `constants/filter_criteria.py`), we calculated some figures from a table in the paper by Peters et al. 
Some of these figures are close percentage wise to the paper's published numbers. However, because the filter criteria described by the paper was vague, 
our main focus for the project became clearly defining a set of filtering constants that are used while setting up the database, that way future projects
can review our filter criteria, and modify or conduct additional analysis as needed.

```
All Incidents - 95735 
    	Rural - 5590 (5.84%)
    	Urban / Suburban - 90145 (94.16%)
    
Age in Years, mean (SD) - 67.16 (15.55)
    	Rural - 66.42 (14.39)
    	Urban / Suburban - 67.2 (15.62)
    
Male - 59823 (62.62%)
    	Rural - 3657 (65.63%)
    	Urban / Suburban - 56166 (62.44%)
    
Epinephrine Administered - Combined
    69505 cases with epinephrine administered / 95735 total cases = 72.6%
    
Epinephrine Administered - Rural 
    3918 cases with epinephrine administered / 5590 total cases = 70.09%
    
Epinephrine Administered - Urban / Suburban
    65587 cases with epinephrine administered / 90145 total cases = 72.76%
```

## EDA
Links for our EDA can be found below:
- [Preliminary EDA on the Data Available](./markdown/preliminary_eda.md): includes the shape of the dataset, datatypes of each column, number of nulls in each column, and information from NEMSIS' data dictionary about what each column represents. 
- [Additional EDA with Charts](./markdown/EDA.md)

For information about our proposed project, see [Proposed Project Information](./markdown/project.md).

## Additional Resources
- [Aaron Fihn's Readme](./markdown/Aaron-Fihn_README.md) - *for reference to Aaron's project*
- [Aaron Fihn's Makefile Information](./markdown/Aaron-Fihn_Makefile_overview.md) - *note: this project's Makefile was adapted from Aaron Fihn's, so not all steps apply, but it is a good reference for seeing how he dealt with the data challenges.*
- [Current Makefile Information](./markdown/Current_Makefile_overview.md) - this will outline the steps of our current Makefile, showing where we modified Aaron's approach
- [Project Proposal](./markdown/Proposal.md)
- [Project Plan](./markdown/Plan.md)
- [Project Story](./markdown/project.md)
- [Preliminary EDA](./markdown/preliminary_eda.md) - *includes information about the columns in the filtered dataset*
- [Visual EDA](./markdown/EDA.md) - *includes some visualizations of patient age and urbanicity in the filtered dataset*
- [Query Exploration](./markdown/Query_Exploration.md) - *shows some questions that were answered while querying the NEMSIS_PUB.db*

## References

* Fihn, A. (Accessed 2024, October 1). *project-aaronfihn*. [GitHub Repository]. *Northeastern University*. https://github.com/ds5500/project-aaronfihn

* Gregory A. Peters, Alexander J. Ordoobadi, Ashish R. Panchal & Rebecca
E. Cash (2023). *Differences in Out-of-Hospital Cardiac Arrest Management and Outcomes across Urban, Suburban, and Rural Settings*. Prehospital Emergency Care, 27:2, 162-169. https://doi.org/10.1080/10903127.2021.2018076

* [NEMSIS]. (Accessed 2024, October 1). *NEMSIS Data Dictionary. NHTSA v3.4.0. Build 200910. EMS Data Standard.* [Data Dictionary]. *NEMSIS*. https://nemsis.org/media/nemsis_v3/release-3.4.0/DataDictionary/PDFHTML/DEMEMS/index.html

* [NEMSIS]. (Accessed 2024, October 1). *NEMSIS V3 Case Definition. Cardiac Arrest* [Definition of Cardiac Arrest Events]. *NEMSIS*. https://nemsis.org/media/nemsis_v3/master/CaseDefinitions/CardiacArrest.pdf
