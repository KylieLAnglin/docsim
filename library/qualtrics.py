import os
import pandas as pd
import numpy as np


def extract_column_labels(csv_path: str):
    """imports qualtrics csv and returns dict /
    containing column labels

    Args:
        csv_path (str): path to csv including file name 

    Returns:
        [dict]: dictionary mapping column names to survey q's
    """
    survey = pd.read_csv(csv_path, nrows=2)

    survey_cols = survey[0:1].to_dict('series')

    survey_labels = {}
    for key in survey_cols:
        survey_labels[key] = survey_cols[key][0]

    return survey_labels


def select_valid_rows(survey: pd.DataFrame,
                      keep_previews: bool = False,
                      min_duration: int = 45):
    """import qualtrics csv and select rows with survey responses

    Args:
        csv_path (str): path to csv including file name 

    Returns:
        [pd.DataFrame]: dataframe containing only survey responses
    """
    survey = survey[2:]

    if not keep_previews:
        survey = drop_previews(survey, min_duration=min_duration)

    return survey


def drop_meta_data(df: pd.DataFrame):
    """Select columns containing survey responses

    Args:
        df (pd.DataFrame): df containing qualtrics data with original column names

    Returns:
        [pd.DataFrame]: df only containing survey response columns, no meta-data

    Survey response column names begin with Q 
    """
    filter_col = [col for col in df if col.startswith('Q')]
    df = df[filter_col]

    return df


def search_column_labels(column_labels: dict, search_term: str, print_col: bool = False):
    """searches label dictionary for word(s)

    Args:
        column_labels (dict): dictionary with keys containing col names and values containing survey questions
        search_term (str): word to search values for

    Function is designed to take dict resulting from extract_column_labels() as argument

    Returns:
        list: List of column names containing search term
    """
    cols = []
    for key, value in column_labels.items():
        if search_term in value:
            if print_col:
                print(key, value)
            cols.append(key)

    return cols


def replace_missing_text(df: pd.DataFrame,
                         columns: list,
                         replace_str: str = ''):
    """replace nans in df text column

    Args:
        df (pd.DataFrame): dataframe containing text column
        columns (list): list of text columns with nans
        replace_str (str): replacement string
    """
    for col in columns:
        df[col] = df[col].replace(np.nan, replace_str, regex=True)

    return df


def drop_previews(df: pd.DataFrame, min_duration: int = 0):
    """drop survey entries where participant was likely just previewing

    Args:
        df (pd.DataFrame): cleaned qualtrics df
        min_duration (int, optional): Drop if duration less than provided seconds. Defaults to 45.

    Returns:
        df: df with only meaningful survey responses
    """
    df = df.loc[df.DistributionChannel != 'preview']
    df = df.loc[df.Status != 'Survey Preview']

    df = df.loc[pd.to_numeric(df['Duration (in seconds)']) > min_duration]

    return df


def drop_test_responses(df: pd.DataFrame, columns: list, values: list):
    """Drop rows where values indicate survey response was a test

    Args:
        columns (list): list of columns to check for values to drop
        values (list): values indicating survey was a test
        df: qualtrics df

    Returns:
        [type]: [description]
    """

