# %%
import pandas as pd

from docsim.library import start
from docsim.library import clean_text

# %% Behavior
ideal_dict = clean_text.import_text(
    start.raw_filepath + "models/", pattern="Classroom Management*.docx"
)
df = pd.DataFrame.from_dict(ideal_dict, orient="index")
df = df.rename(columns={0: "clean_text"})

df["scenario"] = "behavior"
df["study"] = "model"
df["skill"] = ["behavior" + str(list(filter(str.isdigit, doc))[0]) for doc in df.index]


behavior = df
# %% Feedback
ideal_dict = clean_text.import_text(
    start.raw_filepath + "models/", pattern="Feedback Model*.docx"
)
df = pd.DataFrame.from_dict(ideal_dict, orient="index")
df = df.rename(columns={0: "clean_text"})

df["scenario"] = "feedback"
df["study"] = "model"
df["skill"] = ["feedback" + str(list(filter(str.isdigit, doc))[0]) for doc in df.index]


feedback = df
# %%
model_df = pd.concat([behavior, feedback])

model_df = model_df.reset_index().rename(columns={"index": "doc"})
model_df["id"] = [doc[-6:-5] for doc in model_df.doc]
model_df["id"] = model_df.skill.astype(str) + model_df.id
model_df = model_df.set_index("id")

# %%
model_df.to_csv(start.clean_filepath + "text_scripts.csv")
