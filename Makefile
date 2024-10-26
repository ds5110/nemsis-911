unzipped_csvs = ./data/interim/ComputedElements.txt \
                ./data/interim/EINJURY_01REF.txt \
                ./data/interim/EPROCEDURES_03REF.txt \
                ./data/interim/ESITUATION_09REF.txt \
                ./data/interim/ESITUATION_10REF.txt \
                ./data/interim/ESITUATION_11REF.txt \
                ./data/interim/ESITUATION_12REF.txt \
                ./data/interim/FACTPCRADDITIONALRESPONSEMODE.txt \
                ./data/interim/FACTPCRADDITIONALSYMPTOM.txt \
                ./data/interim/FACTPCRADDITIONALTRANSPORTMODE.txt \
                ./data/interim/FACTPCRALCOHOLDRUGUSEINDICATOR.txt \
                ./data/interim/FACTPCRARRESTCPRPROVIDED.txt \
                ./data/interim/FACTPCRARRESTRESUSCITATION.txt \
                ./data/interim/FACTPCRARRESTRHYTHMDESTINATION.txt \
                ./data/interim/FACTPCRARRESTROSC.txt \
                ./data/interim/FACTPCRARRESTWITNESS.txt \
                ./data/interim/FACTPCRBARRIERTOCARE.txt \
                ./data/interim/FACTPCRCAUSEOFINJURY.txt \
                ./data/interim/FACTPCRDESTINATIONREASON.txt \
                ./data/interim/FACTPCRDESTINATIONTEAM.txt \
                ./data/interim/FACTPCRDISPATCHDELAY.txt \
                ./data/interim/FACTPCRINJURYRISKFACTOR.txt \
                ./data/interim/FACTPCRMEDICATION.txt \
                ./data/interim/FACTPCRPRIMARYIMPRESSION.txt \
                ./data/interim/FACTPCRPRIMARYSYMPTOM.txt \
                ./data/interim/FACTPCRPROCEDURE.txt \
                ./data/interim/FACTPCRPROTOCOL.txt \
                ./data/interim/FACTPCRRESPONSEDELAY.txt \
                ./data/interim/FACTPCRSCENEDELAY.txt \
                ./data/interim/FACTPCRSECONDARYIMPRESSION.txt \
                ./data/interim/FACTPCRTRANSPORTDELAY.txt \
                ./data/interim/FACTPCRTRAUMACRITERIA.txt \
                ./data/interim/FACTPCRTURNAROUNDDELAY.txt \
                ./data/interim/FACTPCRVITAL.txt \
                ./data/interim/FACTPCRWORKRELATEDEXPOSURE.txt \
                ./data/interim/PCRMEDCOMPGROUP.txt \
                ./data/interim/PCRPATIENTRACEGROUP.txt \
                ./data/interim/PCRPROCCOMPGROUP.txt \
                ./data/interim/PCRVITALECGGROUP.txt \
                ./data/interim/PCRVITALECGINTERPRETATIONGROUP.txt \
                ./data/interim/PCRVITALGLASGOWQUALIFIERGROUP.txt \
                ./data/interim/Pub_PCRevents.txt

build: ./reports/chi-square.txt

environment:
	conda env create -n dsProjEnv -f environment.yml
# conda activate dsProjEnv

prelim-eda:
	python src/data/column_info.py

eda-charts:
	python src/data/eda_charts.py

./reports/chi-square.txt: ./data/processed/events_renamed.pickle
	python ./src/data/analysis.py

./data/processed/events_renamed.pickle: ./data/processed/events.pickle
	python ./src/data/rename_columns.py

# Convert the CSV to a pickle of a pandas dataframe
./data/processed/events.pickle: ./data/csv/Pub_PCRevents.csv ./data/csv/ComputedElements.csv
	python ./src/data/make_dataset.py

# Pub_PCRevents.txt uses a multi-character delimiter, which means pandas.read_csv() must use the python parsing engine.
# This raises an error when using the chunksize argument and a callable skiprows argument together. Converting the
# delimiter to a comma avoids this issue. For more details, see: https://github.com/pandas-dev/pandas/issues/55677
./data/csv/Pub_PCRevents.csv: $(unzipped_csvs)
	sed 's/~|~/,/g' ./data/interim/Pub_PCRevents.txt > ./data/csv/Pub_PCRevents.csv

./data/csv/ComputedElements.csv: $(unzipped_csvs)
	sed 's/~|~/,/g' ./data/interim/ComputedElements.txt > ./data/csv/ComputedElements.csv

$(unzipped_csvs) &: ./data/repaired/ASCII\ 2022_repaired.zip
	unzip -jo "./data/repaired/ASCII 2022_repaired.zip" -d ./data/interim
	touch -c ./data/interim/*

# The zip file from NEMSIS is corrupted and must be repaired before unzipping
./data/repaired/ASCII\ 2022_repaired.zip: ./data/raw/ASCII\ 2022.zip
	zip -FFfz "./data/raw/ASCII 2022.zip" --out "./data/repaired/ASCII 2022_repaired.zip"

clean:
	find ./data/processed/ -type f -not -name '.gitignore' -delete
	find ./data/csv/ -type f -not -name '.gitignore' -delete
	find ./data/interim/ -type f -not -name '.gitignore' -delete
	find ./data/repaired/ -type f -not -name '.gitignore' -delete