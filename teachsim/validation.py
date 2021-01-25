# %%
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from docsim.library import start
from docsim.library import analyze
from docsim.library import process_text

# %% import

training = pd.read_csv(start.TABLE_FILEPATH + "training.csv")

# %%

mod = smf.ols(formula="script_sim ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())


# %%
plt.plot(training.fidelity, training.script_sim, "o", color="black", alpha=0.1)


# %%
validation[validation.fidelity == 10]

# %%
matrix = pd.read_csv(start.CLEAN_FILEPATH + "matrix_stop_stem_wgt.csv")
matrix["id"] = matrix.id.astype(str)
matrix = matrix.set_index(["study", "id"])
matrix = matrix[list(matrix.filter(regex=("term")))]


# %%
scripts = results[(results.study == "model") & (results.scenario == "behavior")]
scripts = scripts.set_index(["study", "id"])
script_list = scripts.index.tolist()

analyze.max_sim_of_rows_index(matrix, ("spring2019", "58"), script_list)

process_text.what_words_matter(
    matrix, ("spring2019", "58"), ("model", "behavior2a"), 10
)
# %%
