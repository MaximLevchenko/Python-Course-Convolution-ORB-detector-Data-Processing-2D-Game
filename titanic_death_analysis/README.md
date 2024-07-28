# Titanic Survival Analysis

## Overview

This project involves analyzing the Titanic dataset to explore various aspects related to passenger demographics, survival rates, and other characteristics. The dataset includes information about the passengers, such as their age, sex, class, fare, and whether they survived the disaster.

## Project Structure
### Directory and File Descriptions

- **data/**: This directory stores the datasets required for analysis, along with their corresponding encrypted and signature files to ensure data integrity and security.
  - `test.csv` and `train.csv`: These are the primary datasets used for testing and training, respectively.
  - Encrypted and signature files: These files (`.enc` and `.sign`) ensure the authenticity and confidentiality of the datasets.

- **tests/**: Contains the test scripts and related files for validating the data processing and analysis functions.
  - `test_analysis.py`: This script includes various test cases that check the functionality and accuracy of the functions implemented in `titanic_analysis.py`.
  - Encrypted and signature files: These files are used for secure handling of test data and scripts.

- **README.md**: Provides a comprehensive overview of the project, including descriptions of the datasets, data processing functions, testing procedures, and more.

- **titanic_analysis.py**: The main Python script that houses the core functions for loading, processing, and analyzing the Titanic dataset.

## Dataset

The dataset used in this project contains the following attributes:

- **Age**: Age of the passenger in years.
- **Fare**: Ticket fare price.
- **Name**: Name of the passenger.
- **Parch**: Number of parents/children aboard.
- **PassengerId**: Unique identifier for each passenger.
- **Pclass**: Passenger class (1 = 1st, 2 = 2nd, 3 = 3rd).
- **Sex**: Gender of the passenger.
- **SibSp**: Number of siblings/spouses aboard.
- **Survived**: Survival indicator (0 = Did not survive, 1 = Survived).
- **Embarked**: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton).
- **Cabin**: Cabin number.
- **Ticket**: Ticket number.

## Usage

### Data Processing Functions

The `titanic_analysis.py` script includes several functions for data processing and analysis:

- `load_dataset(train_file_path, test_file_path)`: Loads and combines the train and test datasets, adding a "Label" column to distinguish between them.
- `get_missing_values(df)`: Identifies and returns a DataFrame of missing values and their percentages.
- `substitute_missing_values(df)`: Fills missing values in the "Age" and "Fare" columns.
- `get_correlation(df)`: Calculates the Pearson correlation coefficient between "Age" and "Fare".
- `get_survived_per_class(df, group_by_column_name)`: Computes survival rates based on specified groupings (e.g., by class or gender).
- `get_outliers(df)`: Identifies outliers in ticket fare prices using the IQR method.
- `create_new_features(df)`: Creates new features such as scaled fares, logarithmic ages, and numerical gender indicators.
- `determine_survival(df, n_interval, age, sex)`: Predicts survival probability based on age and sex.

## Testing

The `test_analysis.py` script contains tests to ensure the correctness of the data processing functions. It uses `pytest` and includes tests for:

- Loading datasets
- Handling missing data
- Substituting missing values
- Calculating correlations
- Determining survival rates per class
- Detecting outliers
- Creating new features
- Estimating survival probabilities

### Running the Tests

To run the tests, use the following command:

```bash
pytest test_analysis.py
```
Ensure that you have the necessary dependencies installed, including numpy, pandas, and pytest.

## Dependencies
This project requires the following Python packages:
- **numpy**
- **pandas**
- **pytest**
