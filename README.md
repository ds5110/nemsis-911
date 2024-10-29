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
1) **make environment** can be run to create a conda environment named `project-duggani`. This is separate from Aaron's file due to older dependency issues, but his original environment.yml file was renamed to *environment_Aaron-Fihn.yml*. Our current file is named *environment.yml*
1) **conda activate project-duggani** to activate our conda environment
1) **make prelim-eda_sample** can be run to generate the file *"reports/preliminary_eda_sample.txt"*, which has information on the size of the data table, and columns available. *Note: see reports/preliminary_eda.txt for the file that was generated from the full dataset*
1) **make eda-charts_sample** can be run to make the directory *figs/fig_samples* and generate three plots. These plots show an initial investigation into the patient age by urbanicity. *Note: see the figs/ directory for the charts that were generated from the full dataset*

**Note Re: Data**:
* For easier replication of our initial EDA by the TA's, we have a small CSV file with a subset of the data in *data_sample/events_renamed_sample.csv*
* *Due to file size concerns, all other data has been gitignored. If you want to work with the full dataset, follow [Aaron Fihn's instructions](./Makefile_overview.md) for downloading the data, then run his **make** command to prepare the events_renamed.pickle file*

