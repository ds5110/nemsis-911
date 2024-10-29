### Project Repo for Duggan, Jordan, & Darby

***Delete prior to submit
Summary of changes made
created "create_sample_from_pickle.py" to create a csv sample file containing 2 fields only (urbanicity & ageinyear)<br>
saved the sample dataset to new dir "data_sample" in file "events_renamed_sample.csv"<br>
tested new data by copying original plots and modifying source.  Confirmed functionality and shape of samples is close to original data when plotted
saved the test plots in new subdir of figs name "fig_samples"
modified Makefile so that dir creation is a dependency and sample plots can be created from project root by running new command "make eda-charts_sample" 
copied existing plotting script to "eda_charts_sample.py", left originals unchanged
added new visual details to sample plot "patient-counts-by-urbanicity_Sample", this could be used  
tried to copy style of "age_histogram_by_urbanicity" in "age_histogram_by_urbanicity_sample" however legend is not showing detail, don't use this one   
End of Delete***

For information about our proposed project, see [Proposed Project Information](./project.md).

Referenced files from Aaron Fihn's initial project include:
- [Aaron Fihn's Readme](./README_Aaron-Fihn.md)
- [Makefile Information](./Makefile_overview.md)

## EDA
Links for our EDA can be found below:
- [Preliminary EDA on the Data Available](./preliminary_eda.md): includes the shape of the dataset, datatypes of each column, number of nulls in each column, and information from NEMSIS' data dictionary about what each column represents. 
- [Additional EDA with Charts](./EDA.md)

### EDA - Makefile Instructions
1) Due to file size concerns, all data has been gitignored. Follow [Aaron Fihn's instructions](./Makefile_overview.md) for downloading the data, then run his **make** command to prepare the *events_renamed.pickle* file
1) **make environment** can be run to create a conda environment named dsProjEnv. This is separate from Aaron's file due to older dependency issues, but his original environment.yml file was renamed to *environment_Aaron-Fihn.yml*. Our current file is named *environment.yml*
1) **conda activate dsProjEnv** to activate our conda environment
1) **make prelim-eda** can be run to generate the file *"reports/preliminary_eda.txt"*, which has information on the size of the data table, and columns available.
1) **make eda-charts** can be run to generate three plots in the *figs/* directory, and display them. These plots show an initial investigation into the patient age by urbanicity.
