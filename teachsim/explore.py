# %%
# %%
import numpy as np
import pandas as pd
from openpyxl import load_workbook

from docsim.library import start
from docsim.library import process_text

# %%

results = pd.read_csv(start.clean_filepath + "results_stop.csv").set_index(
    ["study", "id"]
)
id1 = results.loc["fall2017"][["sim_spring2018"]].idxmax().astype(int)
id2 = results.loc["spring2018"][["sim_spring2018"]].idxmax().astype(int)
id3 = results.loc["fall2017"][["script_sim"]].idxmax().astype(int)
id4 = results.loc["fall2017"][["script_sim"]].idxmin().astype(int)


print(id1, id2)
# Compare Fall 2017 87 (most similar to behavior study 1) to /
# Spring 2018 14 (most similar to other in study)

matrix = pd.read_csv(start.clean_filepath + "matrix_stop_stem_wgt.csv").set_index(
    ["study", "id"]
)

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
