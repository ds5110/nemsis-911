# Draft Makefile for Final Project
# DS 5110
# Darby, Duggan, Jordan

# Variables
DATA_DIR = data
SRC_DIR = src
DATA_FILE = $(DATA_DIR)/nemsis_data.csv # need to confirm file path when I aquire data

# Targets
.PHONY: setup eda clean

# Setup project directories
setup:
	@mkdir -p $(DATA_DIR)
	@mkdir -p $(SRC_DIR)
	@echo "Project directories have been set up."

# Perform Exploratory Data Analysis
eda:
	$(SRC_DIR)/eda.py
	@python $(SRC_DIR)/eda.py
	@echo "Exploratory Data Analysis complete."



# Clean up generated files and directories
clean:
	@rm -rf $(SRC_DIR)/*.pyc
	@echo "Cleaned up Python bytecode files."
