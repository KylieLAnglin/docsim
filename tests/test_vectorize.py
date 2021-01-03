import pandas as pd
import scipy
import pandas as pd
import scipy

from docsim.library import process_text


text = "So, now we're going to take ten seconds for each partner."
text_df = pd.DataFrame({"text": [text]})


def test_process_text():
    text_result = process_text.process_text(
        text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=False,
        lemma=False,
    )
    assert text_result == "so now we 're going to take ten seconds for each partner"

    text_result2 = process_text.process_text(
        text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=True,
        lemma=False,
    )
    assert "so" not in text_result2[0]

    text_result4 = process_text.process_text(
        text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=True,
        lemma=True,
    )
    print(text_result4)
    assert "-pron-" not in text_result4


def test_vectorize_text():
    # no processing
    result = process_text.vectorize_text(
        text_df, "text", remove_stopwords=False, tfidf=False, lemma=False, lsa=False
    )
    assert len(result.columns) == 12

    # no stop words
    result = process_text.vectorize_text(
        text_df, "text", remove_stopwords=True, tfidf=False, lemma=False, lsa=False
    )
    assert "so" not in list(result.columns)

    result = process_text.vectorize_text(
        text_df, "text", remove_stopwords=False, tfidf=False, lemma=True, lsa=False
    )
    assert len(result.columns) == 12
    assert "be" in list(result.columns)


# This test passes.
def test_vectorize_text_lemma():
    text = "Everybody is going to be answering. Go ahead and answer."
    text_df = pd.DataFrame({"text": [text]})

    result = process_text.vectorize_text(
        text_df, "text", remove_stopwords=True, tfidf=False, lemma=True, lsa=False
    )

    assert "answering" not in list(result.columns)


def test_what_words_matter():
    test = pd.DataFrame(
        {
            "word1": [1, 5],
            "word2": [5, 1],
            "word3": [3, 3],
            "word4": [4, 1],
            "word5": [2, 4],
            "words6": [0, 0],
            "words7": [1, 1],
        }
    )

    test2 = test.copy()
    test2["words8"] = [100, 200]
    # print(1 - scipy.spatial.distance.cosine(test.loc[0], test.loc[1]))
    # print(1 - scipy.spatial.distance.cosine(test2.loc[0], test2.loc[1]))

    result = process_text.what_words_matter(test2, 0, 1, 3)
    # print(result)

    assert result.loc[("row1_distinct", "word2")][0] == 5
