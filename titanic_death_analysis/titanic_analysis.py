"""
In this homework, we will use well-known Titanic dataset which contains 
information about passengers of Titanic. The dataset consists of personal 
information about each passenger and indicator whether the passenger 
survived. We will use this data to analyse passenger list and their chance for
survival.

The provided dataset contains the following attributes:
 'Age' - age in years,
 'Fare' - fare ticked price,
 'Name' - passenger name,
 'Parch' - # of parents/children of a person on board,
 'PassengerId' - identifier,
 'Pclass' - travelling class, 1 = 1. class, 2 = 2. class, 3 = 3. class,
 'Sex' - sex,
 'SibSp' - # siblings/spouses on board,
 'Survived' - 0 = died, 1 = survived,
 'Embarked' - boarding port C = Cherbourg, Q = Queenstown, S = Southampton,
'Cabin' - cabin number
 'Ticket' - ticket number
"""

import pandas as pd
import numpy as np


def load_dataset(train_file_path: str, test_file_path: str) -> pd.DataFrame:
    """
    Write a function which loads CSV from two files to pandas DataFrame and
    performs several data processing steps. Use data provided in `data`
    directory for testing ('data/train.csv' as input parameter
    `train_file_path`, and 'data/test.csv'  as `test_file_path`). Add column
    name "Label" to each DataFrame. The column should contain value "Train"
    for data from `train_file_path` and "Test" from test_file_path.

    Perform following operations with DataFrames (keep the order of the
    operations):
        1. Concatenate both DataFrames.
        2. Remove columns  "Ticket", "Embarked", "Cabin" from created DataFrame.
        3. Set the index to unique numbers from zero to the number of rows.

    The return value of the function is processed DataFrame.
    """
    train_df = pd.read_csv(train_file_path)
    test_df = pd.read_csv(test_file_path)

    # Add "Label" column and set values based on file source
    train_df['Label'] = 'Train'
    test_df['Label'] = 'Test'

    # Concatenate both DataFrames
    df = pd.concat([train_df, test_df], ignore_index=True)

    # Remove specified columns
    columns_to_remove = ["Ticket", "Embarked", "Cabin"]
    df = df.drop(columns=columns_to_remove)

    # Set the index to unique numbers from zero to the number of rows
    df = df.set_index(pd.RangeIndex(start=0, stop=len(df)))

    return df


def get_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    When working and analysing data, one often needs to deal with missing
    values. For example, some passengers did not fill information about
    family members. In that case, one needs to be aware of it as it may
    introduce bias to the data.

    Write a function which determines the number of missing values in given
    DataFrame. The function should output a new DataFrame. The new DataFrame
    should be indexed by columns of original DataFrame. Columns of returned
    DataFrame will be (keep the order of the columns):
        1. "Total" - contains the number of missing values
        2. "Percent" - contains the percentage of missing values with regard to all
        rows of given DataFrame.

    Sort the resulting DataFrame based on the number of missing values from
    largest to smallest.

    Example of output:

               |  Total  |  Percent
    "Column1"  |   34.5  |    76.54321
    "Column2"  |   0     |    0
    """
    # Calculate total missing values
    total_missing = df.isnull().sum()

    # Calculate percentage of missing values
    percent_missing = (total_missing / len(df)) * 100

    # Create a new DataFrame with "Total" and "Percent" columns
    result_df = pd.DataFrame({"Total": total_missing, "Percent": percent_missing})

    # Sort the DataFrame based on the "Total" column in descending order
    result_df = result_df.sort_values(by="Total", ascending=False)

    return result_df


def substitute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    One way how to handle missing data is to substitute missing values with
    some statistic of other rows. We will use this method for two columns:
        1. "Age" - fill missing values with the mean of other rows.
        2. "Fare" - fill missing values with the lowest price of ~$15 (we
        suppose that the majority of unregistered tickets were the cheapest
        ones).

    Do not to modify given DataFrame but create a copy of it.
    """

    # Create a copy of the input DataFrame to avoid modifying the original
    df_copy = df.copy()

    # Substitute missing values in the "Age" column with the mean
    age_mean = df_copy['Age'].mean()
    df_copy['Age'].fillna(age_mean, inplace=True)

    # Substitute missing values in the "Fare" column with the lowest price of ~$15
    lowest_fare = 15.0
    df_copy['Fare'].fillna(lowest_fare, inplace=True)

    return df_copy


def get_correlation(df: pd.DataFrame) -> float:
    """
    We want to know whether there is a relationship between the age of a
    passenger and fare ticket price (e.g. younger children have cheaper
    tickets). We will use Pearson correlation coefficient to quantify linear
    relationship between columns "Age" and "Fare".
    The result will be returned as one number.

    Pearson correlation coefficient quantifies linear relationship between
    two random variables. Correlation ranges from -1 to 1. Value around zero
    indicates no linear relationship, -1 indicates strong negative
    relationship, 1 indicates strong relationship.
    """

    # Calculate the Pearson correlation coefficient between "Age" and "Fare"
    correlation_coefficient = df['Age'].corr(df['Fare'])

    return correlation_coefficient


def get_survived_per_class(df: pd.DataFrame,
                           group_by_column_name: str) -> pd.Series:
    """
    We want to know how big was the chance of survival for different groups of
    passengers (e.g. for different sexes, classes, etc.). Write a function
    that estimates that. The input of the function is a DataFrame with data
    and name of column (group_by_column_name) which holds group information.
    To increase readability of the result sort values from the highest chance of
    survival to lowest and round the resulting values to 2 decimal places.
    Return result as pandas Series.

    Example:

    get_survived_per_class(df, "Sex")

                  Survived
    Female     |      0.82
    Male       |      0.32

    """

    # Group the DataFrame by the specified column and calculate the mean of the "Survived" column
    survived_per_class = df.groupby(group_by_column_name)['Survived'].mean()

    # Sort values from highest to lowest and round to 2 decimal places
    survived_per_class = survived_per_class.sort_values(ascending=False).round(2)

    return survived_per_class


def get_outliers(df: pd.DataFrame) -> (int, pd.DataFrame):
    """
    We want to explore fare ticket prices. An important part of such
    exploration is exploration of outliers. An outlier may indicate an error
    in the data (somebody entered price incorrectly) or some special group of
    passengers.

    We will use the IQR method for the identification of outliers. IQR method
    considers an outlier any point which does not fulfil:
        Q1 - 1.5*IQR < point_value < Q3 + 1.5*IQR,
    where Q1 and Q3 are the first and the third quartiles respectively
    calculated from all points in data. IQR is the inter-quartile range
    calculate as the difference between Q3 and Q1:
        IQR = Q3 - Q1.

    Return tuple with the number of outliers and all passengers with outlier
    fare ticket price.
    """

    # Calculate the first and third quartiles
    q1 = df['Fare'].quantile(0.25)
    q3 = df['Fare'].quantile(0.75)

    # Calculate the inter-quartile range (IQR)
    iqr = q3 - q1

    # Identify outliers based on the IQR method
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[(df['Fare'] < lower_bound) | (df['Fare'] > upper_bound)]

    return len(outliers), outliers


def create_new_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    To analyse data and use them for modeling, it may be convenient to create
    a new columns (features). These new features are usually created
    transformation of original values. For example, if we want to compare
    survivals from Titanic and SS Eastland we will want to scale fare prices
    to the same values for each ship as travelling on Titanic was more
    expensive.

    Create 3 new variables:
        1. "Fare_scaled" - scale "Fare" columns to have zero mean and standard
       deviation equal one.
        2. "Age_log" - is natural logarithm of attribute "Age" (differences
        between age of children are magnified in comparison to adults).
        3. "Sex" -  Replace string values with numerical ones, where "male"
        will be replaced with 0 and "female" with 1. The resulting values
        should have type `int`.

    Do not modify original DataFrame.
    """

    # Create a copy of the original DataFrame
    new_df = df.copy()

    # Feature 1: "Fare_scaled"
    new_df['Fare_scaled'] = (new_df['Fare'] - new_df['Fare'].mean()) / new_df['Fare'].std()

    # Feature 2: "Age_log"
    new_df['Age_log'] = np.log(new_df['Age'])

    # Feature 3: "Sex"
    sex_mapping = {'male': 0, 'female': 1}
    new_df['Sex'] = new_df['Sex'].map(sex_mapping).astype(int)

    return new_df


def determine_survival(df: pd.DataFrame, n_interval: int, age: float,
                       sex: str) -> float:
    """
    Determine the probability of survival of a person specified by age and sex.

    Missing values in column "Age" replace with mean value. In order to
    moderate significance of the estimated probability, divide "Age" to
    specified number of intervals and calculate probability from given
    interval. For example if we have values in "Age" column [2, 13, 18, 25] and
    we want 2 intervals, result should be:

    0    (1.977, 13.5]
    1     (13.5, 25.0]

    With division based on "Sex", the categorization should be:

       "AgeInterval" | "Sex"       |   "Survival Probability"
       (1.977, 13.5] | "male"      |            0.21
       (1.977, 13.5] | "female"    |            0.28
       (13.5, 25.0]  | "male"      |            0.10
       (13.5, 25.0]  | "female"    |            0.15

    Output of determine_survival(df, n_interval=2, age = 5, sex = "male")
    should be 0.21. If there is no passenger for some group, return numpy
    NA value.
    """

    # Create a copy of the original DataFrame
    df_copy = df.copy()

    # Replace missing values in the "Age" column with the mean
    df_copy['Age'].fillna(df_copy['Age'].mean(), inplace=True)

    # Divide "Age" into specified number of intervals
    df_copy['AgeInterval'] = pd.cut(df_copy['Age'], bins=n_interval)

    # Group by "AgeInterval" and "Sex" and calculate the survival probability
    grouped_df = df_copy.groupby(['AgeInterval', 'Sex'])['Survived'].mean().reset_index()

    # Filter the DataFrame based on the specified age and sex
    filtered_df = grouped_df[(grouped_df['AgeInterval'].apply(lambda x: age in x)) & (grouped_df['Sex'] == sex)]

    # If there is no passenger for the specified group, return numpy NA value
    if filtered_df.empty:
        return np.nan
    # Extract and return the survival probability
    return filtered_df['Survived'].values[0]
