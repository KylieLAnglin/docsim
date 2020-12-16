import collections
import os
import re

import pandas as pd
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import Normalizer

nlp = spacy.load("en", disable=["parser", "ner"])


def vectorize_text(
    df: pd.DataFrame,
    text_col: str,
    remove_stopwords: bool = False,
    tfidf: bool = False,
    lemma: bool = False,
    lsa: bool = False,
):
    docs = list(df[text_col])
    if remove_stopwords == False:
        stop_words = []

    elif remove_stopwords:
        stop_words = list(stopwords.words("english"))
        stop_words.append("-pron-")
        stop_words.append("pron")

    if lemma:
        docs = [
            " ".join([token.lemma_ for token in nlp(text)]) for text in df[text_col]
        ]

    if tfidf == False:
        vec = CountVectorizer(stop_words=stop_words)

    elif tfidf:
        vec = TfidfVectorizer(stop_words=stop_words)

    X = vec.fit_transform(docs)
    matrix = pd.DataFrame(X.toarray(), columns=vec.get_feature_names(), index=df.index)

    print("Number of words: ", len(matrix.columns))

    if lsa:
        lsa_dfs = create_lsa_dfs(matrix=matrix)
        matrix = lsa_dfs.matrix
        print("Number of dimensions: ", len(matrix.columns))

    return matrix


def create_lsa_dfs(
    matrix: pd.DataFrame, n_components: int = 100, random_state: int = 100
):

    lsa = TruncatedSVD(n_components=n_components, random_state=random_state)
    lsa_fit = lsa.fit_transform(matrix)
    lsa_fit = Normalizer(copy=False).fit_transform(lsa_fit)
    print(lsa_fit.shape)

    #  Each LSA component is a linear combo of words
    word_weights = pd.DataFrame(lsa.components_, columns=matrix.columns)
    word_weights.head()
    word_weights_trans = word_weights.T

    # Each document is a linear combination of components
    matrix_lsa = pd.DataFrame(lsa_fit, index=matrix.index, columns=word_weights.index)
    matrix_lsa.sample(5)

    word_weights = word_weights_trans.sort_values(by=[0], ascending=False)

    LSA_tuple = collections.namedtuple("LSA_tuple", ["matrix", "word_weights"])
    new = LSA_tuple(matrix_lsa, word_weights)

    return new
