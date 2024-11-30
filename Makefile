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

build: ./reports/preliminary_eda.txt eda_charts calculate_epinephrine_usage find_cols 

./reports/preliminary_eda.txt: ./data/processed/selected_events.pickle
	python ./src/column_info.py

eda_charts: ./data/processed/selected_events.pickle
	python ./src/eda_charts.py

calculate_epinephrine_usage: ./data/processed/selected_events.pickle
	python ./src/calculate_epinephrine_usage.py

./data/processed/selected_events.pickle: $(unzipped_csvs)
	python ./src/create_NEMSIS_db.py
	python ./src/load_data_NEMSIS_db.py
	python ./src/filter_primary_NEMSIS_cases.py

find_cols: col_headers
	python ./src/nemsis_find_cols.py

col_headers: ./data/repaired/ASCII\ 2022_repaired.zip
	python ./src/nemsis_text_format.py

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
	rm -f data/NEMSIS_PUB.db
	rm -f figs/*
	rm -f reports/col_locations/cols_of_interest.txt 
	rm -f reports/preliminary_eda.txt
	rm -f reports/text_file_headers/*
	rm -f reports/epinephrine_usage.txt

environment:
	conda env create -n project-duggani -f environment.yml
# conda activate project-duggani

query:
	python ./src/query.py
