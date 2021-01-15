# %%
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


from docsim.library import start
from docsim.library import analyze

# %%
MATRIX_FILE = start.CLEAN_FILEPATH + "matrix" + PROCESSING + ".csv"
TRANSCRIPTS_FILE = start.CLEAN_FILEPATH + "text_transcripts.csv"
SCRIPTS_FILE = start.CLEAN_FILEPATH + "text_scripts.csv"
RESULTS_FILE = start.CLEAN_FILEPATH + "results" + PROCESSING + ".csv"


PROCESSING = "_stop_stem_wgt"
COLUMNS_OF_INTEREST = ["year", "semester", "scenario", "coach", "skill"]
STUDIES_TO_CONSIDER = ["fall2017", "fall2018"]  # Add in others (like "fall2017") here.

# %%
matrix = pd.read_csv(MATRIX_FILE)
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

# Transcripts and scripts
transcript_df = pd.read_csv(TRANSCRIPTS_FILE)
transcript_df["id"] = transcript_df.id.astype(str)
transcript_df = transcript_df.set_index(["study", "id"])
script_df = pd.read_csv(SCRIPTS_FILE).set_index(["study", "id"])
text_df = transcript_df.append(script_df)
text_df = text_df[COLUMNS_OF_INTEREST]


# Results
results = pd.read_csv(RESULTS_FILE).set_index(["study", "id"])

big_df = text_df.merge(
    results[
        [
            "script_sim",
        ]
    ],
    how="left",
    left_index=True,
    right_index=True,
)

big_df = big_df.merge(
    matrix, how="left", left_index=True, right_index=True, indicator=True
)
df = big_df.loc[STUDIES_TO_CONSIDER]

doc_term_col = list(df.filter(regex=("term")))

doc_term_matrix = df.copy()
doc_term_matrix = doc_term_matrix[doc_term_col]

# %%
# #QUESTION: Normalize before PCA?
# doc_term_matrix_std = StandardScaler().fit_transform(doc_term_matrix)


pca = PCA(n_components=2)
X_r = pca.fit(doc_term_matrix).transform(doc_term_matrix)

print(
    "explained variance ratio (first two components): %s"
    % str(pca.explained_variance_ratio_)
)
pca1 = [i[0] for i in X_r]
pca2 = [i[1] for i in X_r]

df["pca1"] = pca1
df["pca2"] = pca2


# %%
plt.style.use("fivethirtyeight")
fig = plt.figure()
ax = plt.axes(projection="3d")
ax.scatter3D(df.script_sim, df.pca2, df.pca1, c=df.script_sim, cmap="Greens")
# Zach: I need a tool tip that shows the id.

# %%
