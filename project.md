# Project Name: 911

### Team: Ian Duggan, Tristan Jordan, Ben Darby

### Team Lead: Ian Duggan

## Story
>The National Emergency Medical Services Information System (NEMSIS) collects, stores and shares EMS data from across the U.S. The NEMSIS dataset will help many organizations assess EMS needs and performance, and support better strategic planning for the EMS systems of tomorrow. Data also helps benchmark performance, determine the effectiveness of clinical interventions, and facilitate cost-benefit analyses. The goal in this project is to help Dr. May -- a critical care physician at Maine Health -- investigate strategies for improving outcomes when cardiac-arrest victims receive care from first responders. For example, there's evidence of disparities in rural and urban scenarios.
>
>The NEMSIS dataset is complex, so work needs to be done to understand and interpret the data. Some well known facts need to be established first with the dataset. For example, in real world settings a very high percentage of patients receiving care should receive epinephrine. But in our previous analyses with the NEMSIS dataset this rate appeared to be much lower, suggesting that we had not fully filtered and cleaned the data.. Some of the features collected in the data may provide clues. For example, there is one field in the data called "eDisposition" that indicates that a patient is being transported for followup care. As multiple ambulances are dispatched to a call but only one takes the patient, the other ambulances may show up as records with mostly missing data - it is important that these records be excluded from the analysis. Likewise, patients that have passed will not receive epinephrine. Therefore, "eDisposition" should enter somehow into the analysis pipeline, during EDA and cleaning. This kind of EDA involving other features, missing fields, imputation strategies, etc. will reveal sensitivities that have implications for modeling.
>
>Continued work with NEMSIS will benefit two important resources: a recent publication in the peer-reviewed literature and a github repository developed to facilitate reproducible analysis. Peters et al. (2022) investigated urban/rural disparities across the country. And Aaron Fihn, a Roux Institute MSDS graduate, created a github repository in 2023 that has detailed instructions for extracting and analyzing the NEMSIS data. A logical first step is to assess reproducibility of results in the published study.

## Data

### NEMSIS.org is the original data source.

>Peters et al. (2022) "Differences in Out-of-Hospital Cardiac Arrest Management and Outcomes across Urban, Suburban, and Rural Settings", https://doi.org/10.1080/10903127.2021.2018076

>Aaron Fihn's github repo, https://github.com/ds5500/project-aaronfihn, has instructions for accessing, cleaning and analyzing the NEMSIS data from the original data source. This repo will be made available for project teams.

## Project Goals

>__Data Quality and EDA__<br>
    Assess and enhance the quality of the NEMSIS dataset through thorough cleaning and exploratory data analysis, focusing on identifying patterns and trends, particularly in the use of epinephrine for cardiac arrest cases.

>__Modeling and Feature Engineering__<br>
     Develop relevant features and predictive models to evaluate EMS interventions and their impact on patient outcomes, while investigating disparities in outcomes to determine the most influential factors affecting these disparities, especially in urban vs. rural contexts.

>__Reproducibility of Results__<br> 
    Assess the reproducibility of findings from previous studies using the NEMSIS dataset and ensure reproducibility of new findings discovered in the current project.

>__Collaboration__<br> 
    Collaborate with stakeholders to share insights and recommendations, aiming to improve EMS practices and inform strategic planning based on data-driven findings.
