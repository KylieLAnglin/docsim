# %%
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from docsim.library import start

# %%
results = pd.read_csv(start.CLEAN_FILEPATH + "results_stop_stem_wgt_lsa.csv")
results["filename"] = results.filename.str.replace(".docx", "")
results = results.set_index("filename")
# %%
gold_standard = pd.read_excel(start.RAW_FILEPATH + "Fidelity Coding Behavior.xlsx")
gold_standard = gold_standard.rename(
    columns={
        "Transcript File Name": "doc",
        "Opening Components (out of 3)": "opening",
        "Skill-Building Components (Out of 6)": "skill_building",
        "Practice Components (out of 6)": "practice",
        "Closing Components (out of 2)": "closing",
    }
).set_index("doc")

gold_standard["fidelity"] = (
    gold_standard.opening
    + gold_standard.skill_building
    + gold_standard.practice
    + gold_standard.closing
)

# %%
gold_standard = gold_standard[["fidelity"]]

validation = gold_standard.merge(
    results, how="inner", left_index=True, right_index=True
)

validation = validation[["script_sim", "fidelity"]]

# %%

mod = smf.ols(formula="script_sim ~ fidelity", data=validation)
res = mod.fit()
print(res.summary())


# %%
plt.plot(validation.script_sim, validation.fidelity, "o", color="black")
# %%
