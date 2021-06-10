# %%
import pandas as pd


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
    "avatar1": [
        "Ethan",
        "Dev",
    ],
    "avatar2": ["Ava", "Jasmine", "Savannah"],
    "avatar's": ["Ethan's", "Dev's", "Ava's", "Jasmines'", "Savannah's"],
    "gonna": ["going to"],
    "kinda": ["kind of"],
    "wanna": ["want to"],
    "pretend": [
        "I'll be",
        "I’m going to be",
        "role play",
    ],
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
        "beat-boxes",
        "beat",
        "beatbox",
        "beatboxing",
        "rocket club",
        "phone",
        "sing",
        "sings",
        "singing",
        "text",
        "texts",
        "texting",
        "drum",
        "drums",
        "drumming",
        "bang",
        "bangs",
        "banging",
        "impression",
        "impersonation",
        "impersonations",
        "noise",
        "noises",
        "noisy",
        "mumble",
        "video",
        "game",
        "silly",
        "superhero",
        "superheros",
        "darth vadar",
        "jedi",
        "trump",
        "tap",
        "taps",
        "tapping",
        "side conversation",
        "beach",
        "pencil",
        "pencils",
    ],
    "redirection": [
        "voice",
        "pocket",
        "eyes",
        "ears",
        "finger",
        "verbal",
        "re-direction",
        "re-directions",
    ],
    "tone": ["abrasive", "intimidating", "harsh"],
}

feedback_families = {
    "text": ["paragraph", "sentence"],
}


# %%
df_behavior = df[df.scenario == "behavior"]
df_behavior["new_text"] = [
    clean_text.word_family_from_dict(text, behavior_families)
    for text in df_behavior.clean_text.str.lower()
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
matrix1 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=False, tfidf=False, lemma=False, lsa=False
).add_prefix("term_")

df["script_sim1"] = [
    analyze.cosine_similarity_row(matrix1, row, df.loc[row].skill)
    for row in matrix1.index
]


# %%
matrix2 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=False, lemma=False, lsa=False
).add_prefix("term_")

df["script_sim2"] = [
    analyze.cosine_similarity_row(matrix2, row, df.loc[row].skill)
    for row in matrix2.index
]


# %%
matrix3 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=True, lemma=False, lsa=False
).add_prefix("term_")

df["script_sim3"] = [
    analyze.cosine_similarity_row(matrix3, row, df.loc[row].skill)
    for row in matrix3.index
]


# %%


# %%
matrix4 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=True, lemma=True, lsa=False
).add_prefix("term_")

df["script_sim4"] = [
    analyze.cosine_similarity_row(matrix4, row, df.loc[row].skill)
    for row in matrix4.index
]

# %%


# %%
matrix5 = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=True, lemma=True, lsa=True
).add_prefix("term_")

df["script_sim5"] = [
    analyze.cosine_similarity_row(matrix5, row, df.loc[row].skill)
    for row in matrix5.index
]
# %%
matrix6 = process_text.vectorize_text(
    df,
    "new_text",
    remove_stopwords=True,
    tfidf=True,
    lemma=False,
    lsa=False,
    n_gram_range=(1, 3),
).add_prefix("term_")

df["script_sim6"] = [
    analyze.cosine_similarity_row(matrix6, row, df.loc[row].skill)
    for row in matrix6.index
]

# %% Add 50, 100, 150, 200 LSA topics
matrix7 = process_text.vectorize_text(
    df,
    "new_text",
    remove_stopwords=True,
    tfidf=True,
    lemma=True,
    lsa=True,
    n_components=50,
).add_prefix("term_")


df["script_sim7"] = [
    analyze.cosine_similarity_row(matrix7, row, df.loc[row].skill)
    for row in matrix7.index
]
# %%
matrix8 = process_text.vectorize_text(
    df,
    "new_text",
    remove_stopwords=True,
    tfidf=True,
    lemma=True,
    lsa=True,
    n_components=200,
).add_prefix("term_")

df["script_sim8"] = [
    analyze.cosine_similarity_row(matrix8, row, df.loc[row].skill)
    for row in matrix8.index
]


# %%

df[df.study != "model"][
    [
        "study",
        "id",
        "year",
        "semester",
        "scenario",
        "skill",
        "coach",
        "script_sim1",
        "script_sim2",
        "script_sim3",
        "script_sim4",
        "script_sim5",
        "script_sim6",
        "script_sim7",
        "script_sim8",
    ]
].to_csv(start.CLEAN_FILEPATH + "script_sims.csv")

# %%


# %% Replicability


def create_replicability_columns(doc_term_matrix: pd.DataFrame, column_prefix: str):
    matrix = (
        df[["study", "id"]]
        .merge(doc_term_matrix, left_index=True, right_index=True)
        .reset_index()
        .set_index(["study", "id"])
        .drop(labels="filename", axis=1)
    )
    df[column_prefix + "study1"] = analyze.pairwise_distance(
        matrix, matrix.loc["spring2018"]
    )
    df[column_prefix + "study2"] = analyze.pairwise_distance(
        matrix, matrix.loc["spring2019"]
    )
    df[column_prefix + "study3"] = analyze.pairwise_distance(
        matrix, matrix.loc["fall2019TAP"]
    )
    df[column_prefix + "study4"] = analyze.pairwise_distance(
        matrix, matrix.loc["fall2017"]
    )
    df[column_prefix + "study5"] = analyze.pairwise_distance(
        matrix, matrix.loc["fall2018"]
    )

    return matrix


create_replicability_columns(matrix1, "rep1_")
create_replicability_columns(matrix2, "rep2_")
create_replicability_columns(matrix3, "rep3_")
create_replicability_columns(matrix4, "rep4_")
create_replicability_columns(matrix5, "rep5_")


columns = [
    "study",
    "id",
    "year",
    "semester",
    "scenario",
    "skill",
    "coach",
]
columns = columns + [col for col in df if col.startswith("rep")]
df[df.study != "model"][columns].to_csv(start.CLEAN_FILEPATH + "study_sims.csv")  # %%

# # %%

# %%
