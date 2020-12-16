# %%
from docsim.library import start
from docsim.library import clean_text

# %%
ideal_behavior_dict = clean_text.import_text(
    start.raw_filepath + "models/", pattern="Classroom Management*.docx"
)
df = pd.DataFrame.from_dict(ideal_behavior_dict, orient="index")
df = df.rename(columns={0: "clean_text"})

df["scenario"] = "behavior"
df["study"] = "model"

df["skill"] = [int(list(filter(str.isdigit, doc))[0]) for doc in df.index]
df = df.reset_index().rename(columns={"index": "doc"})
df["id"] = [doc[-6:-5] for doc in df.doc]
df["id"] = df.scenario + df.skill.astype(str) + df.id

df = df.set_index("id")
# %%

df.to_csv(start.clean_filepath + "text_scripts.csv", index=False)
