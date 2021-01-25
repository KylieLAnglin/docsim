import numpy as np
import pandas as pd

from docsim.library import start

# %% Import Results
results = pd.read_csv(start.CLEAN_FILEPATH + "results_stop_stem_wgt_lsa.csv")
results["filename"] = results.filename.str.replace(".docx", "")
results["filename"] = results.filename.str.replace("_Transcript", "")


# do not change
training = results.set_index("filename")
training = training[training.study != "model"]
training = training[training.scenario == "behavior"]
training = training.sample(50, random_state=7)


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
gold_standard = gold_standard[["fidelity"]]

# %%

validation = gold_standard.merge(
    training, how="inner", left_index=True, right_index=True
)

validation = validation[
    [
        "study",
        "id",
        "year",
        "semester",
        "scenario",
        "skill",
        "coach",
        "fidelity",
        "script_sim",
    ]
]

validation = (
    validation.reset_index().rename(columns={"index": "filename"}).set_index("filename")
)
# %%

validation.to_csv(start.TABLE_FILEPATH + "training_full.csv")


# # %% Import Results
# results = pd.read_csv(start.CLEAN_FILEPATH + "results_stop_stem_wgt_lsa.csv")
# results["filename"] = results.filename.str.replace(".docx", "")
# results["filename"] = results.filename.str.replace("_Transcript", "")


# # do not change
# training = results.set_index("filename")
# training = training[training.study != "model"]
# training = training[training.scenario == "behavior"]
# training = training.sample(50, random_state=7)


# # %%
# # gold_standard = pd.read_excel(start.RAW_FILEPATH + "Fidelity Coding Behavior.xlsx")
# gold_standard = pd.read_excel(start.RAW_FILEPATH + "Fidelity Behavior.xlsx")
# gold_standard = gold_standard.rename(
#     columns={
#         "Transcript File Name": "doc",
#         "Opening Components (out of 3)": "opening",
#         "Skill-Building Components (Out of 6)": "skill_building",
#         "Practice Components (out of 6)": "practice",
#         "Closing Components (out of 2)": "closing",
#     }
# ).set_index("doc")

# # %%
# gold_standard["fidelity"] = (
#     gold_standard["1"]
#     + gold_standard["2"]
#     + gold_standard["4"]
#     + gold_standard["5"]
#     + gold_standard["7"]
#     + gold_standard["10"]
#     + gold_standard["12"]
#     + gold_standard["14"]
#     + gold_standard["16"]
# )

# gold_standard["fidelity_full"] = (
#     gold_standard["1"]
#     + gold_standard["2"]
#     + gold_standard["3"]
#     + gold_standard["4"]
#     + gold_standard["5"]
#     + gold_standard["6"]
#     + gold_standard["7"]
#     + gold_standard["8"]
#     + gold_standard["9"]
#     + gold_standard["10"]
#     + gold_standard["11"]
#     + gold_standard["12"]
#     + gold_standard["13"]
#     + gold_standard["14"]
#     + gold_standard["15"]
#     + gold_standard["16"]
#     + gold_standard["17"]
# )

# gold_standard = gold_standard[["fidelity", "fidelity_full"]]

# plt.hist(gold_standard.fidelity)
# # %%

# validation = gold_standard.merge(
#     training, how="inner", left_index=True, right_index=True
# )

# validation = validation[
#     [
#         "study",
#         "id",
#         "year",
#         "semester",
#         "scenario",
#         "skill",
#         "coach",
#         "fidelity",
#         "fidelity_full",
#         "script_sim",
#     ]
# ]

# validation.to_csv(start.TABLE_FILEPATH + "training_simplified.csv")
# # %%

# mod = smf.ols(formula="script_sim ~ + fidelity_full", data=validation)
# res = mod.fit()
# print(res.summary())

# plt.plot(validation.fidelity, validation.script_sim, "o", color="black", alpha=0.1)


# # %%
