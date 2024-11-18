# Proposal

This project uses the 2022 public research dataset of national EMS records from [NEMSIS](https://nemsis.org/) to explore
and model the relationship between urbanicity/rurality and the probability of surviving a cardiac arrest.

This project has multiple goals:
  1. Create a reproducible data pipeline that filters the massive NEMSIS public research dataset into a smaller set of
cardiac arrest-related records. This should be automated to allow future researchers to request the same dataset from
NEMSIS and filter it down to the same exact records.
  2. Use this smaller dataset to determine the effects of urbanicity/rurality on cardiac arrest survivability.
  3. Model that survivability using the dataset's available features. (*Who* this model is for and *what* it would be
useful for can be answered after a closer look at the dataset when the exploratory data analysis is completed.)

## Original Timeline:
  - 11/8: Date pipeline completed, imputation work tentatively finished
  - 11/15: The following is completed:
    - Transform the dataset for modeling convenience, including grouping similar categorical features (rural/wilderness) and one-hot encoding for categorical variables
    - Perform an inferential analysis: Find correlations between urbanicity and lethality, identify other features associated with lethality
    - Create visualizations to understand inferential conclusions
  - 11/22: Build and test the accuracy of simple models, including logistic regression and naive bayes.
  - 11/29: Build and test the accuracy of more complicated models, including random forest and xgboost.
  - 12/6: Present results to class.
  - 12/11: Submit the final results, including the reproducible code repo and a written report.
