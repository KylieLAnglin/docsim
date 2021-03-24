# %%
import numpy as np
import pandas as pd

from docsim.library import start
from docsim.library import qualtrics

pd.set_option("display.max_rows", 500)

QUALTRICS_EXPORT = (
    start.RAW_FILEPATH + "/validation/" + "Fidelity Coding survey 2021 02 24.csv"
)


gold = pd.read_csv(QUALTRICS_EXPORT)
labels = qualtrics.extract_column_labels(csv_path=QUALTRICS_EXPORT)

# %%
gold = qualtrics.select_valid_rows(survey=gold, keep_previews=False, min_duration=15)
# gold = gold[["Q2", "Q3", "SC1", "SC3", "Q26#1_1", "Q26#1_2", "Q26#1_3", "Q26#1_4"]]
components = {
    "Q4_1": "open_1",
    "Q4_2": "open_2",
    "Q4_3": "open_3",
    "Q5_1": "skill_1",
    "Q5_2": "skill_2",
    "Q5_3": "skill_3",
    "Q5_4": "skill_4",
    "Q5_5": "skill_5",
    "Q5_6": "skill_6",
    "Q6_1": "practice_1",
    "Q6_2": "practice_2",
    "Q6_3": "practice_3",
    "Q6_4": "practice_4",
    "Q6_5": "practice_5",
    "Q6_6": "practice_6",
    "Q7_1": "close_1",
    "Q7_2": "close_2",
}

gold = gold.rename(columns=components)

replace_categorical_values = {"Yes (1)": 1, "No (0)": 0, "Partially (1/2)": 0.5}
gold = gold.replace(replace_categorical_values)

other_vars = {
    "Q2": "qualtrics_filename",
    "Q3": "scenario",
    "SC1": "fidelity_auto_sum",
    "SC3": "quality",
    "Q26#1_1": "content_opening_cat",
    "Q26#1_2": "content_positive_cat",
    "Q26#1_3": "content_growth_cat",
    "Q26#1_4": "content_closing_cat",
}

gold = gold.rename(columns=other_vars)

keep_vars = list(components.values()) + list(other_vars.values())

gold = gold[keep_vars]

# %%

gold["fidelity"] = gold[list(components.values())].sum(axis=1)

gold["fidelity_auto_sum"] = gold.fidelity_auto_sum.astype(float)

gold["fidelity_skills"] = gold[
    ["skill_1", "skill_2", "skill_3", "skill_4", "skill_5", "skill_6"]
].sum(axis=1)

gold["fidelity_practice"] = gold[
    ["practice_1", "practice_2", "practice_3", "practice_4", "practice_5", "practice_6"]
].sum(axis=1)


gold["fidelity_open"] = gold[["open_1", "open_2"]].sum(axis=1)

gold["fidelity_close"] = gold[["close_1", "close_2"]].sum(axis=1)

gold["quality"] = gold.quality.astype(float)

# %%


gold["fidelity_high_reliability"] = gold[
    [
        "open_1",
        "open_2",
        "open_3",
        "skill_1",
        "skill_2",
        "skill_3",
        # "skill_4",
        "skill_5",
        "skill_6",
        "practice_1",
        "practice_2",
        # "practice_3",
        "practice_4",
        "practice_5",
        "practice_6",
        "close_1",
        # "close_2",
    ]
].sum(axis=1)

# %%
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

gold["double_coded"] = gold.duplicated(subset=["qualtrics_filename"], keep=False)


rubric_mapping = {
    "0 - misaligned": 0,
    "1-poorly aligned": 1,
    "2-somewhat aligned": 2,
    "3-well aligned": 3,
}


gold["content_opening"] = gold.content_opening_cat.map(rubric_mapping)
gold["content_positive"] = gold.content_positive_cat.map(rubric_mapping)
gold["content_growth"] = gold.content_growth_cat.map(rubric_mapping)
gold["content_closing"] = gold.content_closing_cat.map(rubric_mapping)

gold["fidelity_content_opening"] = gold.fidelity_open * gold.content_opening
gold["fidelity_content_skill"] = gold.fidelity_open * gold.content_positive
gold["fidelity_content_practice"] = gold.fidelity_open * gold.content_growth
gold["fidelity_content_close"] = gold.fidelity_open * gold.content_closing

gold["fidelity_content"] = gold[
    [
        "fidelity_content_opening",
        "fidelity_content_skill",
        "fidelity_content_practice",
        "fidelity_content_close",
    ]
].sum(axis=1)


gold["content"] = (
    gold.content_opening
    + gold.content_positive
    + gold.content_growth
    + gold.content_closing
) / 4

duplicates = gold[gold.double_coded == True]
duplicates = (
    duplicates.groupby(["qualtrics_filename", "scenario"])
    .mean()
    .reset_index()
    .set_index("qualtrics_filename")
)

gold = gold[gold.double_coded == False].set_index("qualtrics_filename")
gold = gold.append(duplicates)
gold = gold.reset_index()

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
    gold[
        [
            "qualtrics_filename",
            "fidelity",
            "quality",
            "content",
            "fidelity_high_reliability",
            "fidelity_skills",
            "fidelity_practice",
            "fidelity_open",
            "fidelity_close",
            "fidelity_content",
        ]
    ],
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
        "content",
        "fidelity_high_reliability",
        "fidelity_skills",
        "fidelity_practice",
        "fidelity_open",
        "fidelity_close",
        "fidelity_content",
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
