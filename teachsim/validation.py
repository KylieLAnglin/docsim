# %%
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from docsim.library import start
from docsim.library import analyze
from docsim.library import process_text

# %% import

training = pd.read_csv(start.TABLE_FILEPATH + "training_full.csv")

results = pd.read_csv(start.CLEAN_FILEPATH + "vectorizations.csv")

training = training.merge(
    results, how="left", left_on="filename", right_on="filename", indicator=True
)

# training = training[training.training == 1]
# %% Old

mod = smf.ols(formula="script_sim ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())


# %% New
mod = smf.ols(formula="script_sim1 ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())


plt.plot(training.fidelity, training.script_sim1, "o", color="black", alpha=0.1)

training.fidelity.corr(training.script_sim1)

# %%
