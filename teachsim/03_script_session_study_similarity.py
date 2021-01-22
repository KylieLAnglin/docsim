# %%
import pandas as pd

from docsim.library import start
from docsim.library import analyze

# %%

transcript_df = pd.read_csv(start.CLEAN_FILEPATH + "text_transcripts.csv")
transcript_df["id"] = transcript_df.id.astype(str)
transcript_df = transcript_df.set_index(["study", "id"])

script_df = pd.read_csv(start.CLEAN_FILEPATH + "text_scripts.csv").set_index(
    ["study", "id"]
)
text_df = transcript_df.append(script_df)

text_df = text_df[["year", "semester", "filename", "scenario", "coach", "skill"]]

# %% Create results
def create_results(merged_df: pd.DataFrame):

    new_df = merged_df.copy()

    new_df["peers"] = analyze.row_matches_in_lists(new_df, col_to_match="skill")

    doc_term_matrix = new_df[list(new_df.filter(regex=("term")))]

    new_df["script_sim"] = [
        analyze.max_sim_of_rows(
            matrix=doc_term_matrix,
            main_index=i,
            comp_indices=list(
                set(new_df.xs("model", drop_level=False).index)
                & set(new_df.loc[i].peers)
            ),
        )
        for i in new_df.index
    ]

    results = new_df[
        [
            "filename",
            "year",
            "semester",
            "scenario",
            "skill",
            "coach",
            "text",
            "script_sim",
        ]
    ]

    results["sim_fall2017"] = analyze.pairwise_distance(
        doc_term_matrix, doc_term_matrix.loc["fall2017"]
    )

    results["sim_fall2018"] = analyze.pairwise_distance(
        doc_term_matrix, doc_term_matrix.loc["fall2018"]
    )

    results["sim_spring2018"] = analyze.pairwise_distance(
        doc_term_matrix, doc_term_matrix.loc["spring2018"]
    )

    results["sim_spring2019"] = analyze.pairwise_distance(
        doc_term_matrix, doc_term_matrix.loc["spring2019"]
    )

    results["sim_fall2019TAP"] = analyze.pairwise_distance(
        doc_term_matrix, doc_term_matrix.loc["fall2019TAP"]
    )

    return results


# %% No Pre-Processing
matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

results = create_results(merged_df=df)
results.to_csv(start.CLEAN_FILEPATH + "results.csv")

# %%
matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix_stop.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

results = create_results(merged_df=df)
results.to_csv(start.CLEAN_FILEPATH + "results_stop.csv")

# %%
# %%
matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix_stop_wgt.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

results = create_results(merged_df=df)
results.to_csv(start.CLEAN_FILEPATH + "results_stop_wgt.csv")
# %%
matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix_stop_wgt.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

results = create_results(merged_df=df)
results.to_csv(start.CLEAN_FILEPATH + "results_stop_wgt.csv")

# %%

matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix_stop_stem_wgt.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

results = create_results(merged_df=df)
results.to_csv(start.CLEAN_FILEPATH + "results_stop_stem_wgt.csv")
# %%
matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix_stop_wgt_lsa.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

results = create_results(merged_df=df)
results.to_csv(start.CLEAN_FILEPATH + "results_stop_wgt_lsa.csv")
#%%
matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix_stop_stem_wgt_lsa.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

results = create_results(merged_df=df)
results.to_csv(start.CLEAN_FILEPATH + "results_stop_stem_wgt_lsa.csv")


# %% Stop Stem

matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix_stop_stem.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

results = create_results(merged_df=df)
results.to_csv(start.CLEAN_FILEPATH + "results_stop_stem.csv")
# %%
matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix_lsa.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

df = text_df.merge(matrix, how="left", left_index=True, right_index=True)

results = create_results(merged_df=df)
results.to_csv(start.CLEAN_FILEPATH + "results_lsa.csv")
# %%
