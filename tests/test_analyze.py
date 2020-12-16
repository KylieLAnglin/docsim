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