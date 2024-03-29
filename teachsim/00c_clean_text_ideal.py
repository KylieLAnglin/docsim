# %%
import pandas as pd

from docsim.library import start
from docsim.library import clean_text

# %% Behavior
ideal_dict = clean_text.import_text(
    start.RAW_FILEPATH + "models/", pattern="behavior*.docx"
)
df = pd.DataFrame.from_dict(ideal_dict, orient="index")
df = df.rename(columns={0: "clean_text"})

df["scenario"] = "behavior"
df["study"] = "model"
df["skill"] = ["behavior" + str(list(filter(str.isdigit, doc))[0]) for doc in df.index]


behavior = df

# %% Feedback
ideal_dict = clean_text.import_text(
    start.RAW_FILEPATH + "models/", pattern="feedback*.docx"
)
df = pd.DataFrame.from_dict(ideal_dict, orient="index")
df = df.rename(columns={0: "clean_text"})

df["scenario"] = "feedback"
df["study"] = "model"
df["skill"] = ["feedback" + str(list(filter(str.isdigit, doc))[0]) for doc in df.index]


feedback = df
# %%
model_df = pd.concat([behavior, feedback])
model_df = model_df.reset_index().rename(columns={"index": "filename"})
model_df["id"] = model_df.skill
model_df["filename"] = model_df.skill


# %%
model_df.to_csv(start.CLEAN_FILEPATH + "text_scripts.csv", index=False)
