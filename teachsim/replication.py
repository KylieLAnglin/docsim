# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from docsim.library import start

# %%
replication = pd.read_excel(start.raw_filepath + "replication/capstone_sim_results.xls")
# %%
# script similarity
# lsa, stop, wgt
# behavior study 2
replication = replication[
    (replication.study == "Behavior Study 2")
    & (replication.docsim_type == "normal")
    & (replication.remove_stopwords == False)
    & (replication.stem == False)
    & (replication.tfidf == False)
    & (replication.LSA == False)
].set_index("sim_id")

# %%
original = pd.read_csv(start.clean_filepath + "results_spring2019.csv").set_index("id")


# %%

fig = plt.figure(figsize=(10, 10))
ax = plt.axes()

# ax.set_title('Figure 1: Fidelity Score Distributions', fontsize=15)

bins = np.linspace(0, 0.5, num=10)

sns.distplot(
    original.script_sim,
    hist=False,
    rug=False,
    color="black",
    kde_kws={"linestyle": "solid"},
    label="Kylie",
)

sns.distplot(
    replication.similarity_score,
    hist=False,
    rug=False,
    color="black",
    kde_kws={"linestyle": "dashed"},
    label="Capstone",
)

ax.legend(loc="upper right")
ax.set_xlabel("Adherence Scores")
ax.set_ylabel("Kernel Density")
# %%
fig.savefig(start.table_filepath + "results_spring2019_replication.png")
