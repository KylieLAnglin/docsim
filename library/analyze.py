from scipy import spatial
import pandas as pd


def cosine_similarity_row(matrix: pd.DataFrame, index1, index2):
    """calculates similarity between two rows of doc-term dataframe

    Args:
        matrix (pd.DataFrame): document-term matrix with row indices
        index1 (str or int): index in matrix for main doc
        index2 (str or int): index in matrix for comp doc

    Returns:
        [float]: Cosine similarity score
    """

    return 1 - spatial.distance.cosine(matrix.loc[index1], matrix.loc[index2])


# TODO: fix so that if there are no matches?
def max_sim_of_rows(matrix: pd.DataFrame, main_index, comp_indices: list):
    """[summary]

    Args:
        matrix (pd.DataFrame): doc-term matrix
        main_index ([type]): index of row to calculate similarity to other rows
        comp_indices (list): indices of comparison rows

    Returns:
        [type]: [description]
    """
    return max(
        [cosine_similarity_row(matrix, main_index, comp) for comp in comp_indices]
    )


def row_is_peer(df: pd.DataFrame, main_row, col_to_match: str):
    """[summary]

    Args:
        df (pd.Dataframe): dataframe containing rows and peers
        main_row (index): row with value to match
        col_to_match (str): column to match

    Returns:
        [type]: list of booleans for whether row is peer

    Rows are peers to themselves.
    """

    return list(df[col_to_match] == df.loc[main_row][col_to_match])


def filter_df_with_dict(df: pd.DataFrame, filter_rules: dict):
    """Filters rows of a df using col, value rules in dict

    Args:
        df (pd.DataFrame): df to filter
        filter_rules (dict): dictionary mapping columns to needed column values

    Returns:
        [type]: [description]
    """

    return df.loc[(df[list(filter_rules)] == pd.Series(filter_rules)).all(axis=1)]
