# %%
import pandas as pd

from docsim.library import start

# %%
replication = pd.read_excel(start.raw_filepath + "replication/capstone_sim_results.xls")
# %%
# script similarity
# lsa, stop, wgt
# behavior study 2
relevant = replication[
    (replication.study == "Behavior Study 2")
    & (replication.docsim_type == "normal")
    & (replication.remove_stopwords == True)
    & (replication.stem == False)
    & (replication.tfidf == True)
    & (replication.LSA == False)
][["sim_id", "filename", "similarity_score"]].set_index("id")

# %%
original = pd.read_csv(start.clean_filepath + "results_spring2019.csv")


# %%
