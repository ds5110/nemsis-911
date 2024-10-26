### Project Repo for Duggan, Jordan, & Darby

For information about our proposed project, see [Proposed Project Information](./project.md).

Referenced files from Aaron Fihn's initial project include:
- [Aaron Fihn's Readme](./README_Aaron-Fihn.md)
- [Makefile Information](./Makefile_overview.md)

## EDA
Links for our EDA can be found below:
- [Preliminary EDA on the Data Available](./preliminary_eda.md): includes the shape of the dataset, datatypes of each column, number of nulls in each column, and information from NEMSIS' data dictionary about what each column represents. 
- [Additional EDA with Charts](./EDA.md)

### EDA - Makefile Instructions
1) Due to file size concerns, all data has been gitignored. Follow Aaron Fihn's instructions for downloading the data, then run his **make** command to prepare the *events_renamed.pickle* file
1) **make environment** can be run to create a conda environment named dsProjEnv. This is separate from Aaron's file due to older dependency issues, but his original environment.yml file was renamed to *environment_Aaron-Fihn.yml*. Our current file is named *environment.yml*
1) **conda activate dsProjEnv** to activate our conda environment
1) **make prelim-eda** can be run to generate the file *"reports/preliminary_eda.txt"*, which has information on the size of the data table, and columns available.
1) **make eda-charts** can be run to generate three plots in the *figs/* directory, and display them. These plots show an initial investigation into the patient age by urbanicity.