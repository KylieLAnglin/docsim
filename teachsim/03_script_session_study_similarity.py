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


# %%
doc_term_matrix = df[list(df.filter(regex=("term")))]

df["peers"] = analyze.row_matches_in_lists(df, col_to_match="skill")
study_groups = df.groupby(["study", "scenario"])

new_df = df[df.study == "spring2019"][["study", "year", "semester", "skill"]]
new_df["script_sim"] = [
    analyze.max_sim_of_rows(
        matrix=doc_term_matrix,
        main_index=i,
        comp_indices=list(
            set(study_groups.groups["model", "behavior"]) & set(df.loc[i].peers)
        ),
    )
    for i in study_groups.groups["spring2019", "behavior"]
]

# %%

df.to_csv(start.clean_filepath + "results_spring2019.csv")

# %%
