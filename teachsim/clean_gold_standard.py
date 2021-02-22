# %%
import numpy as np
import pandas as pd

from docsim.library import start
from docsim.library import qualtrics

pd.set_option("display.max_rows", 500)

QUALTRICS_EXPORT = (
    start.RAW_FILEPATH + "/validation/" + "Fidelity Coding survey 2021 02 17.csv"
)


gold = pd.read_csv(QUALTRICS_EXPORT)
labels = qualtrics.extract_column_labels(csv_path=QUALTRICS_EXPORT)
gold = qualtrics.select_valid_rows(survey=gold, keep_previews=False, min_duration=15)
gold = gold[["Q2", "Q3", "SC1", "SC3"]]
gold = gold.rename(
    columns={
        "Q2": "qualtrics_filename",
        "Q3": "scenario",
        "SC1": "fidelity",
        "SC3": "quality",
    }
)
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace("-updated", "")
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace("_updated", "")
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace(" (updated)", "")
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace("_Transcript", "")
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace(" Transcript", "")
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace("Scored", "")
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace("Score", "")
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace(".docx", "")
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace(".doc", "")

gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace(
    "C", "c"
)  # make sure already dropped c words
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace("c_", "")
gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace("c", "")


gold["qualtrics_filename"] = gold.qualtrics_filename.str.replace("-", "_")


# %%
transcripts = pd.read_csv(start.CLEAN_FILEPATH + "text_transcripts.csv")
transcripts = transcripts[
    [
        "study",
        "id",
        "filename",
        "year",
        "semester",
        "scenario",
        "skill",
        "skill_name",
        "coach",
    ]
]
transcripts["filename"] = transcripts.filename.str.replace(".docx", "")
transcripts["filename"] = transcripts.filename.str.replace("_Transcript", "")
transcripts["filename"] = transcripts.filename.str.replace("C", "c")
transcripts["filename"] = transcripts.filename.str.replace("c", "")
transcripts["filename"] = transcripts.filename.str.replace("-", "_")

# %%
linking = transcripts.merge(
    gold,
    how="outer",
    left_on="filename",
    right_on="qualtrics_filename",
    indicator="_merge",
)

linking = linking.sort_values(by=["study", "id", "qualtrics_filename"])

linking[["study", "id", "filename", "qualtrics_filename", "_merge"]].to_csv(
    start.RAW_FILEPATH + "qualtrics_linking.csv"
)

# %%

cleaned_gold = transcripts.merge(
    gold[["qualtrics_filename", "fidelity", "quality"]],
    how="left",
    left_on="filename",
    right_on="qualtrics_filename",
)

# %%
cleaned_gold = cleaned_gold[
    [
        "study",
        "id",
        "filename",
        "qualtrics_filename",
        "year",
        "semester",
        "scenario",
        "skill",
        "skill_name",
        "coach",
        "fidelity",
        "quality",
    ]
]

cleaned_gold = cleaned_gold[cleaned_gold.scenario == "behavior"]
# %% Random hold-out sample
subset = cleaned_gold.sample(60, random_state=7)
cleaned_gold["training"] = np.where(cleaned_gold.index.isin(subset.index), 1, 0)

# %%
cleaned_gold.to_csv(
    start.RAW_FILEPATH + "/validation/" + "human_codes.csv", index=False
)

# %%
