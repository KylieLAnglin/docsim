# %%
from docsim.library import start
from docsim.library import clean_text

# %%
ideal_behavior_dict = clean_text.import_text(
    start.raw_filepath + "models/", pattern="Classroom Management*.docx"
)
ideal_behavior_df = pd.DataFrame.from_dict(ideal_behavior_dict, orient="index")
ideal_behavior_df["scenario"] = "behavior"
ideal_behavior_df["study"] = "model"


# %% Add skill column
skill_dict = {" A": "1", " B": "2", " C": "3", " D": "4"}
ideal_behavior_df["skill"] = ideal_behavior_df.index.str[26:28]
ideal_behavior_df["skill"] = ideal_behavior_df["skill"].map(skill_dict).astype(int)

ideal_behavior_df = ideal_behavior_df.rename(columns={0: "clean_text"})
ideal_behavior_df = ideal_behavior_df.reset_index().rename(columns={"index": "doc"})

# %%

ideal_behavior_df.to_csv(start.clean_filepath + "text_scripts.csv", index=False)
