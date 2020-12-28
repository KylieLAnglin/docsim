# %%

import pandas as pd

from docsim.library import start
from docsim.library import analyze

# %%
matrix = pd.read_csv(start.clean_filepath + "matrix_stop_wgt_lsa.csv").set_index(
    ["study", "id"]
)

transcript_df = pd.read_csv(start.clean_filepath + "text_transcripts.csv")
transcript_df["id"] = transcript_df.id.astype(str)
transcript_df = transcript_df.set_index(["study", "id"])

script_df = pd.read_csv(start.clean_filepath + "text_scripts.csv").set_index(
    ["study", "id"]
)
text_df = transcript_df.append(script_df)

text_df = text_df[["year", "semester", "scenario", "coach", "skill"]]

big_df = text_df.merge(matrix, how="left", left_index=True, right_index=True)


# %%
df = big_df[big_df.skill == "feedback2"]

doc_term_matrix = df[list(df.filter(regex=("term")))]

# %%
