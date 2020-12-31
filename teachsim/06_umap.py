# %%
import altair as alt
import numpy as np
import pandas as pd
import sklearn.cluster
import umap

from docsim.library import start
from docsim.library import analyze

FILE = start.clean_filepath + "matrix_stop_wgt_lsa.csv"
TRANSCRIPTS_FILE = start.clean_filepath + "text_transcripts.csv"
TEXT_SCRIPTS_FILE = start.clean_filepath + "text_scripts.csv"
TRANSCRIPTS_ID_COL = "id"
RESTRICTED_STUDIES = ["fall2017", "fall2018"]
TEXT_COLUMN = "text"
MODEL_INDEX = "model"
MODEL_STARTSWITH = "feedback"

NUMBER_OF_CLUSTERS = 6

SKILL = "feedback2"
COLUMNS_OF_INTEREST = ["year", "semester", "scenario", "coach", "skill"]
STUDIES_TO_CONSIDER = ["fall2018", "model"]  # Add in others (like "fall2017") here.

# %%

matrix = pd.read_csv(FILE).set_index(["study", "id"])

transcript_df = pd.read_csv(TRANSCRIPTS_FILE)
transcript_df[TRANSCRIPTS_ID_COL] = transcript_df.id.astype(str)
transcript_df = transcript_df.set_index(["study", "id"])

script_df = pd.read_csv(TEXT_SCRIPTS_FILE).set_index(["study", "id"])
text_df = transcript_df.append(script_df)

text_df = text_df[COLUMNS_OF_INTEREST]
big_df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

# %%
df = big_df[big_df.skill == SKILL]


mat_restricted = df.copy()
mat_restricted = mat_restricted.loc[STUDIES_TO_CONSIDER]
mat_cluster = mat_restricted[list(mat_restricted.filter(regex=("term")))]

# %%
X = np.array(mat_cluster)
kmeans = sklearn.cluster.KMeans(n_clusters=NUMBER_OF_CLUSTERS, random_state=0).fit(X)
reducer = umap.UMAP()
embedding = reducer.fit_transform(mat_cluster)

df = pd.DataFrame(embedding, columns=["x", "y"])
df["cluster"] = kmeans.labels_
df["cluster"] = df["cluster"].astype(str)

df_plot = pd.concat([mat_restricted.reset_index(), df], axis=1)
df_plot.loc[
    df_plot["study"] == "model", "cluster"
] = "model"  # Coerce models into same cluster.

# %%
points = (
    alt.Chart(df_plot)
    .mark_point()
    .encode(x="x", y="y", color="cluster", tooltip=["id", "study", "text", "coach"])
)

points


# %%
