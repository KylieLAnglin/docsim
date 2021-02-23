# %%
import pandas as pd

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

from docsim.library import start
from docsim.library import process_text
from docsim.library import analyze
from docsim.library import clean_text

# %%

df_corpus = pd.read_csv(start.CLEAN_FILEPATH + "text_transcripts.csv")
df_ideal = pd.read_csv(start.CLEAN_FILEPATH + "text_scripts.csv")
df = df_corpus.append(df_ideal)

df["filename"] = df.filename.str.replace(".docx", "")

df = df.set_index("filename")

df = df.dropna(subset=["skill"])

# %%
cleaning_families = {
    "avatar": ["Ethan", "Dev", "Ava", "Jasmine"],
    "avatar's": ["Ethan's", "Dev's", "Ava's", "Jasmines'"],
    "gonna": ["going to"],
    "kinda": ["kind of"],
    "wanna": ["want to"],
    "pretend": ["I'll be", "I’m going to be a"],
    "improve": ["shape"],
}


behavior_families = {
    "misbehavior": [
        "hum",
        "hums",
        "humming",
        "whisper",
        "whispers",
        "whispering",
        "off-task",
        "off",
        "beat-box",
        "beat-boxing",
        "beat",
        "rocket",
        "phone",
        "sing",
        "singing",
        "texting",
        "drum",
        "drumming",
        "impersonation",
        "impersonations",
        "impersonating",
        "impersonate",
        "darth",
        "impression",
        "noise",
        "noises",
        "mumble",
        "game",
        "silly",
        "superhero",
        "superheros",
        "drummin",
        "Darth Vadar",
        "Jedi",
        "Trump",
    ],
    "redirection": ["voice", "pocket", "eyes", "ears", "finger", "verbal"],
}

feedback_families = {
    "text": ["paragraph", "sentence"],
}


# %%
df_behavior = df[df.scenario == "behavior"]
df_behavior["new_text"] = [
    clean_text.word_family_from_dict(text, behavior_families)
    for text in df_behavior.clean_text
]

df_feedback = df[df.scenario == "feedback"]
df_feedback["new_text"] = [
    clean_text.word_family_from_dict(text, feedback_families)
    for text in df_feedback.clean_text
]

df = df_feedback.append(df_behavior)
df["new_text"] = [
    clean_text.word_family_from_dict(text, cleaning_families) for text in df.new_text
]

# %%
matrix0 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=False, tfidf=False, lemma=False, lsa=False
).add_prefix("term_")

df["script_sim0"] = [
    analyze.cosine_similarity_row(matrix0, row, df.loc[row].skill)
    for row in matrix0.index
]

# %%
matrix1 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=False, lemma=False, lsa=False
).add_prefix("term_")

df["script_sim1"] = [
    analyze.cosine_similarity_row(matrix1, row, df.loc[row].skill)
    for row in matrix1.index
]

# process_text.what_words_matter(matrix1, "6-2C", "behavior2", 10)
# process_text.what_words_matter(matrix1, "49-2C", "behavior3", 10)
# process_text.what_words_matter(matrix1, "78-2C", "behavior3", 10)
# process_text.what_words_matter(matrix1, "6-2C", "behavior2", 10)

# process_text.what_words_matter(matrix1, "2019_58_5C", "behavior2", 10)

# process_text.what_words_matter(matrix1, "2019_58_5C", "behavior2", 20)

# %%
matrix2 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=True, lemma=False, lsa=False
).add_prefix("term_")

df["script_sim2"] = [
    analyze.cosine_similarity_row(matrix2, row, df.loc[row].skill)
    for row in matrix2.index
]

# process_text.what_words_matter(matrix2, "6-2C", "behavior2", 20)
# process_text.what_words_matter(matrix2, "01_1920_05_008_22c", "behavior2", 20)
# process_text.top_terms(matrix2, "01_1920_05_008_22c", 10)

# process_text.what_words_matter(matrix2, "99-2C", "behavior3", 20)

# %%
matrix3 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=False, lemma=True, lsa=False
).add_prefix("term_")

df["script_sim3"] = [
    analyze.cosine_similarity_row(matrix3, row, df.loc[row].skill)
    for row in matrix3.index
]

# %%
matrix4 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=True, lemma=True, lsa=False
).add_prefix("term_")

df["script_sim4"] = [
    analyze.cosine_similarity_row(matrix4, row, df.loc[row].skill)
    for row in matrix4.index
]

# %%
matrix5 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=False, lemma=False, lsa=True
).add_prefix("term_")

df["script_sim5"] = [
    analyze.cosine_similarity_row(matrix5, row, df.loc[row].skill)
    for row in matrix5.index
]

# %%
matrix6 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=True, lemma=True, lsa=True
).add_prefix("term_")

df["script_sim6"] = [
    analyze.cosine_similarity_row(matrix6, row, df.loc[row].skill)
    for row in matrix6.index
]

# %% Doc 2 Vec

model = Doc2Vec.load(start.CLEAN_FILEPATH + "doc2vec.model")

tokenized_docs = [word_tokenize(row.lower()) for row in df.clean_text]

matrix_lists = [model.infer_vector(doc) for doc in tokenized_docs]
matrix7 = pd.DataFrame(matrix_lists, index=df.index)

df["script_sim7"] = [
    analyze.cosine_similarity_row(matrix7, row, df.loc[row].skill)
    for row in matrix7.index
]

# %% Doc 2 Vec with Pre-processing (performs worse than without)
# stop = process_text.spacy_stopwords
# tokenized_docs_no_stop = [
#     [i for i in word_tokenize(row.lower()) if i not in stop] for row in df.clean_text
# ]

# matrix_lists = [model.infer_vector(doc) for doc in tokenized_docs_no_stop]
# matrix8 = pd.DataFrame(matrix_lists, index=df.index)

# df["script_sim8"] = [
#     analyze.cosine_similarity_row(matrix8, row, df.loc[row].skill)
#     for row in matrix8.index
# ]

# %%
matrix8 = process_text.vectorize_text(
    df,
    "new_text",
    remove_stopwords=False,
    tfidf=True,
    lemma=False,
    lsa=False,
    n_gram_range=(1, 2),
).add_prefix("term_")

df["script_sim8"] = [
    analyze.cosine_similarity_row(matrix8, row, df.loc[row].skill)
    for row in matrix8.index
]


# %%

df[
    [
        "study",
        "id",
        "year",
        "semester",
        "scenario",
        "skill",
        "coach",
        "script_sim0",
        "script_sim1",
        "script_sim2",
        "script_sim3",
        "script_sim4",
        "script_sim5",
        "script_sim6",
        "script_sim7",
        "script_sim8",
    ]
].to_csv(start.CLEAN_FILEPATH + "vectorizations.csv")

# %%
