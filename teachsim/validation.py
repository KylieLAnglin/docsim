# %%
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from docsim.library import start
from docsim.library import analyze
from docsim.library import process_text

from openpyxl import load_workbook


# %% import

training = pd.read_csv(start.RAW_FILEPATH + "/validation/" + "human_codes.csv")

results = pd.read_csv(start.CLEAN_FILEPATH + "vectorizations.csv")

training = training.merge(
    results, how="left", left_on="filename", right_on="filename", indicator=True
)

training = training[training.training == 0]


# %%
file = start.TABLE_FILEPATH + "validation.xlsx"
wb = load_workbook(file)
ws = wb.active
row = 4
col = 2

# %%
mod = smf.ols(formula="script_sim0 ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())
ws.cell(row=row, column=col).value = round(res.rsquared, 2)
col = col + 1
plt.plot(training.fidelity, training.script_sim0, "o", color="black", alpha=0.1)

training.fidelity.corr(training.script_sim0)

# %% New
mod = smf.ols(formula="script_sim1 ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())
ws.cell(row=row, column=col).value = round(res.rsquared, 2)
col = col + 1

plt.plot(training.fidelity, training.script_sim1, "o", color="black", alpha=0.1)

training.fidelity.corr(training.script_sim1)

# %%
mod = smf.ols(formula="script_sim2 ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())
ws.cell(row=row, column=col).value = round(res.rsquared, 2)
col = col + 1

plt.plot(training.fidelity, training.script_sim2, "o", color="black", alpha=0.1)

# %%
mod = smf.ols(formula="script_sim3 ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())
ws.cell(row=row, column=col).value = round(res.rsquared, 2)
col = col + 1

plt.plot(training.fidelity, training.script_sim3, "o", color="black", alpha=0.1)


# %%
mod = smf.ols(formula="script_sim4 ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())
ws.cell(row=row, column=col).value = round(res.rsquared, 2)
col = col + 1

# %%

mod = smf.ols(formula="script_sim5 ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())
ws.cell(row=row, column=col).value = round(res.rsquared, 2)
col = col + 1

# %%
mod = smf.ols(formula="script_sim6 ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())
ws.cell(row=row, column=col).value = round(res.rsquared, 2)
col = col + 1

# %%
mod = smf.ols(formula="script_sim7 ~ + fidelity", data=training)
res = mod.fit()
print(res.summary())
ws.cell(row=row, column=col).value = round(res.rsquared, 2)

# %%
wb.save(file)

# %%
