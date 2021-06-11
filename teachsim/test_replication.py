import pandas as pd


old = pd.read_csv("/Users/kylie/Dropbox/Active/docsim/data/clean/script_sims.csv")

new = pd.read_csv(
    "/Users/kylie/Dropbox/Active/Semantic Similarity Replication Files/data/clean/script_sims.csv"
)


old_new = old[["study", "id", "script_sim3", "script_sim5"]].merge(
    new[["study", "id", "filename", "script_sim3", "script_sim5"]],
    on=["study", "id"],
    how="outer",
    indicator=True,
)
