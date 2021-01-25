# %%
import pandas as pd

from docsim.library import start
from docsim.library import process_text
from docsim.library import analyze
from docsim.library import clean_text

# %%

df_corpus = pd.read_csv(start.CLEAN_FILEPATH + "text_transcripts.csv")
df_ideal = pd.read_csv(start.CLEAN_FILEPATH + "text_scriptsV2.csv")
df = df_corpus.append(df_ideal)

df["filename"] = df.filename.str.replace(".docx", "")
df = df.set_index("filename")

df = df.dropna(subset=["skill"])

# %%
families = {
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
    ],
    "avatar": ["Ethan", "Dev"],
}

# %%

df["new_text"] = [
    clean_text.word_family_from_dict(text, families) for text in df.clean_text
]

# %%
matrix = process_text.vectorize_text(
    df, "new_text", remove_stopwords=True, tfidf=False, lemma=True, lsa=False
).add_prefix("term_")

df["script_sim1"] = [
    analyze.cosine_similarity_row(matrix, row, df.loc[row].skill)
    for row in matrix.index
]

process_text.what_words_matter(matrix, "6-2C", "behavior2", 10)
process_text.what_words_matter(matrix, "49-2C", "behavior3", 10)


# %%

df["script_sim1"].to_csv(start.CLEAN_FILEPATH + "vectorizations.csv")

# %%
