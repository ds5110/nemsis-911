# Cardiac Analysis of NEMSIS EMS Dataset

## Overview
This project is an analysis of EMS data from the National Emergency Medical Services Information System (NEMSIS) with
the goal of finding predictors of cardiac arrest, possibly including rurality.

A complete proposal should wait until after a review of the data and a conversation with the stakeholders. Other data
sources may need to be included to measure exposure (i.e., cardiac arrests per *something*).

## Table of Contents
The project structure is based on [this one](https://drivendata.github.io/cookiecutter-data-science/). While we have
defined data directories for reproducibility purposes, the dataset itself is not stored in the repo. 

```
├── environment.yml            <- Conda environment file
├── Makefile                   <- Makefile that extracts processed data from original zip file
├── Makefile_overview.md       <- Overview of Makefile steps, challenges, and rationales
├── Plan.md                    <- Detailed project plan including milestones and timelines
├── Proposal.md                <- Project description, intended approach, and EDA support for feasibility
├── README.md                  <- You are here
├── Terms.md                   <- Mandatory disclosure required by the NEMSIS dataset Terms of Use
├── data
│   ├── csv                    <- Contains a version of Pub_PCRevents.txt converted to comma delimiters for easy parsing
│   ├── interim                <- The unzipped text files
│   ├── processed              <- The final, canonical data sets for modeling
│   ├── raw                    <- Place the original zipped dataset "ASCII 2022.zip" from NEMSIS here
│   └── repaired               <- A repaired zip file of the NEMSIS dataset
│
├── references                 <- Data dictionaries, manuals, data request instructions, other explanatory materials
│   └── NEMSISDataDictionary_v3.4.0.pdf  <- Data dictionary for columns in original dataset
│
├── reports                    <- Analysis such as HTML, PDF, LaTeX, etc
│   ├── chi-square.txt         <- Results of chi-square independence test between urbanicity and cardiac arrest survival
│   ├── ds_5500_capstone.pdf   <- Final presentation
│   └── NEMSIS_EDA.pdf         <- An exploratory data analysis presentation created halfway through this project
│
└── src                        <- Source code
    ├── __init.py__            <- Makes src a Python module
    │
    └── data                   <- Scripts to download data or generate data
        ├── analysis.py        <- Perform chi-square independence test on urbanicity vs cardiac arrest survival
        ├── make_dataset.py    <- Filter dataset to cardiac arrests
        └── rename_columns.py  <- Map important categorical variables
    
```

## Getting Started

### Prerequisites

Request a copy of the NEMSIS Public-Release Research Dataset for 2022 from NEMSIS in ASCII (pipe-delimited) format. You
can currently find the request form [here](https://nemsis.org/using-ems-data/request-research-data/). When you receive
the file, verify that it has the following characteristics:
  - filename: "ASCII 2022.zip"
  - size: 18,021,941,320 bytes
  - sha256 hash: 2fc87b18edf2e762be2d723c44413cb98064bcbc3e6a46468e3b42f25f521898

Use a computer with at least 300 GB of available storage to hold the dataset. This work was originally done on a
computer with 32 GB of RAM; less RAM may work but has not been tested.

You will need [make](https://www.gnu.org/software/make/) installed, along with other GNU utilities. On a Linux or Mac
OS, these are probably pre-installed. On Windows, you can get these working by installing the Windows Subsystem for
Linux (WSL), although that is out of scope for this document.

Install [miniconda](https://docs.conda.io/projects/miniconda) to create reproducible environments for Python
dependencies, and [git](https://git-scm.com/) for version control.

### Instructions

Clone this repository to your local PC using git. Use the environment.yml file to create a Conda environment with the
necessary dependencies.

Drop the zipped NEMSIS dataset into `data/raw/`.

In a terminal, navigate to your project folder and run `make` to extract the files.

A detailed overview of the makefile process can be found in the file `Makefile_overview.md`.

## Other Resources

### Data Dictionary

NEMSIS provides a data dictionary that is necessary to decode the column names and their values. One is included in this
repo, but it can also be found online
[here](https://nemsis.org/technical-resources/version-3/version-3-data-dictionaries/). Note that not all fields in the
data dictionary are present in the dataset.

### Case Definitions

NEMSIS defines over a dozen case definitions, which are medical events or conditions (such as "Opioid Overdose" or
"Seizure") along with structured descriptions of how to identify those events in the NEMSIS dataset. These case
definitions have not been included in this repo out of intellectual property concerns, but can be found online
[here](https://nemsis.org/case-definitions/). The case definition for cardiac arrest is used extensively in this project
to filter the entire dataset down to only the relevant records.

## Results Overview

The primary deliverable from this project is the reproducible data pipeline itself. However, a chi-square analysis was
performed to check the relationship between urbanicity and cardiac survivability.

Urbanicity was recorded as Urban, Suburban, Rural, or Wilderness; in this analysis I aggregated Urban/Suburban into one
group and Rural/Wilderness into another. 184K records were included for cardiac arrests with a recorded urbanicity and a
known survival outcome. The breakdown is shown in the table below.

    -------------------------------------------------
    | Urbanicity       | Alive  | Dead    | Total   |
    -------------------------------------------------
    | Urban/Suburban   | 31,797 | 135,368 | 167,165 |
    | Rural/Wilderness |  3,049 |  14,090 |  17,139 |
    -------------------------------------------------
    | Total            | 34,846 | 149,458 | 184,304 |
    -------------------------------------------------

The overall survival rate was 19%. A literature search showed past rates between 10% (for ambulance calls) and 25% (for
in-hospital alerts), meaning the 19% is in a reasonable range. The survival rates were 19.0% for urban/suburban areas
and 17.8% for rural/wilderness areas. While seemingly small, a chi-square test showed that these differences were large
enough to not be caused by random chance with a p-value less than 0.001. The results from
`PROJECTDIR/reports/chi-square.txt` are also shown below:

    Chi2ContingencyResult(statistic=15.376426110258624, pvalue=8.8080342785201e-05, dof=1, expected_freq=array([[  3240.43750543,  13898.56249457],
           [ 31605.56249457, 135559.43750543]]))

The initial proposal also called for an explicit model for cardiac survivability, but this was eventually scrapped. It
was not clear from the available columns that a useful model could be built for any audience using the provided data.
The data pipeline took enough time that only a limited amount of modeling time was available, and I ultimately did not
have the domain knowledge to identify useful modeling opportunities.