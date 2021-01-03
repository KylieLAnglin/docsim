# %%

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from openpyxl import load_workbook

from docsim.library import start

sns.color_palette("colorblind")

# %%
results = pd.read_csv(start.clean_filepath + "results_stop_stem_wgt_lsa.csv").set_index(
    ["study", "id"]
)
results["study"] = [i[0] for i in results.index]
results["study_sim"] = np.where(
    results.study == "fall2017",
    results.sim_fall2017,
    np.where(
        results.study == "fall2018",
        results.sim_fall2018,
        np.where(
            results.study == "spring2018",
            results.sim_spring2018,
            np.where(
                results.study == "spring2019",
                results.sim_spring2019,
                np.where(
                    results.study == "fall2019TAP", results.sim_fall2019TAP, np.nan
                ),
            ),
        ),
    ),
)

# %% Giant Histogram

studies = ["fall2017", "fall2018", "spring2018", "spring2019", "fall2019TAP"]

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

sns.distplot(
    results.loc[studies]["script_sim"],
    hist=True,
    kde=False,
    bins=int(180 / 5),
    color="darkblue",
    hist_kws={"edgecolor": "black"},
    kde_kws={"linewidth": 4},
)
ax.set_xlabel("Adherence Scores")

# %% By Study
study_labels = {
    "fall2017": "Feedback 1",
    "fall2018": "Feedback 2",
    "spring2018": "Behavior 1",
    "spring2019": "Behavior 2",
    "fall2019TAP": "Behavior 3",
}

study_colors = {
    "fall2017": "navy",
    "fall2018": "blue",
    "spring2018": "lightcoral",
    "spring2019": "maroon",
    "fall2019TAP": "sandybrown",
}

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))


for study in studies:
    subset = results.loc[study]

    # Draw the density plot
    sns.distplot(
        subset["script_sim"],
        hist=False,
        kde=True,
        kde_kws={"linewidth": 3},
        label=study_labels[study],
    )

sns.color_palette("colorblind")


# Add lines for high and low-fidelity
# ax.axvline(x=0.10, color="black")
# ax.axvline(x=0.70, color="black")


# Plot formatting
plt.legend(prop={"size": 16}, title="Study")
plt.title("Density Plots, Disaggregated by Study", fontsize=30)
plt.xlabel("Adherence", fontsize=20)
plt.ylabel("Density", fontsize=20)


# %%
