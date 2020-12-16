# %%
import pandas as pd

from docsim.library import start
from docsim.library import analyze

# %%

transcript_df = pd.read_csv(start.clean_filepath + "text_transcripts.csv").set_index(
    "id"
)
script_df = pd.read_csv(start.clean_filepath + "text_scripts.csv").set_index("id")
df = transcript_df.append(script_df)

df = df[["study", "year", "semester", "scenario", "coach", "skill"]]
df.index = df.index.map(str)

matrix = pd.read_csv(start.clean_filepath + "matrix_stop_wgt_lsa.csv").set_index("id")
matrix = matrix.add_prefix("term_")
matrix.index = matrix.index.map(str)

df = df.merge(matrix, how="left", left_index=True, right_index=True)

# %%


doc_term_matrix = df[list(df.filter(regex=("term")))]

values = []
new_df = df[df.study == "spring2019"][[]]
for doc in df[df.study == "spring2019"].index:
    value = analyze.max_sim_of_rows(
        matrix=doc_term_matrix,
        main_index=doc,
        comp_indices=list(
            df[
                (df.study == "model")
                & (df.scenario == "behavior")
                & (df.skill == df.loc[doc].skill)
            ].index
        ),
    )
    values.append(value)
new_df["script_sim"] = values

new_df.to_csv(start.clean_filepath + "results_spring2019.csv")
