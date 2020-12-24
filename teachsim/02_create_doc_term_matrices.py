# %%
import pandas as pd

from docsim.library import start
from docsim.library import vectorize
from docsim.library import process_text

# %%

df_corpus = pd.read_csv(start.clean_filepath + "text_transcripts.csv").set_index(
    ["study", "id"]
)
df_ideal = pd.read_csv(start.clean_filepath + "text_scripts.csv").set_index(
    ["study", "id"]
)
df = df_corpus.append(df_ideal)

# %%

matrix = process_text.vectorize_text(
    df, "clean_text", remove_stopwords=False, tfidf=False, lemma=False, lsa=False
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=False,
        lemma=False,
    )
    for text in df.clean_text
]

matrix.to_csv(start.clean_filepath + "matrix.csv")

# %%
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=False, tfidf=True, lemma=False, lsa=False
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=False,
        lemma=False,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_wgt.csv")

# %%
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=True, tfidf=False, lemma=False, lsa=False
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=True,
        lemma=False,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_stop.csv")

# %%
# # Stop and weight
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=True, tfidf=True, lemma=False, lsa=False
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=True,
        lemma=False,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_stop_wgt.csv")

# %% Stem
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=False, tfidf=False, lemma=True, lsa=False
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=False,
        lemma=True,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_stem.csv")

# %% Stop and Stem
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=True, tfidf=False, lemma=True, lsa=False
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=True,
        lemma=True,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_stop_stem.csv")


# %% # Stop Stem and Weight
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=True, tfidf=True, lemma=True, lsa=False
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=True,
        lemma=True,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_stop_stem_wgt.csv")

# %% LSA
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=False, tfidf=False, lemma=False, lsa=True
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=False,
        lemma=False,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_lsa.csv")

# %% # LSA + Stop
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=True, tfidf=False, lemma=False, lsa=True
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=True,
        lemma=False,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_stop_lsa.csv")


# %% LSA, Weighting, Stop Words
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=True, tfidf=True, lemma=False, lsa=True
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=True,
        lemma=False,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_stop_wgt_lsa.csv")

# %%
matrix = vectorize.vectorize_text(
    df, "clean_text", remove_stopwords=True, tfidf=True, lemma=True, lsa=True
).add_prefix("term_")
matrix["text"] = [
    process_text.process_text(
        text=text,
        lower_case=True,
        remove_punct=True,
        remove_stopwords=True,
        lemma=True,
    )
    for text in df.clean_text
]
matrix.to_csv(start.clean_filepath + "matrix_stop_stem_wgt_lsa.csv")
