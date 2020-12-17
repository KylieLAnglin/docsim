from docsim.library import analyze
import pandas as pd

test_dict = {"test1": [1, 2, 3, 4], "test2": [1, 2, 3, 4], "test3": [1, 1, 1, 2]}
test = pd.DataFrame.from_dict(test_dict, orient="index")


def test_cosine_similarity_row():

    result = analyze.cosine_similarity_row(test, "test1", "test2")

    assert result == 1


def test_max_sim_of_rows():

    result = analyze.max_sim_of_rows(test, "test1", ["test2", "test3"])
    assert result == 1


def test_row_is_peer():

    test = pd.DataFrame({"col1": [1, 2, 2]})
    result = analyze.row_is_peer(test, 1, "col1")

    assert result[2] == True


def test_filter_df_with_dict():
    test = pd.DataFrame({"col1": [1, 2, 2, 1], "col2": [2, 3, 4, 2]})
    test_rule = {"col1": 1, "col2": 2}
    result = analyze.filter_df_with_dict(test, test_rule)

    assert list(result.index) == [0, 3]

    test = pd.DataFrame({"col1": [1, 2, 2, 1], "col2": [2, 3, 4, 2]})
    test_rule = {}
    result = analyze.filter_df_with_dict(test, test_rule)

    assert list(result.index) == [0, 1, 2, 3]


def test_row_matches_in_list():
    test = pd.DataFrame({"col1": [1, 2, 2, 1], "col2": [2, 3, 4, 2]})
    result = analyze.row_matches_in_lists(test, "col1")
    assert result[0] == [0, 3]
