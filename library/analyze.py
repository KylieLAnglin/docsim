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


def max_sim_of_rows(matrix: pd.DataFrame, main_index, comp_indices: list):
    try:
        return max(
            [cosine_similarity_row(matrix, main_index, comp) for comp in comp_indices]
        )
    except:
        return None


# TODO: fix so that if there are no matches?
