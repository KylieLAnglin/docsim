# %%
import re
import collections

import spacy
import nltk
import pandas as pd
import numpy as np
import scipy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from nltk.corpus import stopwords

from agileteacher.library import start

nlp = spacy.load("en_core_web_lg", disable=["parser", "ner"])

# %% Replace spacy stop word list with nltks

spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
nltk_stopwords = set(nltk.corpus.stopwords.words("english"))

for word in spacy_stopwords:
    if word not in nltk_stopwords:
        if not any(substring in word for substring in ["‘", "’", "'"]):
            lexeme = nlp.vocab[word]
            lexeme.is_stop = False

contractions = ["n't", "'d", "'ll", "'m", "'re", "'s", "'ve"]
spacy_stopwords.update(["-pron-", "-PRON-"])

# %%

# %%
def process_text(
    text: str,
    lower_case: bool = True,
    remove_punct: bool = True,
    remove_stopwords: bool = False,
    lemma: bool = False,
):

    if lemma:  # lemma needs to go first because spacy lemmatizer depends on context
        doc = " ".join([token.lemma_ for token in nlp(text)])

    elif not lemma:
        doc = " ".join([token.text for token in nlp(text)])

    if remove_stopwords:
        doc = " ".join([token.text for token in nlp(doc) if not token.is_stop])

    if remove_punct:
        doc = " ".join([token.text for token in nlp(doc) if not token.is_punct])

    if lower_case:
        doc = " ".join([token.lower_ for token in nlp(doc)])

    return doc


# %%


# %%


def vectorize_text(
    df: pd.DataFrame,
    text_col: str,
    remove_stopwords: bool = False,
    tfidf: bool = False,
    lemma: bool = False,
    lsa: bool = False,
    n_components: int = 100,
):

    docs = [
        process_text(
            text,
            lower_case=False,
            remove_punct=False,
            remove_stopwords=remove_stopwords,
            lemma=lemma,
        )
        for text in df[text_col]
    ]

    if tfidf == False:
        vec = CountVectorizer()

    elif tfidf:
        vec = TfidfVectorizer()

    X = vec.fit_transform(docs)
    matrix = pd.DataFrame(X.toarray(), columns=vec.get_feature_names(), index=df.index)

    print("Number of words: ", len(matrix.columns))

    if lsa:
        lsa_dfs = create_lsa_dfs(matrix=matrix, n_components=n_components)
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

    word_weights = word_weights_trans.sort_values(by=[0], ascending=False)

    LSA_tuple = collections.namedtuple("LSA_tuple", ["matrix", "word_weights"])
    new = LSA_tuple(matrix_lsa, word_weights)

    return new


def create_corpus_from_series(series: pd.Series):
    text = ""
    for row in series:
        text = text + row
    return text


def remove_tags(text: str, regex_str: str):
    text = re.sub(regex_str, " ", text)
    return text


# %%


def what_words_matter(doc_term_matrix: pd.DataFrame, row1, row2, show_num: int = 5):
    """Given a two vectors in a doc-term matrix, show words /
    that discriminate between the documents.

    Args:
        doc_term_matrix (pd.DataFrame): DF with terms in columns, freq in rows
        row1 ([type]): index of first doc
        row2 ([type]): index of other doc
        show_num (int): number of words to show
    """

    new_df = doc_term_matrix.loc[[row1, row2]]

    # divide by total word count
    new_df["total"] = new_df.sum(axis=1)
    totals = list(new_df.total)
    print(totals)

    new_df = new_df.div(new_df.total, axis=0).drop(columns=["total"])

    new_df = new_df.T.reset_index()
    new_df["diff"] = new_df[row1] - new_df[row2]
    new_df["abs"] = new_df["diff"].abs()

    new_df = new_df[(new_df[row1] != 0) | (new_df[row2] != 0)]

    new_df["row1_p"] = new_df[row1].round(2)
    new_df["row2_p"] = new_df[row2].round(2)

    new_df["row1"] = new_df[row1] * totals[0]
    new_df["row2"] = new_df[row2] * totals[1]

    row1_df = new_df.sort_values(by="diff").tail(show_num)
    row1_df["type"] = "row1_distinct"

    row2_df = new_df.sort_values(by="diff").head(show_num)
    row2_df["type"] = "row2_distinct"

    sim_df = new_df.sort_values(by="abs").head(show_num)
    sim_df["type"] = "shared"

    words = (
        row1_df.append(sim_df)
        .append(row2_df)
        .set_index(["type", "index"])[["row1", "row2", "row1_p", "row2_p"]]
    )

    return words


def top_terms(doc_term_matrix: pd.DataFrame, row, show_num: int = 5):
    words = list(doc_term_matrix.columns)
    frequencies = list(doc_term_matrix.loc[row])

    new_df = pd.DataFrame(list(zip(words, frequencies)), columns=["words", "frequency"])
    new_df = new_df.reset_index()
    #new_df = new_df.sort_values(by=["frequency"])
    # print(new_df.columns[0])

    # new_df = new_df.sort_values(by=new_df.columns[0], ascending=False)

    # divide by total word count
    # total = int(new_df.sum(axis=0))
    # print(total)

    # new_df = new_df.div(new_df.total, axis=0).drop(columns=["total"])

    # return new_df.head(show_num)
    return new_df


def doc_matrix_with_embeddings(df: pd.DataFrame, text_col: str):
    df_index = df[[]].reset_index()
    list_arrays = [ave_word_embedding_for_doc(text) for text in df[text_col]]
    matrix = pd.concat([df_index, pd.DataFrame(list_arrays)], axis=1)
    return matrix


def weighted_doc_matrix_with_embeddings(tfidf_matrix: pd.DataFrame):
    df_index = tfidf_matrix[[]].reset_index()
    list_arrays = [
        weighted_ave_word_embedding_for_doc(tfidf_matrix=tfidf_matrix, row=row)
        for row in tfidf_matrix.index
    ]
    matrix = pd.concat([df_index, pd.DataFrame(list_arrays)], axis=1)
    return matrix


def weighted_ave_word_embedding_for_doc(tfidf_matrix: pd.DataFrame, row):
    sum_vector = np.repeat(0, 300)
    for col, weight in zip(tfidf_matrix.columns, tfidf_matrix.loc[row]):
        sum_vector = sum_vector + (tfidf_matrix.loc[row][col] * nlp(col).vector)
    return sum_vector


def ave_word_embedding_for_doc(text: str):
    sum_vector = np.repeat(0, 300)
    for token in nlp(text):
        sum_vector = sum_vector + token.vector

    return sum_vector
