# %%
# %%
import numpy as np
import pandas as pd
from openpyxl import load_workbook

from docsim.library import start
from docsim.library import process_text
from docsim.library import analyze

# %%

results = pd.read_csv(start.clean_filepath + "results_stop_stem_wgt_lsa.csv").set_index(
    ["study", "id"]
)

studies = ["fall2017", "fall2018", "spring2018", "spring2019", "fall2019TAP"]

matrix = pd.read_csv(start.clean_filepath + "results_stop_stem_wgt_lsa.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])

doc_term_col = list(matrix.filter(regex=("term")))

doc_term_matrix = matrix.copy()
doc_term_matrix = doc_term_matrix[doc_term_col]
# %% Low and high fidelity
print(
    "Low fidelity: ", results.loc[["spring2018", "spring2019"]]["script_sim"].idxmin()
)
# or 73, 91 has conversation at beginning about the sound
print(
    "High fidelity: ", results.loc[["spring2018", "spring2019"]]["script_sim"].idxmax()
)

# %%

print(
    analyze.max_sim_of_rows_index(
        doc_term_matrix, ("fall2017", "87"), list(doc_term_matrix.loc[studies].index)
    )
)
# %%
process_text.what_words_matter(
    doc_term_matrix, ("fall2017", "87"), ("fall2017", "31"), 15
)

print(
    analyze.max_sim_of_rows_index(
        doc_term_matrix, ("fall2017", "91"), list(doc_term_matrix.loc[studies].index)
    )
)

print(
    analyze.max_sim_of_rows_index(
        doc_term_matrix, ("fall2017", "3"), list(doc_term_matrix.loc[studies].index)
    )
)

process_text.what_words_matter(
    doc_term_matrix, ("fall2017", "5"), ("fall2017", "22"), 15
)

process_text.what_words_matter(
    doc_term_matrix, ("fall2017", "5"), ("fall2017", "67"), 15
)
# %%

id1 = results.loc["fall2017"][["sim_fall2017"]].idxmax().astype(int)
id2 = results.loc["spring2018"][["sim_spring2018"]].idxmax().astype(int)
id3 = results.loc["fall2017"][["script_sim"]].idxmax().astype(int)
id4 = results.loc["fall2017"][["script_sim"]].idxmin().astype(int)


print(id1, id2)
# Compare Fall 2017 87 (most similar to behavior study 1) to /
# Spring 2018 14 (most similar to other in study)


# %%
test = process_text.what_words_matter(
    matrix[list(matrix.filter(regex=("term")))],
    ("fall2017", 73),
    ("model", "feedback2a"),
    show_num=10,
)
# %%

id3 = results.loc["fall2017"][["script_sim"]].idxmax().astype(int)
id4 = results.loc["fall2017"][["script_sim"]].idxmin().astype(int)
