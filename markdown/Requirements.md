# Requirements
Project Name: Cardiac Analysis of NEMSIS EMS Dataset

Primary Contact: Aaron Fihn

Stakeholders:
  - Dr. Qingchu Jin, Roux Institute
  - Dr. Christine Lary, Roux Institute
  - Dr. Teresa May, Maine Health

## Objectives
The primary goal of this project is to use the NEMSIS EMS dataset to identify predictors of cardiac arrest. The rurality
of the local area has been specified as a predictor of interest. The robustness of different imputation algorithms
should also be tested.

These objectives will be further fleshed out after reviewing the data and meeting with the stakeholders.

## Data
According to the [NEMSIS site](https://nemsis.org/using-ems-data/request-research-data/), the data for 2022 includes
"51,379,493 EMS activations submitted by 13,946 EMS agencies serving 54 states and territories during the 2022 calendar
year".

This data is publicly available by request from NEMSIS, though not downloadable over the internet. The original data
files are expected to be placed in the project subdirectory /data/raw. Instructions will be added for loading the data
once I've handled it myself.

## GitHub Pages
In addition to a final presentation, this repository should have a public-friendly website implemented in GitHub Pages
summarizing the research and findings. Depending on the findings, this could be as simple as a static HTML/CSS site, or
as complicated as an interactive web visualization using [Observable](https://observablehq.com/).